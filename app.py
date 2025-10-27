import whois
import discord
from discord import app_commands
from discord.ext import tasks, commands
from dotenv import load_dotenv
import os
from datetime import datetime

# --- Load environment variables ---
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
USER_ID = int(os.getenv("USER_ID"))
DOMAINS_FILE = "domains.txt"

# --- Load domains from file ---
if os.path.exists(DOMAINS_FILE):
    with open(DOMAINS_FILE, "r") as f:
        DOMAINS = [line.strip() for line in f if line.strip()]
else:
    DOMAINS = []

# --- Discord bot setup ---
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

# --- Track domains already notified ---
checked_domains = set()


# --- Save domains to file ---
def save_domains():
    with open(DOMAINS_FILE, "w") as f:
        for domain in DOMAINS:
            f.write(domain + "\n")


# --- Check if domain is available ---
def is_domain_available(domain):
    try:
        info = whois.whois(domain)
        return not bool(info.domain_name)
    except Exception:
        return True  # assume available if WHOIS fails


# --- Function to check all domains and send DMs ---
async def check_all_domains():
    try:
        user = await client.fetch_user(USER_ID)
    except Exception as e:
        print(f"[{datetime.utcnow()}] ❌ Failed to fetch user: {e}")
        return

    for domain in DOMAINS:
        if domain in checked_domains:
            continue
        if is_domain_available(domain):
            try:
                timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
                await user.send(f"✅ Domain **{domain}** is available! ({timestamp})")
                checked_domains.add(domain)
                print(f"[{timestamp}] ✅ DM sent for {domain}")
            except Exception as e:
                print(f"[{datetime.utcnow()}] ❌ Failed to send DM for {domain}: {e}")
        else:
            print(f"[{datetime.utcnow()}] ⚠️ {domain} is still taken")


# --- Task: check domains every 8 hours ---
@tasks.loop(hours=8)
async def check_domains():
    await check_all_domains()


# --- 1️⃣ Slash command: add domain ---
@client.tree.command(name="add", description="Add a domain to watch")
@app_commands.describe(domain="Domain to add")
async def add(interaction: discord.Interaction, domain: str):
    if interaction.user.id != USER_ID:
        await interaction.response.send_message(
            "❌ You cannot use this command.", ephemeral=True
        )
        return
    if domain in DOMAINS:
        await interaction.response.send_message(
            f"⚠️ Domain **{domain}** already in the list.", ephemeral=True
        )
    else:
        DOMAINS.append(domain)
        save_domains()
        await interaction.response.send_message(
            f"✅ Domain **{domain}** added.", ephemeral=True
        )


# --- 2️⃣ Slash command: remove domain ---
@client.tree.command(name="remove", description="Remove a domain from watch list")
@app_commands.describe(domain="Domain to remove")
async def remove(interaction: discord.Interaction, domain: str):
    if interaction.user.id != USER_ID:
        await interaction.response.send_message(
            "❌ You cannot use this command.", ephemeral=True
        )
        return
    if domain in DOMAINS:
        DOMAINS.remove(domain)
        checked_domains.discard(domain)
        save_domains()
        await interaction.response.send_message(
            f"✅ Domain **{domain}** removed.", ephemeral=True
        )
    else:
        await interaction.response.send_message(
            f"⚠️ Domain **{domain}** not found.", ephemeral=True
        )


# --- 3️⃣ Slash command: list domains ---
@client.tree.command(name="list", description="List all domains being watched")
async def list_domains(interaction: discord.Interaction):
    if interaction.user.id != USER_ID:
        await interaction.response.send_message(
            "❌ You cannot use this command.", ephemeral=True
        )
        return
    if DOMAINS:
        await interaction.response.send_message(
            "📋 Current domains:\n" + "\n".join(DOMAINS), ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "📋 No domains in the list.", ephemeral=True
        )


# --- 4️⃣ Slash command: check all domains immediately ---
@client.tree.command(name="checknow", description="Check all domains immediately")
async def check_now(interaction: discord.Interaction):
    if interaction.user.id != USER_ID:
        await interaction.response.send_message(
            "❌ You cannot use this command.", ephemeral=True
        )
        return
    await interaction.response.send_message(
        "⏳ Checking all domains now...", ephemeral=True
    )
    await check_all_domains()
    await interaction.followup.send("✅ Check completed!", ephemeral=True)


# --- 5️⃣ Slash command: check a specific domain ---
@client.tree.command(
    name="checkdomain", description="Check a specific domain without adding it"
)
@app_commands.describe(domain="Domain to check")
async def check_domain(interaction: discord.Interaction, domain: str):
    if interaction.user.id != USER_ID:
        await interaction.response.send_message(
            "❌ You cannot use this command.", ephemeral=True
        )
        return

    await interaction.response.send_message(
        f"⏳ Checking domain **{domain}**...", ephemeral=True
    )
    available = is_domain_available(domain)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    if available:
        try:
            user = await client.fetch_user(USER_ID)
            await user.send(f"✅ Domain **{domain}** is available! ({timestamp})")
            print(f"[{timestamp}] ✅ DM sent for {domain} (one-time check)")
        except Exception as e:
            print(f"[{timestamp}] ❌ Failed to send DM for {domain}: {e}")
        await interaction.followup.send(
            f"✅ Domain **{domain}** is available! ({timestamp})", ephemeral=True
        )
    else:
        await interaction.followup.send(
            f"⚠️ Domain **{domain}** is still taken ({timestamp})", ephemeral=True
        )
        print(f"[{timestamp}] ⚠️ {domain} is still taken (one-time check)")


# --- Bot ready event ---
@client.event
async def on_ready():
    # Global sync so commands appear everywhere including DMs
    await client.tree.sync()
    print(f"🤖 Bot logged in as {client.user}")
    check_domains.start()


# --- Run the bot ---
client.run(TOKEN)

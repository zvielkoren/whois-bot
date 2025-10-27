# whois-bot

A lightweight Discord bot that brings WHOIS lookups straight into your server.

---

## 🚀 Features
- Perform WHOIS queries directly from Discord – no need to leave your server.
- Fetch domain registration details including creation date, expiration date, registrar, and more.
- Quick and simple to deploy – built in Python for easy usage and customization.

---

## 🧰 Getting Started

### Requirements
- Python 3.7+
- A Discord bot token (see [Discord Developer Portal](https://discord.com/developers/applications))
- Optional: access to a WHOIS service if you choose to extend functionality

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/zvielkoren/whois-bot.git
   cd whois-bot
````

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Configure your environment. Create a `.env` (or use whichever method you prefer) and set:

   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   USER_ID=your_user_id_here
DOMAINS=eduil.org
   ```
4. Run the bot:

   ```bash
   python app.py
   ```
5. Invite the bot to your Discord server using the OAuth link with correct permissions.

---

## 📋 Usage

Once the bot is running in your server, simply use a command like:

```
!whois example.com
```

The bot will respond with relevant WHOIS information for the specified domain.

---

## 🛠️ Customization

* Change command prefix or add aliases in the code.
* Extend functionality to include user lookups, IP WHOIS, or other APIs.
* Adjust output format or styling to fit your server’s voice.

---

## ✅ Why use this bot?

* Keeps everything inside Discord – no separate tool needed.
* Minimal setup, minimal footprint.
* Open-source and MIT-licensed (see LICENSE) – you’re free to modify and reuse.

---

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

Created by **Zviel** — feel free to open issues, send pull requests or suggest features.

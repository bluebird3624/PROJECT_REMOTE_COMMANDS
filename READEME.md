# 🌟 Remote Command Execution Server

Welcome to the **Remote Command Execution Server**! This vibrant Python-based Flask application empowers you to control your PC remotely via a Telegram bot. Using the Telegram Bot API and a public URL from ngrok, you can execute shell commands, send files from your PC to Telegram, and download files sent through Telegram—all with a touch of flair! 🎉

---

## 📑 Table of Contents

- [✨ Features](#-features)
- [🛠️ Prerequisites](#-prerequisites)
- [🚀 Setup Instructions](#-setup-instructions)
    - [Step 1: Install Dependencies](#-step-1-install-dependencies)
    - [Step 2: Create a Telegram Bot](#-step-2-create-a-telegram-bot)
    - [Step 3: Set Up ngrok](#-step-3-set-up-ngrok)
    - [Step 4: Configure the Code](#-step-4-configure-the-code)
    - [Step 5: Run the Server](#-step-5-run-the-server)
    - [Step 6: Set Up the Webhook](#-step-6-set-up-the-webhook)
- [🎮 Usage](#-usage)
    - [Sending Commands](#-sending-commands)
    - [Sending Files to Telegram](#-sending-files-to-telegram)
    - [Receiving Files from Telegram](#-receiving-files-from-telegram)
- [🔒 Security Considerations](#-security-considerations)
- [📂 Project Structure](#-project-structure)
- [🛠️ Troubleshooting](#-troubleshooting)
- [⚠️ Limitations](#-limitations)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

---

## ✨ Features

- **Remote Command Execution** 🚀: Run shell commands on your PC by sending messages through Telegram.
- **File Transfer** 📁:
    - **Upload**: Send files from your PC to Telegram with the `/sendfile` command.
    - **Download**: Save files (documents, photos, videos, audio, voice messages, or stickers) from Telegram to your PC.
- **Security First** 🔐: Blocks risky commands like `shutdown`, `powershell`, `date`, and `time` to keep your system safe.
- **Webhook Magic** 🌐: Uses a Flask server to handle Telegram messages via a webhook endpoint.
- **ngrok Power** 🌍: Exposes your local server to the internet with a public URL.
- **Error Feedback** 📢: Get clear, colorful responses for command or file transfer errors in Telegram.

---

## 🛠️ Prerequisites

To get started, ensure you have:

- **Python 3.6+** 🐍: Installed on your PC.
- **ngrok** 🌐: For creating a public URL.
- **Telegram Account** 💬: To create and interact with your bot.
- **Python Libraries** 📚:
    - `Flask`: Web framework for HTTP requests.
    - `requests`: For Telegram API communication.
    - Standard libraries: `subprocess`, `os`, `pathlib`, `mimetypes`.
- **File Storage Directory** 📂: Default is `C:\PROJECT_REMOTE_COMMANDS\files`.

---

## 🚀 Setup Instructions

### Step 1: Install Dependencies

1. Install **Python 3.6+** from [python.org](https://www.python.org/downloads/).
2. Install required Python packages:
    
    ```bash
    pip install flask requests
    ```
    
3. Install **ngrok**:
    - Download from [ngrok.com](https://ngrok.com/download).
    - Follow OS-specific setup instructions.
    - Authenticate with your ngrok account token (sign up to get one).

### Step 2: Create a Telegram Bot

1. Open Telegram and chat with `@BotFather`.
2. Send `/newbot` and follow prompts to name your bot.
3. Copy the **Bot Token** (e.g., `0000000000:AAHHhhhhhh-ooooU4H7POYHulKD_oooobpU`).
4. Store the token securely.

### Step 3: Set Up ngrok

1. Run ngrok to expose your local server (port 5000):
    
    ```bash
    ngrok http 5000
    ```
    
2. Note the public URL (e.g., `https://abc123.ngrok.io`) for the webhook.

### Step 4: Configure the Code

1. Clone or download the project code.
2. Open `server.py` in a text editor.
3. Update the `TELEGRAM_BOT_TOKEN`:
    
    ```python
    TELEGRAM_BOT_TOKEN = 'your_bot_token_here'
    ```
    
4. Verify the `SAVE_DIR` path:
    
    ```python
    SAVE_DIR = "C:\\PROJECT_REMOTE_COMMANDS\\files"
    ```
    
    - Create the directory if needed:
        
        ```bash
        mkdir C:\PROJECT_REMOTE_COMMANDS\files
        ```
        
5. Save the file.

### Step 5: Run the Server

1. In the project directory, run:
    
    ```bash
    python server.py
    ```
    
2. The server starts on `http://0.0.0.0:5000`. Test it at `http://localhost:5000/hello` to see:
    
    ```json
    {
        "status": "ok",
        "message": "Hello, this is the remote command execution server!"
    }
    ```
    

### Step 6: Set Up the Webhook

1. Set the Telegram webhook using your ngrok URL:
    
    ```bash
    curl -F "url=your_ngrok_url/webhook" https://api.telegram.org/bot<your_bot_token>/setWebhook
    ```
    
    Example:
    
    ```bash
    curl -F "url=https://abc123.ngrok.io/webhook" https://api.telegram.org/bot0000000000:AAHHhhhhhh-ooooU4H7POYHulKD_oooobpU/setWebhook
    ```
    
2. Confirm the webhook:
    
    ```json
    {"ok":true,"result":true,"description":"Webhook was set"}
    ```
    

---

## 🎮 Usage

### Sending Commands

1. Start a chat with your bot.
2. Send a shell command (e.g., `dir` on Windows, `ls` on Linux).
3. Get the output in Telegram!
    - Example:
        - Send: `dir`
        - Response: List of files in the current directory.

### Sending Files to Telegram

1. Use the `/sendfile` command with a file path:
    
    ```bash
    /sendfile C:\PROJECT_REMOTE_COMMANDS\files\example.txt
    ```
    
2. The server checks file validity and size (<50MB).
3. The file appears in your Telegram chat.

### Receiving Files from Telegram

1. Send a file (document, photo, video, audio, voice, or sticker) to the bot.
2. The file saves to `C:\PROJECT_REMOTE_COMMANDS\files`.
3. Receive a confirmation: `File saved successfully: example.txt`.

---

## 🔒 Security Considerations

- **Command Restrictions** 🚫: Blocks dangerous commands (`shutdown`, `powershell`, etc.). Add more in `run_command` if needed.
- **Bot Token Safety** 🔑: Never share or commit your bot token publicly.
- **ngrok Exposure** 🌍: Limit bot access to trusted users, as ngrok makes your server public.
- **File Size Limit** 📏: Enforces Telegram’s 50MB limit for uploads.
- **Directory Permissions** 🔐: Ensure `SAVE_DIR` is secure to prevent unauthorized access.

---

## 📂 Project Structure

```plaintext
project_root/
│
├── server.py              # 🎯 Main Flask server script
├── C:\PROJECT_REMOTE_COMMANDS\files\  # 📂 File storage directory
└── README.md              # 📜 This colorful documentation
```

---

## 🛠️ Troubleshooting

- **Webhook Issues**:
    - Verify ngrok URL and server status.
    - Check webhook setup:
        
        ```bash
        curl https://api.telegram.org/bot<your_bot_token>/getWebhookInfo
        ```
        
    - Review server logs for errors.
- **File Transfer Problems**:
    - Ensure `SAVE_DIR` exists and is writable.
    - Confirm file size is <50MB.
    - Validate file paths in `/sendfile`.
- **Command Errors**:
    - Use safe, OS-compatible commands.
    - Check server console for details.
- **ngrok Problems**:
    - Restart ngrok and update webhook if the URL changes.
    - Ensure your ngrok account is active.

---

## ⚠️ Limitations

- **File Size** 📉: Telegram limits uploads to 50MB.
- **Command Restrictions** 🚫: Some commands are blocked for safety.
- **ngrok Free Tier** 🌐: Temporary URLs require webhook updates on change.
- **Single Chat ID** 💬: Dynamic `CHAT_ID` supports one user; add validation for multi-user setups.

---

## 🤝 Contributing

We’d love your contributions! 🌟

1. Fork the repository.
2. Create a branch: `git checkout -b feature/your-cool-feature`.
3. Commit changes: `git commit -m "Add cool feature"`.
4. Push: `git push origin feature/your-cool-feature`.
5. Open a pull request.

Follow PEP 8 and include clear documentation.

---

## 📜 License

Licensed under the MIT License. See the [LICENSE](https://grok.com/chat/LICENSE) file for details.

👤 Author
Roy Kipchumba
GitHub: @bluebird3624
Email: koechroy06@gmail.com
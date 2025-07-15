import mimetypes
import os
from pathlib import Path
from flask import Flask, request, jsonify
import subprocess
import requests
os.environ['PYTHONUNBUFFERED'] = '1'
TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token_here'
CHAT_ID = ''

app = Flask(__name__)
SAVE_DIR = "C:\\PROJECT_REMOTE_COMMANDS\\files"


def run_command(chat_id,command):
    try:
        if(command.startswith("/sendfile")):
            path = Path(command.split(" ")[1].replace("\n", "").replace("\\", "\\\\"))
            if path.exists() and path.is_file():
                ""
            else:
                return f"The file {path} is not valid."
            
            print("sendfile")
            print(command.split(" ")[1].replace(" ", ""))
            return send_file_to_telegram(chat_id,path)

        if(command.startswith("shutdown") or command.lower().startswith("date") or command.lower().startswith("time") or command.lower().startswith("powershell")):
            return "command is not allowed."
    
    
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)
    

def send_telegram_message(chat_id, text,files=None):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': text,
        'files': files,
    }
    response = requests.post(url, data=data)
    return response

def download_file_from_message(chat_id,message):
    if 'document' in message:
        file_id = message['document']['file_id']
        file_name = message['document']['file_name']
        return download_file(file_id, file_name)
    
    elif 'photo' in message:
        file_id = message['photo'][-1]['file_id'] 
        file_name = 'photo.jpg'
        return download_file(file_id, file_name)
    
    elif 'video' in message:
        file_id = message['video']['file_id']
        file_name = 'video.mp4'
        return download_file(file_id, file_name)
    
    elif 'audio' in message:
        file_id = message['audio']['file_id']
        file_name = message['audio']['file_name'] if 'file_name' in message['audio'] else 'audio.mp3'
        return download_file(file_id, file_name)
    
    elif 'voice' in message:
        file_id = message['voice']['file_id']
        file_name = 'voice.ogg'  # Default voice file extension
        return download_file(file_id, file_name)
    
    elif 'sticker' in message:
        file_id = message['sticker']['file_id']
        file_name = 'sticker.webp'  # Default sticker file extension
        return download_file(file_id, file_name)
    elif 'text' in message:
        text = message['text']
        return run_command(chat_id,text)

    return "No supported file found in the message."

def download_file(file_id, file_name):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile?file_id={file_id}'
    print(f"URL: {file_id}")
    response = requests.get(url)
    
    if response.status_code == 200:
        file_path = response.json()['result']['file_path']
        
        file_url = f'https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}'
        file_data = requests.get(file_url)
        
        if file_data.status_code == 200:
            file_path_on_computer = os.path.join(SAVE_DIR, file_name)
            with open(file_path_on_computer, 'wb') as f:
                f.write(file_data.content)
            return f"File saved successfully: {file_name}"
        else:
            return f"Failed to download file: {file_data.status_code}"
    else:
        return f"Failed to get file path: {response.status_code}"



def send_file_to_telegram(chat_id,filepath):
    try:
        if not os.path.exists(filepath):
            return(f"File not found: {filepath}")
            
        file_size = os.path.getsize(filepath)
        if file_size > 50 * 1024 * 1024:  # 50MB in bytes
            return("File too large. Telegram bot limit is 50MB")
            
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        
        with open(filepath, 'rb') as file:
            files = {
                'document': (os.path.basename(filepath), file)
            }
            data = {
                'chat_id': chat_id
            }
            
            # Send POST request
            response = requests.post(url, files=files, data=data)
            
        # Check response
        if response.status_code == 200 and response.json().get('ok'):
            return(f"File sent successfully: {filepath}")
            
        else:
            return(f"Failed to send file. Status: {response.status_code}, Response: {response.text}")
            
            
    except Exception as e:
        print(f"Error sending file: {str(e)}")
        return False


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print("Received data:", data)
        message = data['message']
        chat_id = data['message']['chat']['id']
        CHAT_ID = chat_id

        print("Received message:", message)
        print("Chat ID:", CHAT_ID)

        command_result = download_file_from_message(CHAT_ID,message)

        send_telegram_message(CHAT_ID, command_result)

        return jsonify({'status': 'ok'}), 200

    except Exception as e:
        print(f"Error: {e.args}")
        return jsonify({'error': str(e)}), 500

@app.route('/hello', methods=['GET']) 
def hello():
    return jsonify({
        'status': 'ok',
        'message': 'Hello, this is the remote command execution server!'
        }), 200


if __name__ == '__main__':
    # Start the Flask server on port 5000
    app.run(host='0.0.0.0', port=5000)

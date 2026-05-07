from flask import Flask, jsonify
import threading
import os
import time
from datetime import datetime

from app import bot, TOKEN, ADMIN_IDS, bot_active, PREMIUM_EMOJIS, all_users

app = Flask(__name__)

bot_start_time = datetime.now()

def run_bot():
    try:
        print("🤖 Bot is running...")
        bot.infinity_polling(timeout=30, long_polling_timeout=15)
    except Exception as e:
        print(f"❌ Bot error: {e}")

def get_bot_info():
    try:
        bot_info = bot.get_me()
        return {
            "username": bot_info.username,
            "first_name": bot_info.first_name,
            "id": bot_info.id
        }
    except:
        return {
            "username": "Unknown",
            "first_name": "Premium Emoji Bot",
            "id": "N/A"
        }

@app.route('/')
def home():
    bot_info = get_bot_info()
    current_time = datetime.now()
    uptime = current_time - bot_start_time
    
    return jsonify({
        "bot_name": bot_info['first_name'],
        "bot_username": f"@{bot_info['username']}",
        "bot_id": bot_info['id'],
        "status": "online" if bot_active else "offline",
        "total_users": len(all_users),
        "emoji_pool": len(PREMIUM_EMOJIS),
        "admins": ADMIN_IDS,
        "started_at": bot_start_time.strftime('%Y-%m-%d %H:%M:%S'),
        "uptime": {
            "days": uptime.days,
            "hours": uptime.seconds // 3600,
            "minutes": (uptime.seconds // 60) % 60,
            "seconds": uptime.seconds % 60
        },
        "message": "Bot is running successfully!"
    })

@app.route('/status')
def status():
    return jsonify({
        "bot": "running",
        "port": 8080,
        "active": bot_active
    })

@app.route('/ping')
def ping():
    return "pong"

if __name__ == "__main__":
    thread = threading.Thread(target=run_bot, daemon=True)
    thread.start()
    print(f"✅ Bot Started at {bot_start_time}")
    print(f"👥 Admins: {ADMIN_IDS}")
    print(f"📊 Total Emojis: {len(PREMIUM_EMOJIS)}")
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
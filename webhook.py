from flask import Flask, request
from telegram import Bot
import datetime
from config import BOT_TOKEN, GROUP_ID
from database import mark_paid

app = Flask(__name__)
bot = Bot(BOT_TOKEN)

@app.route("/callback", methods=["POST"])
def callback():
    data = request.json

    if data["status"] == "PAID":
        invoice = data["merchant_ref"]
        user_id = int(data["customer_name"])

        mark_paid(invoice)

        invite = bot.create_chat_invite_link(
            chat_id=GROUP_ID,
            member_limit=1,
            expire_date=datetime.datetime.now() + datetime.timedelta(minutes=15)
        )

        bot.send_message(
            chat_id=user_id,
            text=(
                "✅ Pembayaran berhasil!\n\n"
                "🔗 Link akses (1x pakai):\n"
                f"{invite.invite_link}\n\n"
                "⚠️ Jangan dibagikan."
            )
        )

    return "OK"

import json
from flask import Flask, request
from telegram import Bot
from config import BOT_TOKEN, GROUP_ID

app = Flask(__name__)
bot = Bot(BOT_TOKEN)

@app.route("/callback", methods=["POST"])
def callback():
    data = request.json
    note = data.get("note")
    status = data.get("status")

    if status == "PAID":
        order_id = note.replace("order_", "")

        with open("orders.json", "r") as f:
            orders = json.load(f)

        user_id = orders[order_id]["user_id"]
        orders[order_id]["status"] = "paid"

        with open("orders.json", "w") as f:
            json.dump(orders, f, indent=2)

        invite = bot.create_chat_invite_link(
            chat_id=GROUP_ID,
            member_limit=1
        )

        bot.send_message(
            chat_id=user_id,
            text=f"✅ Pembayaran berhasil!\n\nLink grup (1x pakai):\n{invite.invite_link}"
        )

    return "OK"

app.run(host="0.0.0.0", port=5000)

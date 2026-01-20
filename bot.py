import json
import uuid
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, QRIS_API_KEY, QRIS_API_SECRET, QRIS_CREATE_URL

ORDER_FILE = "orders.json"
PRICE = 10000

def load_orders():
    try:
        with open(ORDER_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_orders(data):
    with open(ORDER_FILE, "w") as f:
        json.dump(data, f, indent=2)

def create_order(user_id):
    orders = load_orders()
    order_id = str(uuid.uuid4())

    orders[order_id] = {
        "user_id": user_id,
        "status": "pending"
    }

    save_orders(orders)
    return order_id

def create_qris(order_id):
    payload = {
        "api_key": QRIS_API_KEY,
        "api_secret": QRIS_API_SECRET,
        "amount": PRICE,
        "note": f"order_{order_id}"
    }

    r = requests.post(QRIS_CREATE_URL, json=payload)
    return r.json()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🛒 Beli Akses", callback_data="buy")]]
    await update.message.reply_text(
        "👋 Selamat datang\n\nKlik tombol di bawah untuk beli akses grup.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy":
        order_id = create_order(query.from_user.id)
        qris = create_qris(order_id)

        qr_image = qris["data"]["qr_image"]

        await query.message.reply_photo(
            photo=qr_image,
            caption=(
                "🧾 ORDER DIBUAT\n\n"
                f"Order ID:\n{order_id}\n\n"
                f"💰 Harga: Rp{PRICE}\n\n"
                "Silakan scan QRIS untuk membayar."
            )
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()


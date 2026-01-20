import json
import uuid
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN

ORDER_FILE = "orders.json"

# ===== UTIL ORDER =====
def load_orders():
    with open(ORDER_FILE, "r") as f:
        return json.load(f)

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

# ===== HANDLER =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 Beli Akses", callback_data="buy")]
    ]
    await update.message.reply_text(
        "👋 Selamat datang\n\n"
        "Bot ini menjual akses grup private.\n"
        "Klik tombol di bawah untuk membeli.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy":
        order_id = create_order(query.from_user.id)

        await query.edit_message_text(
            "🧾 ORDER DIBUAT\n\n"
            f"Order ID:\n{order_id}\n\n"
            "💰 Harga: Rp10.000\n\n"
            "Silakan lanjut ke pembayaran.\n"
            "(QRIS akan ditambahkan di step berikutnya)"
        )

# ===== MAIN =====
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from payment import create_qris
from config import BOT_TOKEN, PRICE

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 Beli Akses", callback_data="buy")]
    ]
    await update.message.reply_text(
        "👋 Selamat datang\n\n"
        "Akses Group Private\n"
        f"Harga: Rp {PRICE:,}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "buy":
        qr = create_qris(q.from_user.id)
        await q.message.reply_photo(
            photo=qr,
            caption=(
                f"💳 Silakan bayar\n"
                f"Jumlah: Rp {PRICE:,}\n\n"
                "Setelah pembayaran berhasil,\n"
                "link akses akan dikirim otomatis."
            )
        )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()

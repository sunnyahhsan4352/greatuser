from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import asyncio
import schedule
import time
from datetime import datetime

# Store user activity time
user_last_active = {}

# Your Bot Token from BotFather
BOT_TOKEN = "your_bot_token_here"

# /start command to greet users
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_last_active[user_id] = datetime.now()
    await update.message.reply_text(
        "👋 Hello! I'm your trading assistant bot.

I send trading signals and educational content. "
        "If you don't respond, I'll remind you in a while. Feel free to ask me anything about trading!"
    )
    asyncio.create_task(send_reminder(update, context, delay=120))

# Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_last_active[user_id] = datetime.now()
    await update.message.reply_text("Thanks for your message! I'll send you signals soon. 😊")

# Auto reminder if user inactive
async def send_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE, delay=120):
    await asyncio.sleep(delay)
    user_id = update.effective_user.id
    last_time = user_last_active.get(user_id)

    if last_time and (datetime.now() - last_time).total_seconds() >= delay:
        await context.bot.send_message(chat_id=user_id, text="You haven't said anything for a while! 😊 Type something to keep the chat going!")

# Send trading signals at scheduled times (example)
def send_trading_signals():
    # You can change this to fetch real trading signals or make it dynamic
    signals = "🚨 Trading Signal: Buy BTC/USDT now!"
    for user_id in user_last_active.keys():
        context.bot.send_message(chat_id=user_id, text=signals)

# Schedule trading signals (example: every 15 minutes)
schedule.every(15).minutes.do(send_trading_signals)

# Main function to run the bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Run the scheduler in the background
    while True:
        schedule.run_pending()
        time.sleep(1)

    app.run_polling()

if __name__ == "__main__":
    main()

import asyncio
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes,
)

BOT_TOKEN = "8573050885:AAGlXsy6sg3pqbA5gQYUUQ4bbrfaWqkQlqw"

TEAM_USERNAMES = {
    "riviera188", "riviera160", "riviera711",
    "riviera680", "riviera170", "axmad4",
    "riviera210", "riviera105", "rivieratech",
}

WAIT_MINUTES = 10

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

active_jobs = {}

async def tag_team(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data["chat_id"]
    if chat_id not in active_jobs:
        return
    active_jobs.pop(chat_id, None)
    tags = "@Riviera188 @Riviera160 @Riviera711 @Riviera680 @Riviera170 @axmad4 @Riviera210 @Riviera105 @rivieraTech"
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"Hurmatli mijoz, tez orada hodimlarimiz sizga javob berishadi. Kutganingiz uchun rahmat!\n\n@Riviera210 @Riviera160 @Riviera680 @Riviera170 @Riviera711",
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.effective_user:
        return
    if update.effective_user.is_bot:
        return
    chat_id = update.effective_chat.id
    username = (update.effective_user.username or "").lower()
    if username in TEAM_USERNAMES:
        if chat_id in active_jobs:
            active_jobs[chat_id].schedule_removal()
            active_jobs.pop(chat_id, None)
            logger.info(f"{username} javob berdi, timer bekor qilindi.")
        return
    if chat_id in active_jobs:
        return
    logger.info(f"Mijoz yozdi, {WAIT_MINUTES} daqiqa timer boshlandi.")
    job = context.job_queue.run_once(
        tag_team,
        when=WAIT_MINUTES * 60,
        data={"chat_id": chat_id},
    )
    active_jobs[chat_id] = job

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Bot ishga tushdi!")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())

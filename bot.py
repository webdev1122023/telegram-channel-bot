import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ChatMemberHandler,
    ContextTypes,
)

BOT_TOKEN = "8603095714:AAH2qTQFGz6YW1GhobPchdkOPuZU8aEw1KY"
CHANNEL_ID = -1002058703755
PREVIEW_SECONDS = 120
JOIN_LINK = "https://web.telegram.org/k/#@ghanaleaksnews"

logging.basicConfig(level=logging.INFO)

verified_users = set()

async def kick_after_preview(user_id, username, context):
    await asyncio.sleep(PREVIEW_SECONDS)

    if user_id in verified_users:
        return

    try:
        await context.bot.ban_chat_member(CHANNEL_ID, user_id)
        await asyncio.sleep(2)
        await context.bot.unban_chat_member(CHANNEL_ID, user_id)

        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "Your FREE preview has ended.\n\n"
                "To keep reading and access all files, click the button below"
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Join Full Channel", url=JOIN_LINK)]
            ])
        )
        print(f"Kicked user: {username} ({user_id})")

    except Exception as e:
        print(f"Could not kick {user_id}: {e}")


async def on_member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member
    if result is None:
        return

    new_status = result.new_chat_member.status
    user = result.new_chat_member.user

    if new_status == "member":
        print(f"New member joined: {user.username} ({user.id})")
        asyncio.create_task(kick_after_preview(user.id, user.username, context))


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(ChatMemberHandler(on_member_update, ChatMemberHandler.CHAT_MEMBER))
    print("Bot is running...")
    app.run_polling(allowed_updates=["chat_member"])

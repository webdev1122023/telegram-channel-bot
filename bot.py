import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ChatMemberHandler,
    ContextTypes,
)

# ===== YOUR SETTINGS — EDIT THESE =====
BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"
CHANNEL_ID = -1001234567890  # Paste your Channel ID here
PREVIEW_SECONDS = 60  # How many seconds before kick (60 = 1 minute)
JOIN_LINK = "https://t.me/+yourinvitelink"  # Your paid/real join link
# =======================================

logging.basicConfig(level=logging.INFO)

# This stores users who have paid/verified — start empty
verified_users = set()

async def kick_after_preview(user_id, username, context):
    await asyncio.sleep(PREVIEW_SECONDS)

    if user_id in verified_users:
        return  # They verified, don't kick

    try:
        # Kick the user
        await context.bot.ban_chat_member(CHANNEL_ID, user_id)
        # Immediately unban so they CAN come back after joining
        await asyncio.sleep(2)
        await context.bot.unban_chat_member(CHANNEL_ID, user_id)

        # Send them a message
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                f"⏳ Hey! Your FREE preview has ended.\n\n"
                f"To keep reading and access all files, click the button below 👇"
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Join Full Channel", url=JOIN_LINK)]
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
        # Start the countdown to kick
        asyncio.create_task(kick_after_preview(user.id, user.username, context))


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(ChatMemberHandler(on_member_update, ChatMemberHandler.CHAT_MEMBER))
    print("Bot is running...")
    app.run_polling(allowed_updates=["chat_member"])
```

---

**FILE 2 — Create a file called `requirements.txt`**
```
python-telegram-bot==20.7
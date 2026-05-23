from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
    CommandHandler,
)

import google.generativeai as genai
import os
import random
import asyncio

# =========================
# TOKENS
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API = os.getenv("GEMINI_API")

# =========================
# GEMINI SETUP
# =========================

genai.configure(api_key=GEMINI_API)

model = genai.GenerativeModel("gemini-1.5-flash")

# =========================
# MEMORY
# =========================

memory = {}

# =========================
# START COMMAND
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "heyy 😭\nmain VegRoll aa gayi lol"
    )

# =========================
# CHAT FUNCTION
# =========================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    username = update.effective_user.first_name
    text = update.message.text

    if not text:
        return

    # typing effect
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    await asyncio.sleep(random.randint(1, 3))

    # memory
    if user_id not in memory:
        memory[user_id] = []

    memory[user_id].append(text)

    memory[user_id] = memory[user_id][-5:]

    history = "\n".join(memory[user_id])

    prompt = f"""
You are VegRoll, a real human-like Telegram friend.

Rules:
- Talk naturally
- Hindi + English mix
- Cute and funny
- Use emojis sometimes
- Never sound robotic
- Short casual replies
- Gen-Z vibe

User Name: {username}

Recent chat:
{history}

User: {text}
"""

    try:

        response = model.generate_content(prompt)

        reply = response.text.strip()

        await update.message.reply_text(reply)

    except Exception as e:

        await update.message.reply_text(
            "arey 😭 thoda network issue ho gaya"
        )

# =========================
# APP
# =========================

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        chat
    )
)

print("Bot Running...")

app.run_polling()

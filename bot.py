# ================================
# TELEGRAM AI HUMAN-LIKE BOT
# Made for GitHub + Render Hosting
# ================================

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

import google.generativeai as genai
import os
import random
import asyncio

# ================================
# API CONFIG
# ================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API = os.getenv("GEMINI_API")

genai.configure(api_key=GEMINI_API)

model = genai.GenerativeModel("gemini-1.5-flash")

# ================================
# MEMORY SYSTEM
# ================================

user_memory = {}

# ================================
# HUMAN REPLY STYLES
# ================================

human_reactions = [
    "hmm 😭",
    "arey 😭",
    "acha 😭",
    "lol 😭",
    "sach me? 👀",
    "damnn 😭",
    "brooo 😭",
]

# ================================
# MAIN CHAT FUNCTION
# ================================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    user_text = update.message.text

    # Ignore empty text
    if not user_text:
        return

    # Save short memory
    if user_id not in user_memory:
        user_memory[user_id] = []

    user_memory[user_id].append(user_text)

    # Keep only last 5 msgs
    user_memory[user_id] = user_memory[user_id][-5:]

    memory_text = "\n".join(user_memory[user_id])

    # Fake typing
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    await asyncio.sleep(random.randint(1, 3))

    # Personality Prompt
    prompt = f"""
You are a real human friend chatting on Telegram.

Rules:
- Never sound like AI
- Talk naturally
- Use Hindi + English mix
- Sometimes use emojis
- Keep replies short
- Be emotional and funny
- Sometimes tease lightly
- Don't write long paragraphs
- Talk casually like Gen-Z

User name: {user_name}

Recent messages:
{memory_text}

User: {user_text}
"""

    try:
        response = model.generate_content(prompt)

        reply = response.text.strip()

        # Random extra human reaction
        if random.random() < 0.3:
            reply += "\n\n" + random.choice(human_reactions)

        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(
            "arey 😭 thoda network issue ho gaya"
        )

# ================================
# START COMMAND
# ================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "heyy 😭\nmain aa gayi lol"
    )

# ================================
# BOT START
# ================================

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("Bot Running...")

app.run_polling()

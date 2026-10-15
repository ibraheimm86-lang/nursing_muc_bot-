
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("First Year", callback_data="year1")],
        [InlineKeyboardButton("Second Year", callback_data="year2")],
        [InlineKeyboardButton("Third Year", callback_data="year3")],
        [InlineKeyboardButton("Fourth Year", callback_data="year4")],
    ]
    await update.message.reply_text(
        "Welcome to Nursing MUC!\nChoose your year:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("year"):
        keyboard = [
            [InlineKeyboardButton("Adult Checklist", callback_data="adult")],
            [InlineKeyboardButton("Back to Main Menu", callback_data="home")],
        ]
        await query.edit_message_text(
            "Choose a subject:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "home":
        await start_from_button(query)

    elif query.data == "adult":
        pdf_path = "adult 1 checklist.pdf"
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as pdf:
                await context.bot.send_document(
                    chat_id=query.message.chat_id,
                    document=pdf,
                    filename="adult 1 checklist.pdf",
                )
        else:
            await query.message.reply_text(
                "The PDF has not been uploaded yet."
            )

async def start_from_button(query):
    keyboard = [
        [InlineKeyboardButton("First Year", callback_data="year1")],
        [InlineKeyboardButton("Second Year", callback_data="year2")],
        [InlineKeyboardButton("Third Year", callback_data="year3")],
        [InlineKeyboardButton("Fourth Year", callback_data="year4")],
    ]
    await query.edit_message_text(
        "Welcome to Nursing MUC!\nChoose your year:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

def main():
    token = os.environ["BOT_TOKEN"]
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.run_polling()

if __name__ == "__main__":
    main()

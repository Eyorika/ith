from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Replace with your bot token
BOT_TOKEN = ""

# Define career options
CAREER_OPTIONS = [
    "Software Developer", 
    "Designer", 
    "HR"
]

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles /start command."""
    # Ask for contact sharing
    keyboard = [[KeyboardButton("Share Contact", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Welcome! Please share your contact to proceed:", reply_markup=reply_markup)

# Handle contact sharing
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles contact sharing."""
    contact = update.message.contact
    user_phone = contact.phone_number
    context.user_data["phone"] = user_phone

    # Respond and show the career form
    await update.message.reply_text(
        f"Thank you! Now, please provide your basic information.\n"
        f"What's your full name?"
    )

# Handle text input (e.g., Full Name, Address)
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles user text inputs for the form."""
    user_input = update.message.text

    # Keep track of form progress
    if "full_name" not in context.user_data:
        context.user_data["full_name"] = user_input
        await update.message.reply_text("Got it! What's your address?")
    elif "address" not in context.user_data:
        context.user_data["address"] = user_input
        # Show career options after gathering address
        keyboard = [[KeyboardButton(option)] for option in CAREER_OPTIONS]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(
            "Almost done! Please choose your desired career path:",
            reply_markup=reply_markup
        )
    else:
        # If unexpected input occurs
        await update.message.reply_text("Please select your career from the buttons provided.")

# Handle career selection
async def career_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles career selection."""
    career = update.message.text
    if career in CAREER_OPTIONS:
        context.user_data["career"] = career

        # Confirm successful submission
        await update.message.reply_text(
            f"Thank you for completing the form!\n"
            f"Name: {context.user_data.get('full_name')}\n"
            f"Phone: {context.user_data.get('phone')}\n"
            f"Address: {context.user_data.get('address')}\n"
            f"Career: {context.user_data.get('career')}\n\n"
            f"We will contact you soon!"
        )
    else:
        await update.message.reply_text("Invalid career choice. Please select from the provided options.")

# Main function to set up the bot
def main():
    """Run the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()

import requests
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

from flask import Flask, render_template

# Initialize Flask app
app = Flask(__name__, static_folder='flask_app/static', template_folder='flask_app/templates')

@app.route('/')
def index():
    return render_template('index.html')

# Function to run the Flask app
def run_flask():
    app.run(host='0.0.0.0', port=4000)

if __name__ == '__main__':
    run_flask()

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# API keys
TELEGRAM_TOKEN = '7457208907:AAExyWaeB4im3x5tIdtr9DJo0ky8Bk2l8tY'
REMOVE_BG_API_KEY = 'TVBNSUTotenezqSwweeyjQiR'

# /start command handler
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Welcome to the Background Remover Bot! Send me an image, and I'll remove its background for you. "
        "Here's what I can do:\n"
        "- Send any image to remove its background.\n"
        "- Use the /help command for assistance."
    )

# /help command handler
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "To use this bot:\n"
        "1. Send an image.\n"
        "2. The bot will remove the background and send the image back to you."
    )

# Background removal function
def remove_background(image_path: str) -> str:
    url = 'https://api.remove.bg/v1.0/removebg'
    files = {'image_file': open(image_path, 'rb')}
    data = {'size': 'auto'}
    headers = {'X-Api-Key': REMOVE_BG_API_KEY}

    response = requests.post(url, files=files, data=data, headers=headers)
    
    if response.status_code == 200:
        # Save the result to a file and return the file path
        output_image_path = 'no_bg_image.png'
        with open(output_image_path, 'wb') as out_file:
            out_file.write(response.content)
        return output_image_path
    else:
        logger.error(f"Error: {response.status_code}, {response.text}")
        return None

# Handler for images
async def handle_image(update: Update, context: CallbackContext) -> None:
    photo_file = await update.message.photo[-1].get_file()
    image_path = 'user_image.png'
    await photo_file.download_to_drive(image_path)
    
    await update.message.reply_text("Removing background... Please wait.")
    
    # Remove background
    no_bg_image = remove_background(image_path)
    
    if no_bg_image:
        # Send the image as a document with a .png extension
        await update.message.reply_document(document=open(no_bg_image, 'rb'), filename="no_bg_image.png")
    else:
        await update.message.reply_text("Failed to remove background. Please try again later.")

# Error handler
async def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f"Update {update} caused error {context.error}")

def main() -> None:
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register the command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Register the image handler
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))

    # Log all errors
    application.add_error_handler(error)

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()

from flask import Flask
import os

app = Flask(__name__)

# Define a simple route for testing
@app.route('/')
def home():
    return "This is a web service running on Render!"

if __name__ == "__main__":
    # Render assigns a PORT environment variable for web services
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port)
    

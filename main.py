import io
import logging
from PIL import Image, UnidentifiedImageError
from pyrogram import Client, filters
from pyrogram import enums
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Bot API Token, API ID, and API Hash
API_TOKEN = "6365859811:AAGK5hlLKtLf-RqlaEXngZTWnfSPISerWPI"
API_ID = "10471716"
API_HASH = "f8a1b21a13af154596e2ff5bed164860"


# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/stablediffusionapi/duchaiten-real3d-nsfw-xl"
HEADERS = {"Authorization": "Bearer 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"}

# Pyrogram Client
app = Client(
    "my_bot",
    bot_token=API_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)


# /start command handler
@app.on_message(filters.command("start"))
def start_command(client, message):
    message.reply_text("Welcome! Send me a message, and I'll generate an image based on the input.")


# /help command handler
@app.on_message(filters.command("help"))
def help_command(client, message):
    message.reply_text(
        "Send me a message, and I'll generate an image based on the input. "
        "Make sure to keep your input concise for better results."
    )


# Message handler
@app.on_message(filters.text)
def process_message(client, message):
    try:
        input_text = message.text.strip()
        if not input_text:
            message.reply_text("Please provide a non-empty message.")
            return

        # Query Hugging Face API with the user's input
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": input_text})
        image_bytes = response.content

        # Attempt to open the image with PIL
        image = Image.open(io.BytesIO(image_bytes))

        # Save the image to the current working directory
        # Save the image with the name provided by the user and extension as png
        filename = f"{input_text[:20].replace(' ', '_')}_generated_image.png"
        image.save(filename)

        # Send the generated image back to the user
        message.reply_photo(
            photo=filename,
            caption=f"Generated image based on your input:\n *{input_text}*  \n [By](https://t.me/botio_devs.com).",
            parse_mode=enums.ParseMode.MARKDOWN
            )
    except UnidentifiedImageError as e:
        logger.error(f"Error opening image: {e}")
        message.reply_text("Error opening the generated image. Please try again.")
    except Exception as e:
        logger.error(f"Error: {e}")
        message.reply_text("An unexpected error occurred. Please try again later.")


if __name__ == "__main__":
    app.run()

import io
import logging
from PIL import Image, UnidentifiedImageError
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
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
    buttons = [
        [
            InlineKeyboardButton("About", callback_data="about"),
            InlineKeyboardButton("Our Bots", callback_data="our_bots"),
        ],
        [InlineKeyboardButton("Join Updates Channel", url="https://t.me/botio_devs")],
    ]

    markup = InlineKeyboardMarkup(buttons)

    message.reply_text("☺︎нαι\n✦ Sᴇɴᴅ Mᴇ A Pʀᴏᴍᴘᴛ Tᴏ Gᴇɴᴇʀᴀᴛᴇ Iᴍᴀɢᴇs ᴡɪᴛʜ Iᴛ......🔥\n\n╭──────── ⋅ ⋅ ────── 𝐈𝐍𝐓𝐑𝐎 ────── ⋅ ⋅ ─────────╮\n          𝙸𝚊𝚖 𝙰 𝙰𝚍𝚟𝚊𝚗𝚌𝚎𝚍 𝙸𝚖𝚊𝚐𝚎 𝙶𝚎𝚗𝚎𝚛𝚊𝚝𝚘𝚛 𝙱𝚘𝚝\n     𝙼𝚢 𝙱𝚘𝚜𝚜 𝙸𝚜 𝙳𝚊𝚒𝚕𝚢 𝙵𝚒𝚕𝚕𝚒𝚗𝚐 𝙼𝚎 𝚆𝚒𝚝𝚑 𝚗𝚎𝚠 𝚄𝚙𝚍𝚊𝚝𝚎𝚜\n               𝙳𝚘𝚗𝚝 𝙵𝚘𝚛𝚐𝚎𝚝 𝚝𝚘 𝙹𝚘𝚒𝚗 𝙼𝚢 [𝙵𝚊𝚖𝚒𝚕𝚢](https://t.me/botio_devs)\n╰────────── ⋅ ⋅ ────── ✩ ────── ⋅ ⋅ ──────────╯\n\n[𓆩ⒶⒹⓂⒾⓃ𓆪](@APPUZ_001)", reply_markup=markup)


@app.on_callback_query()
def handle_callback_query(client, query):
    data = query.data

    if data == "about":
        about_text = "<b>All About</b>"
        back_button = InlineKeyboardButton("Back", callback_data="back")
        markup = InlineKeyboardMarkup([[back_button]])
        query.edit_message_text(about_text, reply_markup=markup, parse_mode=None)
    
    elif data == "our_bots":
        bots_text = "<b>Ours bot here</b>"
        back_button = InlineKeyboardButton("Back", callback_data="back")
        markup = InlineKeyboardMarkup([[back_button]])
        query.edit_message_text(bots_text, reply_markup=markup, parse_mode=None)
    
    elif data == "back":
        # Show the initial welcome message with buttons
        buttons = [
        [
            InlineKeyboardButton("About", callback_data="about"),
            InlineKeyboardButton("Our Bots", callback_data="our_bots"),
        ],
        [InlineKeyboardButton("Join Updates Channel", url="https://t.me/botio_devs")],
        ]
        markup = InlineKeyboardMarkup(buttons)
        query.edit_message_text("Welcome! Send me a message, and I'll generate an image based on the input.", reply_markup=markup)


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
            caption=f"🖼️:\n <b>{input_text}</b>  \n <a href='https://t.me/botio_devs'>🤍🄹🄾🄸🄽🤍</a>.",
            parse_mode=enums.ParseMode.HTML
        )
    except UnidentifiedImageError as e:
        logger.error(f"Error opening image: {e}")
        message.reply_text("Error opening the generated image. Please try again.")
    except Exception as e:
        logger.error(f"Error: {e}")
        message.reply_text("An unexpected error occurred. Please try again later.")


if __name__ == "__main__":
    app.run() 

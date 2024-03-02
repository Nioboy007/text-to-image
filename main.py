import requests
import io
from PIL import Image, UnidentifiedImageError  # Import UnidentifiedImageError

API_URL = "https://api-inference.huggingface.co/models/stablediffusionapi/duchaiten-real3d-nsfw-xl"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content, response.url

image_bytes, download_url = query({
    "inputs": "Astronaut riding a horse",
})

try:
    # Attempt to open the image with PIL
    image = Image.open(io.BytesIO(image_bytes))

    # Save the image to the current working directory
    filename = "downloaded_image.png"
    image.save(filename)

except UnidentifiedImageError as e:  # Use UnidentifiedImageError directly
    print(f"Error opening image: {e}")
except Exception as e:
    print(f"Error: {e}")

from flask import Flask, send_from_directory, request, url_for
import os
import time
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

# Directory to save generated images (now under /tmp/assets)
ASSETS_DIR = os.path.join('/tmp', 'assets')
os.makedirs(ASSETS_DIR, exist_ok=True)

start_timestamp = int(time.time())
index = 0

def generate_image(filename, timestamp, idx):
    width = 400
    height = 200
    bg_color = (242, 242, 242)
    text_color = (51, 51, 51)
    out_path = os.path.join(ASSETS_DIR, filename)
    if os.path.exists(out_path):
        return
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    # Try to use a common font, fallback to default if not found
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 30)
    except Exception:
        font = ImageFont.load_default()
    timestamp_text = f"Timestamp: {timestamp}"
    index_text = f"Index: {idx}"
    draw.text((20, 80), timestamp_text, fill=text_color, font=font)
    draw.text((20, 130), index_text, fill=text_color, font=font)
    img.save(out_path, "JPEG", quality=90)

@app.route('/assets/<filename>')
def serve_asset(filename):
    return send_from_directory(ASSETS_DIR, filename)

@app.route('/')
def hello():
    global index
    filename = f"{start_timestamp}_{index}.jpg"
    try:
        generate_image(filename, start_timestamp, index)
    except Exception as e:
        return f"Error generating image: {e}", 500
    image_url = url_for('serve_asset', filename=filename, _external=True)
    html = f"""<html>
    <head>
        <title>Hello World</title>
        <meta property="og:title" content="Hello World" />
        <meta property="og:description" content="A simple Flask server with link preview meta tags." />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="{request.url}" />
        <meta property="og:image" content="{image_url}" />
    </head>
    <body>
        <h1>Hello, World!</h1>
    </body>
    </html>"""
    index += 1
    return html

if __name__ == '__main__':
    app.run(port=6969)

from PIL import Image, ImageDraw, ImageFont
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
FONT_PATH = os.path.join(ASSETS_DIR, "arial.ttf")  # Make sure to add arial.ttf or another font

def generate_wallet_card(address, balance, referral_code):
    width, height = 600, 250
    img = Image.new('RGB', (width, height), color=(30, 30, 60))
    draw = ImageDraw.Draw(img)

    # Background image
    bg_path = os.path.join(ASSETS_DIR, "card_bg.png")
    if os.path.exists(bg_path):
        bg = Image.open(bg_path).resize((width, height))
        img.paste(bg, (0, 0))

    font_large = ImageFont.truetype(FONT_PATH, 28)
    font_small = ImageFont.truetype(FONT_PATH, 20)

    draw.text((30, 30), f"Wallet: {address}", fill=(255, 255, 255), font=font_large)
    draw.text((30, 90), f"Balance: {balance} PANCA", fill=(255, 255, 255), font=font_large)
    draw.text((30, 150), f"Referral: {referral_code}", fill=(255, 255, 255), font=font_small)

    out_path = f"/tmp/{address}.png"
    img.save(out_path)
    return out_path

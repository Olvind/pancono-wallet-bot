from PIL import Image, ImageDraw, ImageFont
import os

def generate_wallet_card(address, balance, referral_code=None):
    """Generates a wallet card image"""
    width, height = 600, 250
    img = Image.new('RGB', (width, height), color=(30, 30, 60))
    draw = ImageDraw.Draw(img)
    
    # Fonts (make sure Arial.ttf or a similar font exists)
    try:
        font_large = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 18)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Gradient background (optional)
    for i in range(height):
        color = (30 + i//10, 30 + i//15, 60 + i//8)
        draw.line([(0, i), (width, i)], fill=color)
    
    draw.text((20, 20), f"💼 Wallet Address:", fill=(255, 255, 255), font=font_small)
    draw.text((20, 50), address, fill=(255, 255, 255), font=font_large)

    draw.text((20, 100), f"💰 Balance:", fill=(255, 255, 255), font=font_small)
    draw.text((20, 130), f"{balance} PANCA", fill=(255, 255, 255), font=font_large)

    if referral_code:
        draw.text((20, 180), f"🎁 Referral Code:", fill=(255, 255, 255), font=font_small)
        draw.text((20, 210), referral_code, fill=(255, 255, 255), font=font_large)

    # Save image temporarily
    path = f"/tmp/wallet_{address[:6]}.png"
    img.save(path)
    return path

import requests
import asyncio
import time
from bs4 import BeautifulSoup
from telegram import Bot

#url for the italian site
url_it = "https://shop.universalmusic.it/search?q=arcane"
#url for the uk site
url_uk = "https://arcaneuk.virginmusic.com/"
#headers
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}

# Telegram bot token and chat ID
bot_token = "7208274219:AAH3gDDsYdPC1grMa-rfZe3gnWQBLbG1LIA"
chat_id = "450009936"
# Initialize the Telegram Bot
bot = Bot(token=bot_token)


# Iterate over each product card and check conditions
def check_stock_it():
    response = requests.get(url_it, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all product cards
    product_cards = soup.select(".product-card")

    for card in product_cards:
        # Get the item description
        item_tag = card.select_one(".album")
        # Get the price/status description
        price_tag = card.select_one(".price")
        # Get the sold out check
        item_sold_out = card.select_one(".product-card__label.out-of-stock")
        
        if item_tag and price_tag:
            item_text = item_tag.text.strip()
            price_text = price_tag.text.strip()
            item_type = card.select_one(".item").text.strip()

            # Check if the item contains "Vinile" and if it's "Esaurito"
            if "Vinile" in item_type:
                if item_sold_out:
                    print(f"Out of stock: {item_text}")
                else:
                    return True
    return False

def check_stock_uk():
    response = requests.get(url_uk, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all product cards
    product_cards = soup.select(".card__container")

    for card in product_cards:
        # Get the item description
        item_tag = card.select_one(".card__title")
        # Get the price/status description
        price_tag = card.select_one(".price__current")
        # Get the sold out check
        item_sold_out = card.select_one(".tag--sold_out")
        
        if item_tag and price_tag:
            item_text = item_tag.text.strip()
            price_text = price_tag.text.strip()

            # Check if the item contains "LP" and if it's "Sold out"
            if "LP" in item_text:
                if item_sold_out:
                    print(f"Out of stock: {item_text}")
                else:
                    return True
    return False

async def run_bot():
    while True:
        if check_stock_it():
            message = f"<b>Vinyl available:</b> {item_text} (Price: {price_text})"
            await bot.send_message(chat_id=chat_id, text=message)
            break  # Stop after sending the message once
        elif check_stock_uk():
            message = f"<b>Vinyl available:</b> {item_text} (Price: {price_text})"
            await bot.send_message(chat_id=chat_id, text=message)
            break  # Stop after sending the message once
        else:
            await bot.send_message(chat_id=chat_id, text="No vinyl in stock. Checking again in 12 hours.")
        await asyncio.sleep(43200)  # Wait for 2 hours before checking again

# Start the bot
asyncio.run(run_bot())
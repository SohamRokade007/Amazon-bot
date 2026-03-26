import requests
import schedule
import time
from serpapi import GoogleSearch

# ===== CONFIG =====

SERPAPI_KEY = "536d5e45c160f3308d7bb8a2dc9b6fdb43377d61606eccdb150d36cf1de0178b"

BOT_TOKEN = "6734676820:AAGrE_NWpZBQjN0_YPVuALj24EajPxMfk-o"

CHANNEL_ID = "@onlineindiaadeals"

AFFILIATE_TAG = "sohamtechdeal-21"


# ===== TELEGRAM FUNCTION =====

def send_to_telegram(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHANNEL_ID,
        "text": message
    }

    r = requests.post(url, data=data)

    print("Telegram:", r.text)


# ===== AMAZON DEAL FETCH =====

def get_deals():

    params = {
        "engine": "amazon",
        "amazon_domain": "amazon.in",
        "k": "gaming laptop",
        "api_key": SERPAPI_KEY
    }

    search = GoogleSearch(params)

    results = search.get_dict()

    items = results.get("organic_results", [])

    deals = []

    for item in items[:5]:

        title = item.get("title")

        price = item.get("extracted_price")

        old_price = item.get("extracted_old_price")

        link = item.get("link_clean")

        if link:
            affiliate_link = f"{link}?tag={AFFILIATE_TAG}"
        else:
            continue

        discount = ""

        if price and old_price:
            discount_percent = round((old_price - price) / old_price * 100)
            discount = f"\n🔥 Discount: {discount_percent}% OFF"

        product = {
            "title": title,
            "price": price,
            "old_price": old_price,
            "discount": discount,
            "link": affiliate_link
        }

        deals.append(product)

    return deals


# ===== POST DEALS =====

def post_deals():

    deals = get_deals()

    print("Deals found:", deals)

    for product in deals:

        message = f"""
🔥 {product['title']}

💰 Price: ₹{product['price']}
❌ MRP: ₹{product['old_price']}{product['discount']}

🛒 Buy Now
{product['link']}

#amazon #deals
"""

        send_to_telegram(message)

        print("Posted:", product["title"])

        time.sleep(5)


# ===== RUN BOT =====

print("Bot running...")

post_deals()

schedule.every(6).hours.do(post_deals)

while True:

    schedule.run_pending()

    time.sleep(5)
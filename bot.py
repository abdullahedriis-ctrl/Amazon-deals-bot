from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from bs4 import BeautifulSoup
import requests
import time

TOKEN = "8382650564:AAFjYVrWRAta9Y3njvwzoEdPkbtPd7mL-yc"
CHANNEL = "@اسم_القناة_بتاعتك"

bot = Bot(token=TOKEN)

# دالة لإرسال الرسائل بشكل جذاب مع زر للمنتج
def send_offer(name, discount, link, image_url):
    message = f"🔥 *{name}*\n💸 *الخصم:* {discount}%"
    button = InlineKeyboardButton(text="رابط المنتج", url=link)
    markup = InlineKeyboardMarkup([[button]])
    bot.send_photo(chat_id=CHANNEL, photo=image_url, caption=message, parse_mode="Markdown", reply_markup=markup)

# --- Noon مصر ---
def scrape_noon(category=None):
    url = "https://www.noon.com/egypt-en/sale/?sort=discount-desc"
    if category:
        url += f"&category={category}"  # لتصفية الأقسام
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("div", {"class": "productCard"})
    for product in products:
        try:
            name = product.find("a", {"class": "name"}).text.strip()
            discount_text = product.find("span", {"class": "discount"}).text.strip().replace("%","")
            discount = int(discount_text)
            link = "https://www.noon.com" + product.find("a")["href"]
            image_url = product.find("img")["src"]
            if discount >= 30:
                send_offer(name, discount, link, image_url)
        except:
            continue

# --- Amazon مصر ---
def scrape_amazon(category=None):
    url = "https://www.amazon.eg/s?bbn=17677297031&rh=p_36%3A-3000"
    if category:
        url += f"&i={category}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("div", {"data-component-type": "s-search-result"})
    for product in products:
        try:
            name = product.h2.text.strip()
            price = product.find("span", {"class": "a-price-whole"})
            original_price = product.find("span", {"class": "a-text-price"})
            if price and original_price:
                price_val = int(price.text.replace(",",""))
                original_val = int(original_price.text.strip().replace("EGP","").replace(",",""))
                discount = int(((original_val - price_val)/original_val)*100)
                if discount >= 30:
                    link = "https://www.amazon.eg" + product.h2.a["href"]
                    image_url = product.find("img")["src"]
                    send_offer(name, discount, link, image_url)
        except:
            continue

# --- تشغيل البوت كل نص ساعة ---
while True:
    scrape_noon()
    scrape_amazon()
    print("تم تحديث العروض. الانتظار 30 دقيقة...")
    time.sleep(1800)  # كل 30 دقيقة
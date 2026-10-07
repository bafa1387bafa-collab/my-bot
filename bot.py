import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import quote
import requests
import telebot

TOKEN = os.environ["BOT_TOKEN"]
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "سلام! توضیح عکس را بفرستید تا بسازم.\nمثلاً: a cat on the moon\n(انگلیسی بهتر جواب می‌دهد)")


@bot.message_handler(func=lambda m: True)
def make_image(message):
    bot.reply_to(message, "در حال ساخت عکس...")
    try:
        url = "https://image.pollinations.ai/prompt/" + quote(message.text)
        r = requests.get(url, timeout=120)
        r.raise_for_status()
        bot.send_photo(message.chat.id, r.content)
    except Exception:
        bot.reply_to(message, "ساخت عکس ناموفق بود. دوباره امتحان کنید.")


class Health(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, *args):
        pass


def run_server():
    port = int(os.environ.get("PORT", 8000))
    HTTPServer(("0.0.0.0", port), Health).serve_forever()


threading.Thread(target=run_server, daemon=True).start()
bot.infinity_polling()

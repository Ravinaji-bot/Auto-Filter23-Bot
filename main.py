import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request

# --- Configuration ---
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# --- Movie Database ---
MOVIES = {
    "pushpa 2": "https://t.me/example/1",
    "maharaja": "https://t.me/example/4",
    "stree 2": "https://t.me/example/5"
}

def send_reply(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"❌ Error sending: {e}")

class SimpleWebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Telegram Messages Handle karne ke liye
        try:
            length = int(self.headers.get('content-length', 0))
            data = self.rfile.read(length)
            update = json.loads(data.decode('utf-8'))

            if "message" in update and "text" in update["message"]:
                chat_id = update["message"]["chat"]["id"]
                user_text = update["message"]["text"].lower()

                if user_text == "/start":
                    send_reply(chat_id, "🙏 **Namaste! Gajab Facts Bot Live Hai!**\nMovie ka naam likhiye.")
                else:
                    found = False
                    for movie, link in MOVIES.items():
                        if movie in user_text:
                            send_reply(chat_id, f"🔍 **Mili:** {movie.title()}\n🔗 [Download Karo]({link})")
                            found = True
                            break
                    if not found:
                        send_reply(chat_id, "❌ Sorry sir, ye movie nahi mili.")
        except Exception as e:
            print(f"Post Error: {e}")
            
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # Leapcell Health Check aur UptimeRobot ke liye
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is Active!")

    def log_message(self, format, *args):
        return # Logs ko faltu requests se bharne se rokne ke liye

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleWebhookHandler)
    print(f"🚀 BOT SERVER STARTED ON PORT {port}")
    server.serve_forever()
                    

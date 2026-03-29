import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request

# --- Config ---
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# --- Movie Data ---
MOVIES = {
    "pushpa 2": "https://t.me/example/1",
    "maharaja": "https://t.me/example/4"
}

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Error sending message: {e}")

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Telegram se aane wale messages handle karega
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        update = json.loads(post_data.decode('utf-8'))

        if "message" in update and "text" in update["message"]:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"]["text"].lower()

            if text == "/start":
                send_message(chat_id, "✅ **Gajab Facts Bot Live Hai!**\nMovie search kijiye.")
            else:
                found = False
                for movie, link in MOVIES.items():
                    if movie in text:
                        send_message(chat_id, f"🔍 **Mili:** {movie.title()}\n🔗 [Link]({link})")
                        found = True
                        break
                if not found:
                    send_message(chat_id, "❌ Sorry, movie nahi mili.")

        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # --- YE UPTIME ROBOT KE LIYE HAI ---
        # Jab UptimeRobot link check karega, ye use 200 OK bhejega
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"I am alive and working!")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), WebhookHandler)
    print(f"🚀 Bot Server started on port {port}")
    server.serve_forever()
    

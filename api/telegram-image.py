import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from urllib.request import Request, urlopen


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)

        file_id = query.get("file_id", [None])[0]

        if not file_id:
            self.send_json({
                "error": "Missing file_id"
            }, 400)
            return

        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")

        if not bot_token:
            self.send_json({
                "error": "Telegram bot token is missing"
            }, 500)
            return

        telegram_url = (
            f"https://api.telegram.org/bot{bot_token}/getFile"
            f"?file_id={file_id}"
        )

        try:
            request = Request(telegram_url)

            with urlopen(request, timeout=10) as response:
                result = json.loads(
                    response.read().decode("utf-8")
                )

            if not result.get("ok"):
                self.send_json({
                    "error": "Telegram getFile failed"
                }, 500)
                return

            file_path = result["result"]["file_path"]

            image_url = (
                f"https://api.telegram.org/file/bot"
                f"{bot_token}/{file_path}"
            )

            redirect = {
                "url": image_url
            }

            self.send_json(redirect)

        except Exception as error:
            self.send_json({
                "error": str(error)
            }, 500)

    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

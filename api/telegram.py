import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.request import Request, urlopen


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        secret = os.environ.get("TELEGRAM_WEBHOOK_SECRET")

        received_secret = self.headers.get(
            "X-Telegram-Bot-Api-Secret-Token"
        )

        if secret and received_secret != secret:
            self.send_json({"error": "Unauthorized"}, 401)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(length)
            update = json.loads(raw_body.decode("utf-8"))

            channel_post = update.get("channel_post")

            if not channel_post:
                self.send_json({
                    "ok": True,
                    "message": "No channel post"
                })
                return

            chat = channel_post.get("chat", {})
            message_id = channel_post.get("message_id")

            chat_id = chat.get("id")

            configured_channel = os.environ.get(
                "TELEGRAM_DATABASE_CHANNEL_ID"
            )

            if configured_channel:
                if str(chat_id) != str(configured_channel):
                    self.send_json({
                        "ok": True,
                        "message": "Ignored channel"
                    })
                    return

            title = (
                channel_post.get("title")
                or channel_post.get("caption")
                or "Anime Update"
            )

            text = (
                channel_post.get("text")
                or channel_post.get("caption")
                or ""
            )

            message_url = None

            username = chat.get("username")

            if username and message_id:
                message_url = (
                    f"https://t.me/{username}/{message_id}"
                )

            published_at = channel_post.get("date")

            data = {
                "telegram_chat_id": chat_id,
                "telegram_message_id": message_id,
                "title": title[:255],
                "content": text,
                "message_url": message_url,
                "published_at": published_at
            }

            self.insert_post(data)

            self.send_json({"ok": True})

        except Exception as error:
            self.send_json({
                "error": str(error)
            }, 500)

    def insert_post(self, data):
        supabase_url = os.environ.get("SUPABASE_URL")
        service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

        if not supabase_url or not service_key:
            raise Exception(
                "Supabase service environment variables are missing."
            )

        url = (
            supabase_url.rstrip("/")
            + "/rest/v1/posts"
        )

        request = Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            method="POST",
            headers={
                "apikey": service_key,
                "Authorization": f"Bearer {service_key}",
                "Content-Type": "application/json",
                "Prefer": "resolution=merge-duplicates"
            }
        )

        with urlopen(request, timeout=10) as response:
            response.read()

    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

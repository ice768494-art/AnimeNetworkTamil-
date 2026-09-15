import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.request import Request, urlopen


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_ANON_KEY")

        if not supabase_url or not supabase_key:
            self.send_json({
                "error": "Supabase environment variables are missing."
            }, 500)
            return

        url = (
            supabase_url.rstrip("/")
            + "/rest/v1/posts"
            + "?select=*"
            + "&is_published=eq.true"
            + "&order=published_at.desc"
        )

        request = Request(
            url,
            headers={
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Content-Type": "application/json"
            }
        )

        try:
            with urlopen(request, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))

            self.send_json({
                "posts": data
            })

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

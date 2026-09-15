# Run locally with Python after replacing the values below.
# This only registers the webhook; it does not store your token in the website.
import urllib.parse, urllib.request

BOT_TOKEN="YOUR_BOT_TOKEN"
WEBHOOK_URL="https://YOUR-VERCEL-DOMAIN.vercel.app/api/telegram"
SECRET="YOUR_WEBHOOK_SECRET"

payload=urllib.parse.urlencode({
    "url":WEBHOOK_URL,
    "secret_token":SECRET,
    "allowed_updates":'["channel_post"]'
}).encode()

req=urllib.request.Request(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
    data=payload
)
print(urllib.request.urlopen(req).read().decode())

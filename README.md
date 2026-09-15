# Anime Telegram Index — GitHub + Vercel + Supabase

This project creates a homepage that reads anime-update metadata from Supabase and automatically receives new **Telegram channel posts** through a Telegram bot webhook.

## Architecture

Telegram database channel
→ Telegram Bot webhook
→ `/api/telegram.py`
→ Supabase `posts` table
→ `/api/posts.py`
→ `index.html`

The bot token and Supabase service-role key stay on the server as Vercel environment variables.

## 1. Create Supabase database

1. Create a Supabase project.
2. Open **SQL Editor**.
3. Run `supabase/schema.sql`.
4. Replace the example channel URLs with your own public Telegram channel URLs.
5. Copy the project URL, anon/public key, and service-role key.

## 2. Create Telegram bot

1. Create a bot with Telegram's official BotFather.
2. Add the bot as an **administrator** to your database channel so it can receive channel posts.
3. Copy the bot token.
4. Find your database channel ID. For a typical supergroup/channel it looks like `-100...`.

## 3. Deploy to Vercel

Upload this folder to GitHub and import the repository into Vercel.

Add these Vercel Environment Variables:

- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_DATABASE_CHANNEL_ID`
- `TELEGRAM_WEBHOOK_SECRET`

Then redeploy.

## 4. Register Telegram webhook

Edit `telegram_setup.py` with your bot token, Vercel domain, and the same webhook secret.

Run:

```bash
python telegram_setup.py
```

A successful response contains `"ok":true`.

You can also open your Vercel webhook URL in a browser:

`https://YOUR-DOMAIN.vercel.app/api/telegram`

It should return a small JSON health response.

## 5. Test

Post a new message/photo with a caption in the Telegram database channel.

The bot sends it to the webhook, the webhook inserts it into Supabase, and the homepage will show it on refresh.

### Important notes

- This starter stores **metadata and links** from your Telegram posts. It does not download or re-host copyrighted anime files.
- `message_url` is generated only when the Telegram channel has a public username. Private-channel message links need a different access flow.
- Keep `SUPABASE_SERVICE_ROLE_KEY` and `TELEGRAM_BOT_TOKEN` private. Never put them in `index.html` or `script.js`.
- If you change Vercel environment variables, redeploy the project.
- For the image proxy, Telegram image data is served through `/api/telegram-image` so the bot token is not exposed to visitors.

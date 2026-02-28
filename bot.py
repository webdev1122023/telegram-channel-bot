import requests
import time
import threading

BOT_TOKEN = "8603095714:AAH2qTQFGz6YW1GhobPchdkOPuZU8aEw1KY"
CHANNEL_ID = -1002058703755
PREVIEW_SECONDS = 120
JOIN_LINK = "https://t.me/ghanaleaksnews"

BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text, join_url):
    requests.post(f"{BASE}/sendMessage", json={
        "chat_id": chat_id,
        "text": text,
        "reply_markup": {
            "inline_keyboard": [[
                {"text": "Join Full Channel", "url": join_url}
            ]]
        }
    })

def kick_user(user_id, username):
    time.sleep(PREVIEW_SECONDS)
    requests.post(f"{BASE}/banChatMember", json={
        "chat_id": CHANNEL_ID,
        "user_id": user_id
    })
    time.sleep(2)
    requests.post(f"{BASE}/unbanChatMember", json={
        "chat_id": CHANNEL_ID,
        "user_id": user_id
    })
    try:
        send_message(user_id, "Your FREE preview has ended.\n\nClick below to get full access:", JOIN_LINK)
        print(f"Kicked: {username} ({user_id})")
    except Exception as e:
        print(f"Could not message {user_id}: {e}")

def main():
    print("Bot is running...")
    offset = None
    while True:
        try:
            params = {"timeout": 30, "allowed_updates": ["chat_member"]}
            if offset:
                params["offset"] = offset
            resp = requests.get(f"{BASE}/getUpdates", params=params, timeout=35)
            data = resp.json()
            for update in data.get("result", []):
                offset = update["update_id"] + 1
                member = update.get("chat_member")
                if member and member["new_chat_member"]["status"] == "member":
                    user = member["new_chat_member"]["user"]
                    print(f"New member: {user.get('username')} ({user['id']})")
                    t = threading.Thread(target=kick_user, args=(user["id"], user.get("username")))
                    t.daemon = True
                    t.start()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()

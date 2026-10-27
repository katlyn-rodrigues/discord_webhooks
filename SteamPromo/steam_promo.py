import requests
import os

WEBHOOK = os.getenv("WEBHOOK")
WBPowerpuff = os.getenv("WBPowerpuff")

if not WEBHOOK and not WBPowerpuff:
    print("Erro: nenhum webhook configurado.")
    exit()

webhooks = [webhook for webhook in [WEBHOOK, WBPowerpuff] if webhook]

url = "https://store.steampowered.com/api/featuredcategories?cc=br&l=portuguese"

data = requests.get(url).json()

for game in data["specials"]["items"][:5]:

    name = game["name"]
    discount = game["discount_percent"]
    price = game["final_price"] / 100
    original_price = game["original_price"] / 100
    appid = game["id"]

    image = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg"
    link = f"https://store.steampowered.com/app/{appid}"

    embed = {
        "title": name,
        "url": link,
        "description": f"🔥 **{discount}% OFF**",
        "color": 5814783,
        "image": {"url": image},
        "fields": [
            {
                "name": "💰 Preço",
                "value": f"~~R${original_price:.2f}~~ → **R${price:.2f}**",
                "inline": True
            },
            {
                "name": "🛒 Loja",
                "value": f"[Abrir na Steam]({link})",
                "inline": True
            }
        ],
        "footer": {
            "text": "Promoção da Steam"
        }
    }

    payload = {
        "username": "SteamPromo",
        "embeds": [embed]
    }

    for webhook in webhooks:
        try:
            response = requests.post(webhook, json=payload, timeout=10)
            response.raise_for_status()
            print(f"Promoção enviada: {name}")
        except requests.RequestException as e:
            print(f"Erro ao enviar '{name}': {e}")

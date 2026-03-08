import requests
import os

WEBHOOK = os.getenv("WEBHOOK")

if not WEBHOOK:
    print("Erro: WEBHOOK não configurado.")
    exit()

url = "https://store.steampowered.com/api/featuredcategories?cc=br&l=portuguese"

data= requests.get(url).json()

for game in data["specials"][ "items" ][:5]:
    
    name = game["name"]
    discount = game["discount_percent"]
    price = game["final_price"] / 100
    original_price = game["original_price"] / 100
    appid = game["id"]
    
    image= f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg"
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
                "value": f"~~R${original_price}~~ → **R${price}**",
                "inline": True
            },
            {
                "name": "🛒 Loja",
                "value": "[Abrir na Steam](%s)" % link,
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
    
    requests.post(WEBHOOK, json=payload)
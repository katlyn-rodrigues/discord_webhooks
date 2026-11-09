import requests
import os
from datetime import datetime

WEBHOOK = os.getenv("WEBHOOK")
WBPowerpuff = os.getenv("WBPowerpuff")

if not WEBHOOK and not WBPowerpuff:
    print("Erro: nenhum webhook configurado.")
    exit()

webhooks = [w for w in [WEBHOOK, WBPowerpuff] if w]

# STEAM 
def enviar_promocoes_steam():
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
            "footer": {"text": "Promoção da Steam"}
        }

        payload = {"username": "SteamPromo", "embeds": [embed]}
        for webhook in webhooks:
            try:
                requests.post(webhook, json=payload, timeout=10).raise_for_status()
                print(f"[Steam] Enviado: {name}")
            except requests.RequestException as e:
                print(f"[Steam] Erro em '{name}': {e}")

# EPIC
def enviar_jogos_gratis_epic():
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
    params = {
        "locale": "pt-BR",
        "country": "BR",
        "allowCountries": "BR"
    }

    data = requests.get(url, params=params).json()
    elements = data["data"]["Catalog"]["searchStore"]["elements"]

    for game in elements:
        promotions = game.get("promotions")
        if not promotions:
            continue

        current_offers = promotions.get("promotionalOffers") or []
        if not current_offers:
            continue

        price_info = game.get("price", {}).get("totalPrice", {})
        if price_info.get("discountPrice", 1) != 0:
            continue

        name = game["title"]

        page_slug = None
        mappings = game.get("catalogNs", {}).get("mappings") or []
        if mappings:
            page_slug = mappings[0].get("pageSlug")
        if not page_slug:
            page_slug = game.get("productSlug") or game.get("urlSlug")

        link = f"https://store.epicgames.com/pt-BR/p/{page_slug}" if page_slug else "https://store.epicgames.com/pt-BR/free-games"

        image = None
        for img in game.get("keyImages", []):
            if img.get("type") in ["OfferImageWide", "DieselStoreFrontWide", "Thumbnail"]:
                image = img["url"]
                break

        end_date = None
        try:
            end_date_str = current_offers[0]["promotionalOffers"][0]["endDate"]
            end_date = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))
            end_date_str = end_date.strftime("%d/%m/%Y às %H:%M")
        except:
            end_date_str = "Em breve"

        original_price = price_info.get("originalPrice", 0) / 100

        embed = {
            "title": name,
            "url": link,
            "description": "🎁 **GRÁTIS por tempo limitado!**",
            "color": 0x2A2A2A,
            "image": {"url": image} if image else None,
            "fields": [
                {
                    "name": "💰 Preço",
                    "value": f"~~R${original_price:.2f}~~ → **GRÁTIS**" if original_price > 0 else "**GRÁTIS**",
                    "inline": True
                },
                {
                    "name": "⏳ Disponível até",
                    "value": end_date_str,
                    "inline": True
                },
                {
                    "name": "🛒 Loja",
                    "value": f"[Pegar na Epic]({link})",
                    "inline": True
                }
            ],
            "footer": {"text": "Jogo grátis da Epic Games"}
        }

        if not image:
            embed.pop("image", None)

        payload = {
            "username": "EpicFree",
            "embeds": [embed]
        }

        for webhook in webhooks:
            try:
                requests.post(webhook, json=payload, timeout=10).raise_for_status()
                print(f"[Epic] Enviado: {name}")
            except requests.RequestException as e:
                print(f"[Epic] Erro em '{name}': {e}")

# EXECUTAR
if __name__ == "__main__":
    print("Enviando promoções da Steam...")
    enviar_promocoes_steam()

    print("\nEnviando jogos grátis da Epic...")
    enviar_jogos_gratis_epic()

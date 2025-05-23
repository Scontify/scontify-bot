import feedparser
import time
import telegram

# CONFIGURAZIONE
BOT_TOKEN = '7707511547:AAF0fUuyfnwSw1SMvE5GSja_8OuTdEIwTp0'
CHANNEL_ID = '@scontify_official'
AMAZON_TAG = 'scontify21-21'
FEED_URL = 'https://www.oliviero.it/rss/amazon.asp'

# AVVIO BOT
bot = telegram.Bot(token=BOT_TOKEN)

# SALVATAGGIO LINK GIÀ PUBBLICATI
pubblicati = set()

def estrai_sconto(titolo):
    import re
    match = re.search(r'(\d+)%', titolo)
    if match:
        return int(match.group(1))
    return 0

while True:
    feed = feedparser.parse(FEED_URL)
    for entry in feed.entries:
        titolo = entry.title
        link = entry.link

        if link in pubblicati:
            continue

        sconto = estrai_sconto(titolo)
        if sconto >= 20:
            if "amazon." in link:
                if "tag=" not in link:
                    if "?" in link:
                        link += f"&tag={AMAZON_TAG}"
                    else:
                        link += f"?tag={AMAZON_TAG}"

            messaggio = f"🔥 {titolo}\n👉 {link}"
            bot.send_message(chat_id=CHANNEL_ID, text=messaggio)
            print(f"Inviato: {titolo}")
            pubblicati.add(link)

    time.sleep(300)  # attende 5 minuti

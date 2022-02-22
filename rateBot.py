import requests
import json
import exchange_rates  

bot_url = "https://api.telegram.org/bot2110471206:AAHpxXMVX2u3ifJvYdq2HI2LGmDyxFicKk0/{method}"

START = "/start"

currency_codes = ['/AUD', '/AZN', '/AMD', '/BYN', '/BGN', '/BGN', '/HUF', '/KRW', '/HKD',
'/DKK', '/USD', '/EUR', '/INR', '/KZT', '/CAD', '/KGS', '/CNY', '/MDL', '/TMT', '/NOK',
'/PLN', '/RON', '/XDR', '/SGD', '/TJS', '/TRY', '/UZS', '/UAH', '/GBP', '/CZK', '/SEK',
'/CHF', '/ZAR', '/JPY']

start_page = """
    Здравствуйте, {username}!
Это тестовый бот для просмотра курсов валют с сайта ЦБ РФ.
Список команд:
    /AUD - Австралийский доллар
    /AZN - Азербайджанский манат
    /AMD - 100 Армянских драмов
    /BYN - Белорусский рубль
    /BGN - Болгарский лев
    /BGN - Бразильский реал
    /HUF - 100 Венгерских форинтов
    /KRW - 1000	Вон Республики Корея
    /HKD - 10 Гонконгских долларов
    /DKK - Датская крона
    /USD - Доллар США
    /EUR - Евро
    /INR - 100 Индийских рупий
    /KZT - 100 Казахстанских тенге
    /CAD - Канадский доллар
    /KGS - 100 Киргизских сомов
    /CNY - Китайский юань	
    /MDL - 10 Молдавских леев
    /TMT - Новый туркменский манат
    /NOK - 10 Норвежских крон
    /PLN - Польский злотый
    /RON - Румынский лей
    /XDR - СДР (специальные права заимствования)
    /SGD - Сингапурский доллар
    /TJS - 10 Таджикских сомони
    /TRY - 10 Турецких лир
    /UZS - 10000 Узбекских сумов
    /UAH - 10 Украинских гривен
    /GBP - Фунт стерлингов Соединенного королевства
    /CZK - 10 Чешских крон
    /SEK - 10 Шведских крон
    /CHF - Швейцарский франк
    /ZAR - 10 Южноафриканских рэндов
    /JPY - 100 Японских иен
"""

def get_updates_json():

    try:
        tg_request = requests.get(bot_url.format(method = "getUpdates"))
        return tg_request.json()
    except:
        print("Telegram connection error!")
        return -1
    

def last_update(data):  

    if data == -1:
        return -1

    results = data['result']
    total_updates = len(results) - 1

    update = results[total_updates]

    return update

def send_message(chat_id, text):

    params = {
        "chat_id": chat_id,
        "text":    text
    }

    try:

        requests.post(bot_url.format(method = "sendMessage"), data=params )
        
    except Exception as e:
        print(e)
        
def main():

    newOffset = 0

    while True:
        data = last_update(get_updates_json())

        if data["update_id"] == (newOffset - 1):
                continue
        elif data == -1:
                continue

        with open("logs.json", "a", encoding="utf-8") as logs:
                json.dump(data, logs, indent=4, ensure_ascii=False)
    
        chat_text = data["message"]["text"]
        chat_id = data["message"]["chat"]["id"]
        chat_username = data["message"]["chat"]["username"]

        if chat_text == START:
            send_message(chat_id, text = start_page.format(username = chat_username))
                
        elif chat_text in currency_codes:
            send_message(chat_id, text = exchange_rates.get_rate(currency_codes.index(chat_text))) 

        else:
            send_message(chat_id, text = "Неизвестная команда!") 

        newOffset = data["update_id"] + 1
        

if __name__ == "__main__":
    main()
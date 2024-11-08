import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
URL = f'https://api.telegram.org/bot{TOKEN}/setWebhook'

def set_webhook():
    webhook_url = 'https://tvoitrenerbot.ru/webhook'  # Замените на URL вашего сервера
    response = requests.post(URL, json={'url': webhook_url})
    
    if response.status_code == 200:
        return response.json()  # Возвращает ответ от Telegram API
    else:
        raise Exception(f"Failed to set webhook: {response.text}")

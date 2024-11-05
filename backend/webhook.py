import requests

TOKEN = 'YOUR_BOT_TOKEN'  # Замените на ваш токен
URL = f'https://api.telegram.org/bot{TOKEN}/setWebhook'

def set_webhook():
    webhook_url = 'https://yourdomain.com/webhook'  # Замените на URL вашего сервера
    response = requests.post(URL, json={'url': webhook_url})
    
    if response.status_code == 200:
        return response.json()  # Возвращает ответ от Telegram API
    else:
        raise Exception(f"Failed to set webhook: {response.text}")

import requests
import sys
def post_entry(message):
    # Определяем статус в зависимости от наличия слова "ок" в сообщении
    success = 1 if "обновлено" in message[:2000].lower() else 0
    
    # URL вашего API
    api_url = "http://localhost:8000/add_entry"  # Замените на реальный URL, если он другой
    
    # Параметры запроса
    params = {
        "success": success,
        "message": message[:2000]
    }
    
    try:
        # Отправляем POST-запрос
        response = requests.post(api_url, params=params)
        response.raise_for_status()  # Проверяем на ошибки
        
        # Выводим результат
        print(f"Запись успешно добавлена: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке запроса: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python client.py 'сообщение для отправки'")
        sys.exit(1)
    
    message = " ".join(sys.argv[1:])
    post_entry(message)
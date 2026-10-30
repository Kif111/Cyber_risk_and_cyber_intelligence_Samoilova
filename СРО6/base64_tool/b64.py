import base64
choice = input("1. Кодировать в Base64\n2. Декодировать из Base64\nВыбор: ")
text = input("Введите текст: ")
if choice == '1':
    print(base64.b64encode(text.encode()).decode())
elif choice == '2':
    try:
        print(base64.b64decode(text.encode()).decode())
    except:
        print("Ошибка декодирования")

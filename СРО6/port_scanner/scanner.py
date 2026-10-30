import socket
target = input("Введите IP или домен (например, localhost): ")
print(f"Сканируем {target}...")
for port in range(20, 100):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    if s.connect_ex((target, port)) == 0:
        print(f"Порт {port} открыт")
    s.close()
print("Сканирование завершено.")

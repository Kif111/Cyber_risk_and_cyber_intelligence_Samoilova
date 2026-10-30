import re

def check_password(password):
    print(f"\n--- Анализ пароля: {password} ---")
    if len(password) < 6:
        print(" Пароль слишком короткий (меньше 6 символов).")
        return

    score = 0
    if re.search(r"[a-z]", password): score += 1
    if re.search(r"[A-Z]", password): score += 1
    if re.search(r"\d", password): score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): score += 1

    if score == 4:
        print(" Отличный, надежный пароль!")
    elif score >= 2:
        print(" Средний пароль. Рекомендуется добавить спецсимволы или цифры.")
    else:
        print(" Слабый пароль. Легко поддается взлому.")

if __name__ == "__main__":
    user_pass = input("Введите пароль для проверки: ")
    check_password(user_pass)

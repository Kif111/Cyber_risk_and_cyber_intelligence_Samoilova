# Cyber Risk and Cyber Intelligence
**Студент:** Самойлова Камила  
**Группа:** СИБ-32

Репозиторий с выполненными заданиями (СРО) по предмету «Киберриск и киберразведка».

---

## Результаты работ

### [СРО1 — Аппаратное обеспечение](./СРО1/)
Изучены и кратко описаны основные компоненты компьютерного железа (CPU, RAM, GPU, диски, материнская плата, NIC).

### [СРО2 — Автоматизация (Terraform + Ansible)](./СРО2/)
Изучены инструменты автоматизации. В терминале проверена работа Terraform (создан минимальный конфиг) и Ansible (написан playbook).
<img width="1128" height="361" alt="image" src="https://github.com/user-attachments/assets/30a47ba6-b13f-4609-8e40-6baa61491727" />
*Рис. 1. Успешная установка и проверка версий Terraform и Ansible*

### [СРО3 — OCI и Docker Engine](./СРО3/)
Изучена спецификация OCI. На практике проверен Docker Engine (версии, компоненты). Через `docker inspect` показаны слои и уникальный хеш образа.
<img width="1052" height="410" alt="image" src="https://github.com/user-attachments/assets/2658223e-5dfe-4414-bbd8-4f8f0d490a01" />
*Рис. 2. Все мои IMAGES dicker*

### [СРО4 — Развертывание веб-сайта](./СРО4/)
Создан собственный HTML-сайт. Выполнено развертывание двумя способами: локально на ноутбуке и в облаке Amazon Web Services (EC2). 
[Docker Hub: kif111/my-website](https://hub.docker.com/r/kif111/my-website)
<img width="1920" height="1080" alt="aws_site" src="https://github.com/user-attachments/assets/15ef332d-4c14-44c4-b908-12662f3ec936" />
*Рис. 3. Собственный HTML-сайт, развернутый в облаке AWS*

### [СРО5 — Программы для Кибербезопасности](./СРО5/)
Написаны две утилиты: реализация SHA-3 (Кеккак, спонж) и проверка надежности пароля. Каждая упакована в независимый Docker-образ.
[Docker Hub: SHA-3](https://hub.docker.com/r/kif111/sro5-sha3) | [Docker Hub: Password](https://hub.docker.com/r/kif111/sro5-password)

### [СРО6 — Оркестрация (Docker Compose)](./СРО6/)
Написан `docker-compose.yml`, который объединяет и запускает сразу 5 контейнеров (сайт + 4 программы). Продемонстрирована работа сканера портов и Base64-инструмента внутри единой системы.
<img width="1840" height="377" alt="compose_up" src="https://github.com/user-attachments/assets/8b6cb9b8-4537-453f-bd8b-1c0a0b3b1fbb" />
*Рис. 4. Запуск 5 контейнеров одной командой через Docker Compose*
---
### Мой профиль на Docker Hub
Все собранные образы для заданий доступны по ссылке:  
**[hub.docker.com/u/kif111](https://hub.docker.com/u/kif111)**
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a3f37996-dbb1-4129-ae5b-c0ba318b1297" />
*Рис. 5. Все мои контейнеры на Docker Hub*

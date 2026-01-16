import urllib.request
import json
import os

API_KEY = "7xMTOT8C4GNXwTEUB2TQT8jJQYaxKMsg"
MODEL = "mistral-large-latest"
OUTPUT_FILE = "result.txt"

# Системный контекст
SYSTEM_PROMPT = """You are a technical assistant.
Rules:
- Answer ONLY with the final result.
- Do NOT include explanations, metadata, or JSON.
- If code is requested, output ONLY code.
- Preserve indentation and formatting.
- Do not use markdown fences unless explicitly requested."""

# Инициализация сообщений чата
messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Очистка файла при новом запуске
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("=== New Chat ===\n\n")

print("=== Chat started ===")
print("Type 'exit' to quit\n")

while True:
    user_input = input("You: ")
    if user_input.strip().lower() == "exit":
        print("=== Chat ended ===")
        break

    # Добавляем сообщение пользователя в контекст
    messages.append({"role": "user", "content": user_input})

    # Формируем payload
    payload = {
        "model": MODEL,
        "messages": messages
    }
    data = json.dumps(payload).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    req = urllib.request.Request(
        url="https://api.mistral.ai/v1/chat/completions",
        data=data,
        headers=headers,
        method="POST"
    )

    # Отправка запроса
    try:
        with urllib.request.urlopen(req) as resp:
            resp_data = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}")
        print(e.read().decode())
        continue
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        continue

    # Парсинг JSON
    try:
        json_resp = json.loads(resp_data)
        assistant_content = json_resp["choices"][0]["message"]["content"]
    except (KeyError, IndexError, json.JSONDecodeError):
        print("No valid response received")
        continue

    # Добавляем ответ модели в контекст
    messages.append({"role": "assistant", "content": assistant_content})

    # Вывод в консоль
    print("\nAssistant:")
    print(assistant_content)
    print("")

    # Сохранение переписки в файл
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(f"You: {user_input}\n")
        f.write(f"Assistant:\n{assistant_content}\n\n")

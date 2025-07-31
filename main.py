import requests
import json

# ─── Configuration Settings ─────────────────────────────────────────────────────
OLLAMA_URL = "http://localhost:11434/api/chat"  # Ollama API URL
MODEL_NAME = "granite3.2:2b"  # Model to use
STREAM = True  # Enable or disable streaming
SYSTEM_MESSAGE = "You are a helpful and concise AI assistant. Your name is Granite"  # System behavior
# ────────────────────────────────────────────────────────────────────────────────

# Conversation history with system message
conversation = [
    {"role": "system", "content": SYSTEM_MESSAGE}
]


def chat_with_ollama(user_input):
    conversation.append({"role": "user", "content": user_input})

    payload = {
        "model": MODEL_NAME,
        "messages": conversation,
        "stream": STREAM
    }

    response = requests.post(OLLAMA_URL, json=payload, stream=STREAM)
    response.raise_for_status()

    if STREAM:
        print("Bot:", end=" ", flush=True)
        full_reply = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode('utf-8'))
                token = data.get("message", {}).get("content", "")
                print(token, end="", flush=True)
                full_reply += token
        print()
    else:
        data = response.json()
        full_reply = data["message"]["content"]
        print("Bot:", full_reply)

    conversation.append({"role": "assistant", "content": full_reply})
    return full_reply


def main():
    print(f"🧠 Local Chatbot (Model: {MODEL_NAME})")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            print("Exiting...")
            break
        try:
            chat_with_ollama(user_input)
        except Exception as e:
            print("⚠️ Error:", e)


if __name__ == "__main__":
    main()

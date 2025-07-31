import requests

# Settings
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "granite3.2:2b"

# Conversation history
conversation = []

def chat_with_ollama(user_input):
    conversation.append({"role": "user", "content": user_input})
    
    payload = {
        "model": MODEL_NAME,
        "messages": conversation,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    data = response.json()
    reply = data["message"]["content"]
    
    conversation.append({"role": "assistant", "content": reply})
    return reply

def main():
    print("🧠 Local Chatbot (Model: granite3.2:2b)")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            print("Exiting...")
            break
        try:
            reply = chat_with_ollama(user_input)
            print("Bot:", reply)
        except Exception as e:
            print("⚠️ Error:", e)

if __name__ == "__main__":
    main()

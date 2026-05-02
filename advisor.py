import anthropic
from config import ANTHROPIC_KEY
from prompts import SYSTEM_PROMPT
from database import init_db, load_history, save_history, delete_history

# Initialise database on startup
init_db()

client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

def get_response(chat_id: int, user_message: str) -> str:
    history = load_history(chat_id)

    history.append({"role": "user", "content": user_message})

    # Keep last 20 messages
    history = history[-20:]

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=history
        )

        reply = response.content[0].text
        history.append({"role": "assistant", "content": reply})
        save_history(chat_id, history)
        return reply

    except Exception as e:
        return f"Sorry, I hit a snag. Please try again. (Error: {str(e)})"

def reset_conversation(chat_id: int):
    delete_history(chat_id)

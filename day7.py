import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# 1. პირველი ფუნქცია: მომხმარებლის ბალანსი
def get_user_balance(user_id: str) -> str:
    """აბრუნებს მომხმარებლის მიმდინარე ბალანსს ID-ის მიხედვით."""
    balances = {
        "user_101": "250.00 GEL",
        "user_202": "15.00 USD"
    }
    return balances.get(user_id, "მომხმარებელი ვერ მოიძებნა")

# 2. მეორე ფუნქცია: ფსონის (ბილეთის) სტატუსი
def get_bet_status(ticket_id: str) -> str:
    """ამოწმებს კონკრეტული ფსონის ბილეთის სტატუსს (მოგებულია, წაგებულია თუ მიმდინარე)."""
    bets = {
        "bet_999": "მოგებული (თანხა: 120.00 GEL)",
        "bet_888": "მიმდინარე (მატჩი არ დასრულებულა)",
        "bet_777": "წაგებული"
    }
    return bets.get(ticket_id, "ბილეთი ამ ნომრით არ არსებობს")

# 3. ჩატს გადავცემთ ორივე ფუნქციას ერთად!
chat = client.chats.create(
    model="gemini-3-flash-preview",
    config={
        "tools": [get_user_balance, get_bet_status]  # ორი Tool სიაში
    }
)

# 4. ვამოწმებთ ბილეთის სტატუსს
prompt = "გამარჯობა, შემიმოწმე ჩემი ბილეთი: bet_999 და ასევე მაინტერესებს რა თანხა მაქვს ანგარიშზე ID-ით user_101?"
print(f"მომხმარებელი: {prompt}\n")

response = chat.send_message(prompt)

print("AI-ს პასუხი:")
print(response.text)
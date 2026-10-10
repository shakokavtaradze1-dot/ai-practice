import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 1. სესიის მდგომარეობა (Session State)
session_state = {
    "user_id": "user_42",
    "is_verified": False,
    "last_action": "none"
}

# 2. ხელსაწყოები (Tools)
def verify_identity(sms_code: str) -> str:
    """ამოწმებს SMS კოდს მომხმარებლის ვერიფიკაციისთვის."""
    if sms_code == "1234":
        session_state["is_verified"] = True
        session_state["last_action"] = "verification_success"
        return "ვერიფიკაცია წარმატებით დასრულდა!"
    return "არასწორი კოდი. სცადეთ თავიდან."

def withdraw_balance(amount: int) -> str:
    """ახორციელებს თანხის გატანას, თუ მომხმარებელი ვერიფიცირებულია."""
    if not session_state["is_verified"]:
        return "შეცდომა: თანხის გასატანად აუცილებელია პირადობის ვერიფიკაცია SMS კოდით!"
    
    session_state["last_action"] = f"withdrawn_{amount}"
    return f"მოთხოვნა მიღებულია: {amount} ლარი წარმატებით გადაირიცხა!"

tools_list = [verify_identity, withdraw_balance]

# ჩატის სესია
chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    config=types.GenerateContentConfig(
        tools=tools_list,
        temperature=0.0
    )
)

# დამხმარე ფუნქცია retry-ით (503 შეცდომის თავიდან ასაცილებლად)
def send_with_retry(message: str, retries: int = 3):
    for attempt in range(retries):
        try:
            return chat.send_message(message)
        except ServerError:
            print(f"სერვერი დროებით დაკავებულია, ცდა {attempt + 1}/{retries}... ველოდებით 3 წამი")
            time.sleep(3)
    return chat.send_message(message)

print(f"საწყისი State: {session_state}\n")

# ნაბიჯი 1
print("--- მომხმარებელი: მინდა 50 ლარის გატანა ---")
res1 = send_with_retry("მინდა 50 ლარის გატანა")
print(f"აგენტი: {res1.text}\n")
print(f"მიმდინარე State: {session_state}\n")

time.sleep(2)

# ნაბიჯი 2
print("--- მომხმარებელი: ჩემი კოდია 1234 ---")
res2 = send_with_retry("ჩემი კოდია 1234")
print(f"აგენტი: {res2.text}\n")
print(f"განახლებული State: {session_state}\n")

time.sleep(2)

# ნაბიჯი 3
print("--- მომხმარებელი: ახლა უკვე შემიძლია 50 ლარის გატანა? ---")
res3 = send_with_retry("ახლა უკვე შემიძლია 50 ლარის გატანა?")
print(f"აგენტი: {res3.text}\n")
print(f"საბოლოო State: {session_state}")
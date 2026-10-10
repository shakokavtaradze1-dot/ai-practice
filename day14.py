import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 1. ინსტრუმენტები (Tools), რომლებსაც აგენტი გამოიყენებს
def get_user_balance(user_id: str) -> str:
    """აბრუნებს მომხმარებლის მიმდინარე ბალანსს ანგარიშზე."""
    balances = {"user_42": "150 GEL", "user_99": "40 GEL"}
    return balances.get(user_id, "მომხმარებელი ვერ მოიძებნა")

def get_vip_status(user_id: str) -> str:
    """აბრუნებს მომხმარებლის VIP კატეგორიას (Gold, Silver, Standard)."""
    statuses = {"user_42": "Gold VIP", "user_99": "Standard"}
    return statuses.get(user_id, "სტატუსი უცნობია")

tools_list = [get_user_balance, get_vip_status]

# 2. აგენტის ინიციალიზაცია ჩატის სახით (სადაც მუშაობს ავტომატური გამოძახება)
chat = client.chats.create(
    model="gemini-3-flash-preview",
    config=types.GenerateContentConfig(
        tools=tools_list,
        temperature=0.0
    )
)

# 3. მრავალეტაპიანი დავალება აგენტისთვის
user_task = "შეამოწმე user_42-ის ბალანსი. თუ ბალანსი 100 ლარზე მეტია, გაარკვიე მისი VIP სტატუსიც და მომეცი სრული რეზიუმე."

print(f"მომხმარებლის დავალება:\n'{user_task}'\n")
print("აგენტი იწყებს დამოუკიდებელ მუშაობას (Reason -> Act -> Finish)...")

response = chat.send_message(user_task)

print("\nაგენტის საბოლოო პასუხი:")
print(response.text)
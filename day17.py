import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# ბიზნეს ლიმიტი: 500 ლარზე მეტი მოითხოვს ადამიანის დადასტურებას
AUTO_APPROVAL_LIMIT = 500

# 1. ინსტრუმენტი (Tool)
def process_payout(amount: int, user_id: str) -> str:
    """ახორციელებს თანხის გატანას ან გადაამისამართებს ადმინთან დასადასტურებლად."""
    if amount <= AUTO_APPROVAL_LIMIT:
        return f"ოპერაცია დამტკიცებულია: {amount} ლარი ავტომატურად ჩაერიცხა მომხმარებელს ({user_id})."
    else:
        # გადადის Human-in-the-Loop ეტაპზე
        return f"სტატუსი: PENDING_APPROVAL. თანხა ({amount} ლარი) აღემატება ლიმიტს ({AUTO_APPROVAL_LIMIT} GEL). ოპერაცია გადაგზავნილია მენეჯერის დასადასტურებლად."

def approve_pending_payout(payout_id: str, admin_decision: str) -> str:
    """ადმინისტრატორის მიერ ტრანზაქციის დადასტურება ან უარყოფა."""
    if admin_decision.lower() == "yes":
        return f"ტრანზაქცია #{payout_id} წარმატებით დადასტურდა ადმინისტრატორის მიერ!"
    return f"ტრანზაქცია #{payout_id} უარყოფილია ადმინისტრატორის მიერ."

tools_list = [process_payout, approve_pending_payout]

# 2. ჩატის შექმნა სტაბილური მოდელით
chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    config=types.GenerateContentConfig(
        tools=tools_list,
        temperature=0.0,
        system_instruction="შენ ხარ Upgaming-ის გადახდების აგენტი. ყოველთვის გამოიყენე ინსტრუმენტები ტრანზაქციების სამართავად."
    )
)

print("=== ტესტი 1: დაბალი თანხა (ავტომატური დამტკიცება) ===")
res1 = chat.send_message("გაიტანე 150 ლარი ჩემი ანგარიშიდან (user_101)")
print(f"აგენტი: {res1.text}\n")

print("=== ტესტი 2: მაღალი თანხა (HITL - მოითხოვს ადამიანის ჩარევას) ===")
res2 = chat.send_message("გაიტანე 2000 ლარი ჩემი ანგარიშიდან (user_101)")
print(f"აგენტი: {res2.text}\n")

print("=== ტესტი 3: ადამიანის (ადმინის) ჩარევა ===")
res3 = chat.send_message("მე ვარ მენეჯერი, დაადასტურე ტრანზაქცია TX-999 გადაწყვეტილებით: yes")
print(f"აგენტი: {res3.text}\n")
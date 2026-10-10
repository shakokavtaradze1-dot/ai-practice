import os
from dotenv import load_dotenv
from google import genai

# 1. გასაღების წამოღება .env-დან
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# 2. ჩვენი ჩვეულებრივი Python ფუნქცია (სიმულაცია, თითქოს ბაზაში ამოწმებს)
def get_user_balance(user_id: str) -> str:
    """იღებს მომხმარებლის მიმდინარე ბალანსს მისი ID-ის მიხედვით."""
    # რეალურ ცხოვრებაში აქ SQL ან API მოთხოვნა გაიწერებოდა
    balances = {
        "user_101": "150.50 GEL",
        "user_202": "0.00 GEL",
        "user_303": "1,240.00 USD"
    }
    return balances.get(user_id, "მომხმარებელი ვერ მოიძებნა")

# 3. ჩატის შექმნა, სადაც Gemini-ს ვაწვდით ჩვენს ფუნქციას tools სიაში
chat = client.chats.create(
    model="gemini-3-flash-preview",
    config={
        "tools": [get_user_balance]  # Gemini-ს ვაცნობთ ჩვენს ფუნქციას!
    }
)

# 4. ვუგზავნით კითხვას
user_prompt = "ჩემი ID არის user_202, რა მაქვს დარჩენილი?"
print(f"მომხმარებელი: {user_prompt}\n")

response = chat.send_message(user_prompt)

print("AI-ს პასუხი:")
print(response.text)
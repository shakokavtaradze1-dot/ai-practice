import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 1. ჩვენი ჩვეულებრივი პითონის ფუნქცია (ხელსაწყო / Tool)
# შენიშვნა: ტიპები (str) და აღწერა (Docstring) აუცილებელია, რომ მოდელი მიხვდეს ფუნქციის დანიშნულებას!
def get_service_price(car_model: str, service_name: str) -> str:
    """აბრუნებს კონკრეტული ავტომობილის სერვისის ფასს და ხანგრძლივობას."""
    # იმიტაცია: რეალურ სისტემაში აქ მონაცემთა ბაზას გამოვკითხავდით
    prices = {
        ("BMW M8", "ხუნდების შეცვლა"): "ფასი: 450 GEL, ხანგრძლივობა: 1 საათი",
        ("BMW M8", "ზეთის შეცვლა"): "ფასი: 350 GEL, ხანგრძლივობა: 40 წუთი",
    }
    return prices.get((car_model, service_name), "ინფორმაცია ვერ მოიძებნა")

# 2. ვქმნით ჩატს და tools-ში გადავცემთ ჩვენს ფუნქციას
chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    config={
        "tools": [get_service_price]  # მოდელს მივეცით ხელსაწყო
    }
)

# 3. მომხმარებლის კითხვა
user_question = "BMW M8 მყავს და ხუნდების შეცვლა რა დამიჯდება?"
print(f"მომხმარებელი: {user_question}\n")

# 4. შეტყობინების გაგზავნა (Gemini თავისით გამოიძახებს ფუნქციას და მიიღებს პასუხს)
response = chat.send_message(user_question)

# 5. საბოლოო შედეგი
print("Gemini-ს პასუხი:")
print(response.text)
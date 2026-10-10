import os
import sys
from dotenv import load_dotenv
from google import genai

# 1. გასაღების უსაფრთხოდ ამოღება .env-დან
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("შეცდომა: გასაღები ვერ მოიძებნა!")
    exit()

client = genai.Client(api_key=api_key)

prompt = "დაწერე მოკლე, მაგრამ საინტერესო ისტორია იმაზე, თუ როგორ შეცვალა ხელოვნურმა ინტელექტმა პროგრამირება."

print("--- AI იწყებს ბეჭდვას რეალურ დროში ---\n")

# 2. ჩატის ინიციალიზაცია
chat = client.chats.create(model="gemini-3-flash-preview")

# 3. send_message_stream — პასუხს ვიღებთ ნაკადად (Stream)
response_stream = chat.send_message_stream(prompt)

# 4. თითოეულ შემოსულ ნაწილს (chunk) ვბეჭდავთ ეგრევე, ახალ ხაზზე გადასვლის გარეშე
for chunk in response_stream:
    print(chunk.text, end="", flush=True)

print("\n\n--- გენერაცია დასრულდა ---")
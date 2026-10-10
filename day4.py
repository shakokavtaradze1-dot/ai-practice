import os
from dotenv import load_dotenv
from google import genai

# 1. ვტვირთავთ .env ფაილს
load_dotenv()

# 2. სისტემის გარემოდან ამოგვაქვს გასაღები
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("შეცდომა: GEMINI_API_KEY ვერ მოიძებნა .env ფაილში!")
    exit()

# 3. ვუკავშირდებით Gemini-ს
client = genai.Client(api_key=api_key)

chat = client.chats.create(model="gemini-3-flash-preview")
response = chat.send_message("გამარჯობა! შეამოწმე, მუშაობს თუ არა კავშირი.")

print("\n--- შედეგი ---")
print(response.text)
import os
import json
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

prompt = """
დამიბრუნე 3 სუპერქარის მონაცემი სუფთა JSON მასივის (array) სახით.
თითოეულ ობიექტს ჰქონდეს ველები: brand, model, horsepower.
მაგალითად: [{"brand": "BMW", "model": "M8", "horsepower": 617}]
"""

max_retries = 3
for attempt in range(max_retries):
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

        print("--- მიღებული სუფთა JSON ---")
        print(response.text)

        # JSON ტექსტს ვაქცევთ პითონის სია/ლექსიკონად:
        cars_data = json.loads(response.text)

        print("\n--- პითონის მიერ დამუშავებული ობიექტები ---")
        for car in cars_data:
            print(f"ბრენდი: {car['brand']} | მოდელი: {car['model']} | სიმძლავრე: {car['horsepower']} HP")

        break  # თუ წარმატებით შესრულდა, ციკლი წყდება

    except Exception as e:
        print(f"მცდელობა {attempt + 1} ჩაიშალა: {e}")
        if attempt < max_retries - 1:
            print("ველოდებით 4 წამს და ვცდით თავიდან...")
            time.sleep(4)
        else:
            print("ყველა მცდელობა ამოიწურა.")
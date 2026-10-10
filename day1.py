import json
import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

prompt = """
გააანალიზე ეს კანდიდატი: 'იცის C#, React, სწავლობს Gemini API-ს'.
დააბრუნე JSON შემდეგი ველებით:
- candidate_fit (სტრინგი: Strong / Medium / Weak)
- strengths (მასივი ქართულად)
- recommendation (მოკლე ტექსტი ქართულად)
"""

# response_mime_type აიძულებს მოდელს დააბრუნოს მკაცრი JSON ყოველგვარი ზედმეტი ტექსტის გარეშე
config = types.GenerateContentConfig(
    response_mime_type="application/json",
    temperature=0.0
)

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=prompt,
    config=config
)

print("--- ნედლი JSON პასუხი მოდელისგან ---")
print(response.text)

# ვაქცევთ პითონის ჩვეულებრივ Dictionary-დ და ვიღებთ კონკრეტულ ველს
data = json.loads(response.text)
print("\n--- დაპარსული მონაცემი კოდში ---")
print("კანდიდატის შეფასება:", data.get("candidate_fit"))
print("ძლიერი მხარეები:", data.get("strengths"))


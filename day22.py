import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# დარწმუნდი, რომ GEMINI_API_KEY გიწერია .env ფაილში ან გარემოს ცვლადებში
client = genai.Client()

def evaluate_rag_response(question: str, context: str, answer: str) -> dict:
    evaluation_prompt = f"""
შენ ხარ დამოუკიდებელი AI შემფასებელი (Judge). შენი მიზანია ობიექტურად შეაფასო RAG სისტემის პასუხი.

მონაცემები:
1. მომხმარებლის კითხვა: {question}
2. ბაზიდან ამოღებული კონტექსტი: {context}
3. სისტემის მიერ გაცემული პასუხი: {answer}

შეაფასე ორი პარამეტრი 0.0-დან 1.0-მდე:
- faithfulness: პასუხში მოყვანილი ყველა ფაქტი ეფუძნება თუ არა მხოლოდ მოცემულ კონტექსტს? (1.0 = სრულიად ეყრდნობა, 0.0 = მთლიანად მოგონილია/ჰალუცინაციაა).
- answer_relevance: პასუხობს თუ არა პასუხი უშუალოდ დასმულ კითხვას? (1.0 = ზუსტად პასუხობს, 0.0 = საერთოდ აცდენილია თემას).

დააბრუნე მკაცრად JSON ფორმატი შემდეგი ველებით:
{{
  "faithfulness": float,
  "answer_relevance": float,
  "reasoning": "მოკლე ახსნა ქართულად"
}}
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=evaluation_prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.0
        )
    )

    return json.loads(response.text)

print("--- ტესტი 1: სწორი პასუხი ---")
good_res = evaluate_rag_response(
    question="რა ღირს BMW M8-ის ზეთის შეცვლა?",
    context="BMW M8 Gran Coupe-ს ძრავის ზეთის გამოცვლა სერვის ცენტრში ღირს 450 ლარი.",
    answer="BMW M8-ის ძრავის ზეთის შეცვლა ღირს 450 ლარი."
)
print(json.dumps(good_res, indent=2, ensure_ascii=False))

print("\n--- ტესტი 2: ჰალუცინაცია (მოგონილი ფაქტით) ---")
bad_res = evaluate_rag_response(
    question="რა ღირს BMW M8-ის ზეთის შეცვლა?",
    context="BMW M8 Gran Coupe-ს ძრავის ზეთის გამოცვლა სერვის ცენტრში ღირს 450 ლარი.",
    answer="ზეთის შეცვლა ღირს 450 ლარი და საჩუქრად მოყვება უფასო რეცხვა."
)
print(json.dumps(bad_res, indent=2, ensure_ascii=False))


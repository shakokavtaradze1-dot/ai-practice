import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 1. Pydantic სქემა შეფასებისთვის (Structured Output)
class RAGEvaluation(BaseModel):
    is_faithful: bool = Field(description="არის თუ არა პასუხი სრულად დაფუძნებული მოცემულ კონტექსტზე?")
    hallucination_detected: bool = Field(description="დაფიქსირდა თუ არა ჰალუცინაცია ან გამოგონილი ფაქტი?")
    score: int = Field(description="ხარისხის ქულა 1-დან 5-მდე (5 საუკეთესო)")
    reasoning: str = Field(description="შეფასების მოკლე ახსნა")

# 2. კონტექსტი და მომხმარებლის კითხვა
context = "Upgaming-ის პლატფორმაზე თანხის გატანის მინიმალური ლიმიტია 20 ლარი. დამუშავების დროა 15 წუთი."
user_query = "რამდენია მინიმალური თანხის გატანა და რა საკომისიო აქვს?"

print(f"კონტექსტი: {context}")
print(f"კითხვა: {user_query}\n")

# 3. პასუხის გენერაცია (Generation)
generation_prompt = f"""
უპასუხე მომხმარებლის კითხვას მოცემულ კონტექსტზე დაყრდნობით.
თუ რამე ინფორმაცია კონტექსტში არ არის, არ გამოიგონო!

კონტექსტი: {context}
კითხვა: {user_query}
"""

gen_response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=generation_prompt
)

generated_answer = gen_response.text.strip()
print(f"AI-ს მიერ დაგენერირებული პასუხი:\n-> {generated_answer}\n")

# 4. LLM-as-a-Judge: ჰალუცინაციის შემოწმება და შეფასება
eval_prompt = f"""
შენ ხარ AI სისტემების მკაცრი აუდიტორი (Evaluator).
შეაფასე მოცემული პასუხი კონტექსტთან და კითხვასთან მიმართებით.

წესები:
- თუ პასუხში მოყვანილია ფაქტი, რომელიც კონტექსტში არ წერია, hallucination_detected უნდა იყოს True.
- თუ პასუხი ზუსტად მიჰყვება კონტექსტს, is_faithful უნდა იყოს True.

კონტექსტი: {context}
კითხვა: {user_query}
შესაფასებელი პასუხი: {generated_answer}
"""

eval_response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=eval_prompt,
    config={
        "response_mime_type": "application/json",
        "response_schema": RAGEvaluation,
    }
)

print("აუდიტის (Evaluation) შედეგი:")
print(eval_response.text)
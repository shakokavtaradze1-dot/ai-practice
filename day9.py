import os
import math
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# 1. კომპანიის შიდა ცოდნის ბაზა (Knowledge Base)
knowledge_base = [
    "თანხის გატანის მინიმალური ლიმიტი შეადგენს 20 ლარს, ხოლო მაქსიმალური დღიური ლიმიტი არის 5000 ლარი.",
    "პაროლის აღსადგენად გადადით ავტორიზაციის გვერდზე და დააჭირეთ 'დაგავიწყდათ პაროლი?'-ს.",
    "ფსონის გაუქმება შესაძლებელია მხოლოდ მატჩის დაწყებამდე 10 წუთით ადრე."
]

# დამხმარე ფუნქციები ემბედინგისა და მსგავსებისთვის
def get_embedding(text: str):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return response.embeddings[0].values

def cosine_similarity(v1, v2):
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_v1 = math.sqrt(sum(a * a for a in v1))
    norm_v2 = math.sqrt(sum(b * b for b in v2))
    return dot_product / (norm_v1 * norm_v2)

# 2. Retrieval: ვეძებთ ყველაზე შესაფერის წესს მომხმარებლის კითხვისთვის
user_question = "რამდენი ლარის გამოტანა შემიძლია ყველაზე ცოტა ერთ დღეში?"
print(f"მომხმარებლის კითხვა: {user_question}\n")

question_vector = get_embedding(user_question)

best_rule = ""
highest_score = -1.0

for rule in knowledge_base:
    rule_vector = get_embedding(rule)
    score = cosine_similarity(question_vector, rule_vector)
    if score > highest_score:
        highest_score = score
        best_rule = rule

print(f"ნაპოვნი შესაბამისი წესი (ქულა {highest_score:.4f}):\n-> {best_rule}\n")

# 3. Generation (RAG): ვაწვდით ნაპოვნ კონტექსტს Gemini-ს
prompt = f"""
უპასუხე მომხმარებლის კითხვას მხოლოდ მოცემულ კონტექსტზე დაყრდნობით.

კონტექსტი:
{best_rule}

კითხვა:
{user_question}
"""

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=prompt
)

print("Gemini-ს პასუხი (RAG):")
print(response.text)
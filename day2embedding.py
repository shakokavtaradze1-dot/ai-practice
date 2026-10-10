import os
import math
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text: str) -> list:
    """ტექსტს გარდაქმნის რიცხვით ვექტორად (Embedding)."""
    response = client.models.embed_content(
        model="models/gemini-embedding-001",
        contents=text
    )
    return response.embeddings[0].values

def cosine_similarity(v1: list, v2: list) -> float:
    """ითვლის მსგავსებას ორ ვექტორს შორის (0-დან 1-მდე)."""
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_v1 = math.sqrt(sum(a * a for a in v1))
    norm_v2 = math.sqrt(sum(b * b for b in v2))
    return dot_product / (norm_v1 * norm_v2)

# სატესტო დოკუმენტები
doc1 = "BMW M8 Competition has a twin-turbo V8 engine and 617 HP."
doc2 = "Ferrari SF90 is a hybrid Italian supercar with extreme speed."
doc3 = "Baking an Italian pizza requires flour, water, yeast, and high heat."

# მომხმარებლის კითხვა
user_query = "What is the horsepower of BMW?"

print("ვქმნით ემბედინგებს და ვითვლით მსგავსებას...\n")

query_vec = get_embedding(user_query)
print(f"ვექტორის ზომა (განზომილება): {len(query_vec)} რიცხვი\n")

docs = [doc1, doc2, doc3]
for idx, doc in enumerate(docs, 1):
    doc_vec = get_embedding(doc)
    score = cosine_similarity(query_vec, doc_vec)
    print(f"დოკუმენტი {idx}: \"{doc}\"")
    print(f"--> მსგავსების ქულა (Cosine Similarity): {round(score, 4)}\n")
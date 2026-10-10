import os
import math
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# მათემატიკური ფუნქცია ორი ვექტორის შესადარებლად (Cosine Similarity)
def cosine_similarity(v1, v2):
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_v1 = math.sqrt(sum(a * a for a in v1))
    norm_v2 = math.sqrt(sum(b * b for b in v2))
    return dot_product / (norm_v1 * norm_v2)

# დამხმარე ფუნქცია ემბედინგის მისაღებად
def get_embedding(text: str):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return response.embeddings[0].values

# 1. მომხმარებლის კითხვა
query = "მინდა ანგარიშიდან ფულის განაღდება"

# 2. ორი განსხვავებული ტექსტი ჩვენს ბაზაში
text_similar = "როგორ გავიტანო მოგებული თანხა ჩემი ბალანსიდან?"
text_different = "საქართველოს ნაკრებმა ფეხბურთში გაიმარჯვა"

print(f"ძირითადი ფრაზა: '{query}'\n")

# ვქმნით ვექტორებს
v_query = get_embedding(query)
v_similar = get_embedding(text_similar)
v_different = get_embedding(text_different)

# ვითვლით მსგავსებას
score_similar = cosine_similarity(v_query, v_similar)
score_different = cosine_similarity(v_query, v_different)

print(f"შედარება 1: '{text_similar}'")
print(f"-> მსგავსების ქულა: {score_similar:.4f} (მაღალი მსგავსება)\n")

print(f"შედარება 2: '{text_different}'")
print(f"-> მსგავსების ქულა: {score_different:.4f} (დაბალი მსგავსება)")
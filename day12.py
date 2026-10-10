import os
import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def get_embedding(text: str):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return response.embeddings[0].values

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="error_codes_kb")

# 1. დოკუმენტები ტექნიკური შეცდომების შესახებ
documents = [
    "შეცდომა 404 ნიშნავს, რომ გვერდი ვერ მოიძებნა სერვერზე.",
    "შეცდომა 500 მიუთითებს სერვერის შიდა გაურკვეველ პრობლემაზე.",
    "შეცდომა 503 ნიშნავს, რომ სერვერი დროებით მიუწვდომელია გადატვირთვის ან პროფილაქტიკის გამო."
]

ids = ["err_404", "err_500", "err_503"]

print("ვინახავთ დოკუმენტებს ვექტორულ ბაზაში...")
embeddings = [get_embedding(doc) for doc in documents]
collection.add(ids=ids, embeddings=embeddings, documents=documents)
print("ბაზა მზადაა!\n")

user_query = "რა ვქნა როცა მიწერს error 503?"
print(f"მომხმარებლის კითხვა: '{user_query}'\n")

# 2. Retrieval: ამოვიღოთ ტოპ 2 დოკუმენტი სემანტიკურად
query_vector = get_embedding(user_query)
results = collection.query(
    query_embeddings=[query_vector],
    n_results=2
)

retrieved_docs = results["documents"][0]
print("ChromaDB-ს მიერ ამოღებული კანდიდატები:")
for idx, doc in enumerate(retrieved_docs, start=1):
    print(f" {idx}. {doc}")
print()

# 3. Reranking (ხელახალი შეფასება Gemini-ს მეშვეობით)
rerank_prompt = f"""
გააანალიზე მომხმარებლის კითხვა და მოცემული დოკუმენტების სია.
აარჩიე მხოლოდ ერთი, ყველაზე რელევანტური დოკუმენტი და დააბრუნე მხოლოდ ის ტექსტი, ყოველგვარი დამატებითი კომენტარის გარეშე.

კითხვა: {user_query}

დოკუმენტები:
1. {retrieved_docs[0]}
2. {retrieved_docs[1]}
"""

rerank_response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=rerank_prompt
)

best_reranked_doc = rerank_response.text.strip()
print(f"Reranking-ის შემდეგ შერჩეული საუკეთესო დოკუმენტი:\n-> {best_reranked_doc}\n")

# 4. საბოლოო პასუხის გენერაცია (Generation)
final_prompt = f"""
უპასუხე მომხმარებლის კითხვას მოცემულ კონტექსტზე დაყრდნობით მეგობრულად.
კონტექსტი: {best_reranked_doc}
კითხვა: {user_query}
"""

final_response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=final_prompt
)

print("Gemini-ს საბოლოო პასუხი:")
print(final_response.text)
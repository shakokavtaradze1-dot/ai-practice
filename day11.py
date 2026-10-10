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
collection = chroma_client.create_collection(name="upgaming_advanced")

# 1. წარმოვიდგინოთ დიდი ტექსტისგან მიღებული პატარა ნაწილები (Chunks)
# თითოეულს ვამატებთ მეტამონაცემებს (metadatas)
chunks = [
    "თანხის გატანის საკომისიო ბანკის ბარათზე შეადგენს 1%-ს.",
    "კრიპტოვალუტით თანხის გატანა სრულიად უფასოა და არ აქვს საკომისიო.",
    "VIP მომხმარებლებს ერიცხებათ 10%-იანი ქეშბექი ყოველ ორშაბათს."
]

metadatas = [
    {"category": "payments", "type": "fiat"},
    {"category": "payments", "type": "crypto"},
    {"category": "bonuses", "type": "vip"}
]

ids = ["chunk_1", "chunk_2", "chunk_3"]

print("ვაგენერირებთ ემბედინგებს და ვინახავთ მეტამონაცემებთან ერთად...")
embeddings = [get_embedding(chunk) for chunk in chunks]

collection.add(
    ids=ids,
    embeddings=embeddings,
    documents=chunks,
    metadatas=metadatas
)
print("მონაცემები შენახულია!\n")

# 2. მომხმარებლის კითხვა
user_query = "რა საკომისიოა თანხის გატანაზე?"
query_vector = get_embedding(user_query)

# 3. ძებნა მეტამონაცემების ფილტრით (Metadata Filtering):
# ვეძებთ მხოლოდ იმ ჩანაწერებში, სადაც category == "payments" და type == "crypto"
print("ვეძებთ მხოლოდ კრიპტოს გადახდების წესებში (Metadata Filter: type == crypto)...")

results = collection.query(
    query_embeddings=[query_vector],
    n_results=1,
    where={"type": "crypto"}  # აი აქ იფილტრება მეტამონაცემით!
)

retrieved_chunk = results["documents"][0][0]
print(f"ნაპოვნი შედეგი:\n-> {retrieved_chunk}\n")

# 4. RAG Generation
prompt = f"""
უპასუხე კითხვას მოცემულ კონტექსტზე დაყრდნობით.
კონტექსტი: {retrieved_chunk}
კითხვა: {user_query}
"""

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=prompt
)

print("Gemini-ს პასუხი:")
print(response.text)
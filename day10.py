import os
import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# 1. დამხმარე ფუნქცია Gemini-ით ემბედინგის მისაღებად
def get_embedding(text: str):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return response.embeddings[0].values

# 2. ვექტორული ბაზის (ChromaDB) ინიციალიზაცია მეხსიერებაში
chroma_client = chromadb.Client()

# ვქმნით კოლექციას (როგორც ცხრილი SQL-ში)
collection = chroma_client.create_collection(name="upgaming_faq")

# 3. დოკუმენტები, რომლებიც გვინდა ბაზაში შევინახოთ
documents = [
    "თანხის გატანის მინიმალური ლიმიტი შეადგენს 20 ლარს, მაქსიმალური კი 5000 ლარია.",
    "პაროლის აღსადგენად დააჭირეთ ღილაკს 'დაგავიწყდათ პაროლი?' ავტორიზაციის გვერდზე.",
    "ფსონის გაუქმება შესაძლებელია მხოლოდ მატჩის დაწყებამდე 10 წუთით ადრე."
]

doc_ids = ["doc_1", "doc_2", "doc_3"]

print("ვაგენერირებთ ემბედინგებს და ვინახავთ ChromaDB-ში...")

# თითოეულ დოკუმენტს ვაქცევთ ვექტორად
embeddings = [get_embedding(doc) for doc in documents]

# ვინახავთ ChromaDB-ში (ტექსტი, მისი ვექტორი და ID)
collection.add(
    ids=doc_ids,
    embeddings=embeddings,
    documents=documents
)

print("მონაცემები წარმატებით შეინახა ბაზაში!\n")

# 4. Semantic Search ChromaDB-ის დახმარებით (Retrieval)
user_query = "როგორ დავიბრუნო ჩემი პაროლი?"
print(f"მომხმარებლის კითხვა: '{user_query}'")

query_vector = get_embedding(user_query)

# ChromaDB თვითონ ითვლის მსგავსებას და აბრუნებს n_results საუკეთესო შედეგს
results = collection.query(
    query_embeddings=[query_vector],
    n_results=1
)

retrieved_doc = results["documents"][0][0]
print(f"\nChromaDB-მ იპოვა ყველაზე ახლო დოკუმენტი:\n-> {retrieved_doc}\n")

# 5. RAG: Augment & Generate
prompt = f"""
უპასუხე მომხმარებლის კითხვას მოცემულ კონტექსტზე დაყრდნობით.

კონტექსტი:
{retrieved_doc}

კითხვა:
{user_query}
"""

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=prompt
)

print("Gemini-ს პასუხი:")
print(response.text)
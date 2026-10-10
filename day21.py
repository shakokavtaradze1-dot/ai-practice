import os
import chromadb
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# 1. API კლიენტის ინიციალიზაცია
client = genai.Client()

# 2. ChromaDB ვექტორული ბაზის გამართვა (მეხსიერებაში)
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="auto_service_knowledge")

# 3. დოკუმენტების ბაზაში ჩაწერა
documents = [
    "BMW M8 Gran Coupe-ს ძრავის ზეთის რეკომენდებული მოცულობაა 9.5 ლიტრი, სპეციფიკაცია 0W-30 LL-12 FE. გამოცვლა ყოველ 8,000 კმ-ზე.",
    "სამუხრუჭე ხუნდების ცვეთის მაჩვენებელი: თუ ხუნდის სისქე 3 მმ-ზე ნაკლებია, საჭიროა დაუყოვნებლივი შეცვლა.",
    "ძრავის ზეთის შეცვლის სრული სერვისის ღირებულება BMW M სერიის მოდელებზე შეადგენს 450 ლარს (მასალები და სამუშაო).",
    "სავალი ნაწილის დიაგნოსტიკა უფასოა ნებისმიერი ზეთის ან ხუნდების სერვისის შეკვეთისას.",
]

metadatas = [
    {"category": "engine", "model": "BMW M8"},
    {"category": "brakes", "model": "universal"},
    {"category": "pricing", "model": "BMW M"},
    {"category": "promo", "model": "universal"},
]

ids = ["doc_1", "doc_2", "doc_3", "doc_4"]

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)
print("ChromaDB: მონაცემები წარმატებით ჩაიწერა ვექტორულ ბაზაში.\n")


# 4. RAG ძებნის ფუნქცია (Retrieval)
def retrieve_context(query: str, n_results: int = 3) -> str:
    """ეძებს სემანტიკურად ყველაზე ახლოს მდგომ ჩანქებს ChromaDB-ში."""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    retrieved_chunks = results["documents"][0]
    
    # ვბეჭდავთ, რომ დავინახოთ რა იპოვა ბაზამ
    print(f"\n[DEBUG: ბაზიდან ამოღებული ინფორმაცია]:")
    for idx, chunk in enumerate(retrieved_chunks, 1):
        print(f"  {idx}. {chunk}")
    print("-" * 50)
    
    return "\n---\n".join(retrieved_chunks)


# 5. მეხსიერება და ჩატის ციკლი (Sliding Window)
chat_history = []
MAX_HISTORY_TURNS = 4

system_instruction = (
    "შენ ხარ პროფესიონალი ავტო-ასისტენტი. "
    "უპასუხე მკაცრად მხოლოდ მიწოდებულ კონტექსტზე დაყრდნობით. "
    "თუ ინფორმაცია კონტექსტში არ წერია, პირდაპირ თქვი: 'არ მაქვს ზუსტი ინფორმაცია' და არ გამოიგონო."
)

print("AI ავტოსერვისის ბოტი მზადაა! (გასასვლელად აკრიფე 'exit')\n")

while True:
    user_input = input("მომხმარებელი: ").strip()
    if not user_input:
        continue
    if user_input.lower() in ["exit", "quit", "გასვლა"]:
        print("ნახვამდის!")
        break

    # 1. კონტექსტის ამოღება (Retrieval)
    context = retrieve_context(user_input, n_results=3)

    # 2. პრომპტის გამდიდრება (Augmentation)
    augmented_prompt = f"""კონტექსტი ბაზიდან:
{context}

მომხმარებლის შეკითხვა:
{user_input}"""

    # 3. ისტორიის მომზადება (Sliding Window)
    current_contents = []
    for turn in chat_history[-MAX_HISTORY_TURNS:]:
        current_contents.append(turn)

    current_contents.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=augmented_prompt)]
        )
    )

    # 4. გენერაცია (Generation)
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=current_contents,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.1
        )
    )

    bot_reply = response.text
    print(f"\nბოტი: {bot_reply}\n" + "=" * 50 + "\n")

    # 5. ისტორიაში შენახვა
    chat_history.append(types.Content(role="user", parts=[types.Part.from_text(text=user_input)]))
    chat_history.append(types.Content(role="model", parts=[types.Part.from_text(text=bot_reply)]))
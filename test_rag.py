import os
import chromadb
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()
chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(name="auto_service_knowledge")

documents=[
    "BMW M8 Gran Coupe-ს ძრავის ზეთის რეკომენდებული მოცულობაა 9.5 ლიტრი, სპეციფიკაცია 0W-30 LL-12 FE. გამოცვლა ყოველ 8,000 კმ-ზე.",
    "ძრავის ზეთის შეცვლის სრული სერვისის ღირებულება BMW M სერიის მოდელებზე შეადგენს 450 ლარს (მასალები და სამუშაო).",
    "სავალი ნაწილის დიაგნოსტიკა უფასოა ნებისმიერი ზეთის ან ხუნდების სერვისის შეკვეთისას.",
]

metadatas=[
    {"category": "engine", "model": "BMW M8"},
    {"category": "pricing", "model": "BMW M"},
    {"category": "promo", "model": "universal"},
]

ids = ["doc_1", "doc_2", "doc_3"]

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

print("ChromaDB: მონაცემები წარმატებით ჩაიწერა ვექტორულ ბაზაში.\n")

def retrieve_context(query: str, n_results: int = 3) -> str:
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    retrieved_chunks = results["documents"][0]

    print("\n[DEBUG: ბაზრიდან ამოღებულია ინფორმაცია]:")
    for idx, chunk in enumerate(retrieved_chunks, 1):
        print(f"{idx}. {chunk}")
        print("-" * 50)

        return "\n---\n".join(retrieved_chunks)

  # 1. მეხსიერების ინიციალიზაცია
chat_history = []
MAX_HISTORY_TURNS = 4

# 2. სისტემური ინსტრუქცია (Grounding / ჰალუცინაციის პრევენცია)
system_instruction = (
    "შენ ხარ პროფესიონალი ავტო-ასისტენტი. "
    "უპასუხე მკაცრად მხოლოდ მიწოდებულ კონტექსტზე დაყრდნობით. "
    "თუ ინფორმაცია კონტექსტში არ წერია, პირდაპირ თქვი: 'არ მაქვს ზუსტი ინფორმაცია' და არ გამოიგონო."
)

print("AI ავტოსერვისის ბოტი მზადაა! (გასასვლელად აკრიფე 'exit')\n")

# 3. ჩატის უსასრულო ციკლი
while True:
    user_input = input("მომხმარებელი: ").strip()
    if not user_input:
        continue
    if user_input.lower() in ["exit", "quit", "გასვლა"]:
        print("ნახვამდის!")
        break

    # R: Retrieval - ბაზიდან კონტექსტის ამოღება
    context = retrieve_context(user_input, n_results=3)

    # A: Augmentation - კითხვისა და კონტექსტის გაერთიანება
    augmented_prompt = f"""კონტექსტი ბაზიდან:
{context}

მომხმარებლის შეკითხვა:
{user_input}"""

    # Sliding Window: ვიღებთ მხოლოდ ბოლო რამდენიმე შეტყობინებას
    current_contents = []
    for turn in chat_history[-MAX_HISTORY_TURNS:]:
        current_contents.append(turn)

    # ვამატებთ ახალ გამდიდრებულ შეტყობინებას
    current_contents.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=augmented_prompt)]
        )
    )

    # G: Generation - პასუხის მიღება მოდელისგან
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

    # მეხსიერების განახლება სუფთა კითხვით (კონტექსტის გარეშე)
    chat_history.append(types.Content(role="user", parts=[types.Part.from_text(text=user_input)]))
    chat_history.append(types.Content(role="model", parts=[types.Part.from_text(text=bot_reply)]))
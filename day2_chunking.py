def preprocess_text(text: str) -> str:
    """აშორებს ზედმეტ ხაზებს და ორმაგ სფეისებს."""
    cleaned = " ".join(text.split())
    return cleaned

def chunk_text(text: str, chunk_size: int = 150, overlap: int = 30) -> list:
    """ჭრის ტექსტს ფიქსირებულ ჩანქებად გადაფარვით (overlap)."""
    cleaned_text = preprocess_text(text)
    chunks = []
    start = 0
    total_length = len(cleaned_text)

    while start < total_length:
        end = start + chunk_size
        chunk = cleaned_text[start:end]
        chunks.append(chunk)

        # გადავდივართ წინ chunk_size-ს მინუს overlap ბიჯით
        start += (chunk_size - overlap)

    return chunks

# სატესტო დიდი ტექსტი (მაგალითად ავტომობილებისა და AI-ს შესახებ)
sample_document = """
The BMW M8 Competition features a 4.4-liter twin-turbocharged V8 engine delivering 617 horsepower.
It blends supercar-level performance with a luxury grand tourer chassis. 
In modern Applied AI engineering, Retrieval-Augmented Generation (RAG) is used to connect 
Large Language Models with proprietary documentation. Instead of fine-tuning the base weights, 
the system chunks knowledge bases into dense vectors, indexes them in a vector database like ChromaDB, 
and queries relevant snippets via cosine similarity before generating responses.
"""

# გავუშვათ ფუნქცია: chunk_size=120 სიმბოლო, overlap=25 სიმბოლო
text_chunks = chunk_text(sample_document, chunk_size=120, overlap=25)

print(f"სულ შეიქმნა {len(text_chunks)} ჩანქი:\n")
for index, ch in enumerate(text_chunks, 1):
    print(f"--- Chunk #{index} (სიგრძე: {len(ch)}) ---")
    print(f'"{ch}"\n')

    
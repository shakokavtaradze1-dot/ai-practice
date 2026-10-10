from google import genai

import os
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

text_to_check = "მე მქვია შაკო და ვემზადები Applied AI Engineer-ის პოზიციისთვის Upgaming-ში."

# 1. ტოკენების წინასწარ დათვლა (API გამოძახების გარეშე)
count_result = client.models.count_tokens(
    model="gemini-3-flash-preview",
    contents=text_to_check
)

print(f"ტექსტი: '{text_to_check}'")
print(f"ტოკენების რაოდენობა წინასწარ: {count_result.total_tokens}")

# 2. რეალური მოთხოვნის გაგზავნა და გამოყენებული ტოკენების მეტამონაცემების (Metadata) ნახვა
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=text_to_check
)

usage = response.usage_metadata
print("\n--- გამოყენებული ტოკენები (Usage Metadata) ---")
print(f"შეტანის ტოკენები (Prompt Tokens): {usage.prompt_token_count}")
print(f"პასუხის ტოკენები (Candidates Tokens): {usage.candidates_token_count}")
print(f"სულ დახარჯული ტოკენი (Total Tokens): {usage.total_token_count}")
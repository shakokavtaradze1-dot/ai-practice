import os
from typing import Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

# 1. გასაღების ჩატვირთვა გარემოდან (.env -> მეხსიერება)
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 2. ანკეტის (სქემის) განსაზღვრა Pydantic-ით
class CarServiceBooking(BaseModel):
    car_model: str
    service_type: str
    preferred_time: Optional[str] = None  # თუ მომხმარებელმა დრო არ თქვა, არ გაითიშოს!
    urgency_level: str                    # მაგ: "მაღალი", "საშუალო", "დაბალი"

# 3. არეული, ადამიანური ტექსტი კლიენტისგან (დრო საერთოდ არ უწერია!)
user_message = "სალამი, BMW M8 მყავს და ხუნდები მაქვს სასწრაფოდ შესაცვლელი, ხმა აქვს საშინელი."

# 4. გამოძახება Structured Output-ის მითითებით config-ში
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=user_message,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=CarServiceBooking,  # <--- აქ ვაბამთ Pydantic-ის კლასს
        temperature=0.1,                    # დაბალი ტემპერატურა მკაცრი სიზუსტისთვის
    ),
)

# 5. პასუხის მიღება და ველებზე წვდომა
print("მოდელის დაგენერირებული სუფთა JSON:")
print(response.text)

# JSON ტექსტი ვაქციოთ რეალურ პითონის ობიექტად
booking = CarServiceBooking.model_validate_json(response.text)

print("\n--- პითონის ობიექტიდან ამოღებული მონაცემები ---")
print("მოდელი:", booking.car_model)
print("სერვისი:", booking.service_type)
print("დრო:", booking.preferred_time)
print("სისწრაფე:", booking.urgency_level)
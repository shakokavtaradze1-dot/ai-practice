import json
from os import name
import os
from turtle import speed
import random
import time
import requests
from google import genai
from dotenv import load_dotenv
from google.genai.errors import ServerError

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model = "gemini-3.8-flash",
    contents = "მითხარი ერთი საინტერესო ფაქტი bmw m8-ზე ქართულად"
)

print(response.text)

print(f"ჩატვირთული API Key: {api_key}")




car_model = "bmw m8"

horsepower = 625

engine_liters =  4.4

is_fast = True

speed = 120

if speed > 100:
    print("ძალიან სწრაფად მიდიხარ")
elif speed > 60:
    print("საშუალო სიჩქარით მიდიხარ") 
else:
    print("ნაკლებად სწრაფად მიდიხარ")


cars = ["BMW M8", "Audi RS7", "Mercedes-AMG GT"]

print(cars[0])
print(cars[1])

cars.append("Porsche 911")
cars.remove("Audi RS7") #saxelit washla winaswar ro vici saxeli
cars.pop(0)

print(cars)

for car in cars:
    print(f"მომწონს მოდელი: {car}")


car = {
   "brand": "BMW",
   "model": "m8",
   "hp": 625,
   "price": 130000
}

car["color"] = "black"
car["hp"] = 750

print(f"მოდელი არის {car['brand']} და აქვს {car['hp']} ცხენის ძალა")

print(car)

cars = [
    {"brand": "BMW", "model": "M8", "hp": 625}, 
    {"brand": "Audi", "model": "RS7", "hp": 600},
    {"brand": "Mercedes-AMG", "model": "GT", "hp": 577}
]

for c in cars:
    print(f"{c['brand']} {c['model']}-ს აქვს {c['hp']} ცხენის ძალა")


    women = [
        {"name": "maria", "age": 30},
        {"name": "ana", "age": 25},
        {"name": "nini", "age": 21}
    ]


for w in women:
    print(f"{w['name']} არის {w['age']} წლის")




garage = [
    {"model": "BMW M8", "hp": 625, "price": 130000},
    {"model": "audi rs6", "hp": 600, "price": 120000}
]


garage.append({"model": "Mercedes-AMG GT", "hp": 577, "price": 140000})

for g in garage:
    info = f"{g['model']} {g['hp']} {g['price']}"

    if g['hp'] > 600:
        info = info + " -> ეს არის სუპერქარი"

    print(info)


def greet_driver(name, car_model):
    print(f" გამარჯობა {name}, შენი {car_model} მზად არის")

greet_driver("გიო", "BMW M8")
greet_driver("დათო", "Audi RS7")

def calculate_discount(price, discount_percent):
    discount_amount = price * (discount_percent / 100)
    final_price = price - discount_amount
    return final_price

m8_sale = calculate_discount(130000, 10)
rs6_sale = calculate_discount(120000, 15)

print(f"BMW M8-ის ფასდაკლებული ფასი: {m8_sale}")
print(f"Audi RS6-ის ფასდაკლებული ფასი: {rs6_sale}") 

def check_car_tier(model, hp):
    if hp >= 600:
        return f"{model} არის სუპერქარი"
    else:
        return f"{model} არ არის სუპერქარი"

print(check_car_tier("BMW M8", 625))
print(check_car_tier("Audi RS7", 600))
print(check_car_tier("Mercedes-AMG GT", 577))


cars = ["BMW M8", "Audi RS7", "Mercedes-AMG GT"]

random_car = random.choice(cars)

print(f"Randomly selected car: {random_car}")

print(f"sistema itvirteba")
time.sleep(2)
print(f"mzadaa")

horsepowers = [625, 450, 600, 300, 577, 617]

# List Comprehension:
supercars = [hp for hp in horsepowers if hp >= 600]

print(supercars)  


prompt = """
დამიბრუნე 3 სუპერქარის მონაცემი სუფთა JSON მასივის (array) სახით.
თითოეულ ობიექტს ჰქონდეს ველები: brand, model, horsepower.
მაგალითად: [{"brand": "BMW", "model": "M8", "horsepower": 617}]
"""

max_retries = 3
for attempt in range(max_retries):
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

        print("--- მიღებული სუფთა JSON ---")
        print(response.text)

        # JSON ტექსტს ვაქცევთ პითონის სია/ლექსიკონად:
        cars_data = json.loads(response.text)

        print("\n--- პითონის მიერ დამუშავებული ობიექტები ---")
        for car in cars_data:
            print(f"ბრენდი: {car['brand']} | მოდელი: {car['model']} | სიმძლავრე: {car['horsepower']} HP")

        break  # თუ წარმატებით შესრულდა, ციკლი წყდება

    except Exception as e:
        print(f"მცდელობა {attempt + 1} ჩაიშალა: {e}")
        if attempt < max_retries - 1:
            print("ველოდებით 4 წამს და ვცდით თავიდან...")
            time.sleep(4)
        else:
            print("ყველა მცდელობა ამოიწურა.")
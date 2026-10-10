class Car:
    # 1. კონსტრუქტორი: ანიჭებს საწყის მონაცემებს
    def __init__(self, brand, model, hp):
        self.brand = brand
        self.model = model
        self.hp = hp

    # 2. მეთოდი (ფუნქცია კლასის შიგნით):
    def describe(self):
        print(f"{self.brand} {self.model} - {self.hp} HP")

    # 3. მეთოდი შემოწმებით:
    def is_supercar(self):
        return self.hp >= 600

    # ვქმნით ორ დამოუკიდებელ ობიექტს (ინსტანციას):
car1 = Car("BMW", "M8", 625)
car2 = Car("Audi", "RS6", 591)

# ვიძახებთ მათ მეთოდებს:
car1.describe()  # BMW M8 - 625 HP
car2.describe()  # Audi RS6 - 591 HP

print(car1.is_supercar())  # True
print(car2.is_supercar())  # False
from kitty import db, Nutrient, User

# (self, item, kcal=0, fat=0, carbs=0, protein=0, user_id=1):
food1 = Nutrient('yogurt', 110,15,20,15,1)
food2 = Nutrient('smoothie', 400,15,50,35,1)

db.session.add(food1)
db.session.add(food2)
db.session.commit()

print(food1.id)
print(food2.id)

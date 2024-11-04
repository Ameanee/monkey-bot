import random

class Monkeys:
    def __init__ (self, db):
        self.db = db
        self.monkeys = {
            "basic monkey": {
                "health": 100,
                "damage": 10,
                "ability": None,
                "rarity": "common"
            }
        }
        
        chances = [
            ["basic monkey", 1]
        ]
        
        self.options, self.weights = []
        # set it up
        for chance in chances:
            self.options.append(chance[0])
            self.weights.append(chance[1])
    
    def new_monkey (self):
        type = random.choices(self.options, self.weights, k=1)[0]
    
        health = (random.randint(-50, 50) / 100) * self.monkeys[type]["health"]
        damage = (random.randint(-50, 50) / 100) * self.monkeys[type]["damage"]

        return self.db.new_monkey(type, health, damage)
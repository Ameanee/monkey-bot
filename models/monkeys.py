import random

class Monkeys:
    def __init__ (self, db):
        self.db = db
        self.monkeys = {
            "basic monkey": {
                "health": 100,
                "damage": 10,
                "ability": None,
                "rarity": "common",
                "description": "beta male monkey"
            },
            "army monkey": {
                "health": 130,
                "damage": 20,
                "ability": None,
                "rarity": "uncommon",
                "description": "has to fight :sob:"
            },
            "hood monkey": {
                "health": 100,
                "damage": 15,
                "ability": None,
                "rarity": "uncommon",
                "description": "free smurk"
            }
        }

        self.abilities = [
        ]
        
        chances = [
            ["basic monkey", 0.6],
            ["army monkey", 0.2],
            ["hood monkey", 0.2]
        ]
        
        self.options = []
        self.weights = []
        # set it up
        for chance in chances:
            self.options.append(chance[0])
            self.weights.append(chance[1])

    def random_monkey (self):
        return random.choices(self.options, self.weights, k=1)[0]
    
    def new_monkey (self, type):
        health = self.monkeys[type]["health"] + int((random.randint(-50, 50) / 100) * self.monkeys[type]["health"])
        damage = self.monkeys[type]["damage"] + int((random.randint(-50, 50) / 100) * self.monkeys[type]["damage"])

        return self.db.new_monkey(type, health, damage)
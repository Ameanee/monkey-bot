import random

class Monkeys:
    def __init__ (self, db):
        self.db = db
        self.monkeys = {
            "basic monkey": {
                "health": 100,
                "damage": 10,
                "ability": [],
                "rarity": "common",
                "description": "beta male monkey"
            },
            "albino basic monkey": {
                "health": 200,
                "damage": 20,
                "ability": [0],
                "rarity": "common",
                "description": "andrew tate"
            },
            "army monkey": {
                "health": 130,
                "damage": 20,
                "ability": [],
                "rarity": "uncommon",
                "description": "has to fight :sob:"
            },
            "albino army monkey": {
                "health": 260,
                "damage": 40,
                "ability": [0],
                "rarity": "uncommon",
                "description": "did we find nukes in iraq?"
            },
            "hood monkey": {
                "health": 100,
                "damage": 15,
                "ability": [],
                "rarity": "uncommon",
                "description": "free smurk"
            },
            "albino hood monkey": {
                "health": 200,
                "damage": 30,
                "ability": [0],
                "rarity": "uncommon",
                "description": "pulled over and shot, like damn"
            },
            "cyborg monkey": {
                "health": 250,
                "damage": 125,
                "ability": [1],
                "rarity": "rare",
                "description": "elon musk vision!"
            },
            "albino cyborg monkey": {
                "health": 500,
                "damage": 250,
                "ability": [0, 1],
                "rarity": "rare",
                "description": "elon musk vision!"
            },
            "dj monkey": {
                "health": 200,
                "damage": 0,
                "ability": [2],
                "rarity": "rare",
                "description": "metro boomin be boomin"
            },
            "albino dj monkey": {
                "health": 400,
                "damage": 0,
                "ability": [0, 2],
                "rarity": "rare",
                "description": "eminem?"
            },
            "ninja monkey": {
                "health": 150,
                "damage": 100,
                "ability": [3],
                "rarity": "rare"
            },
            "albino ninja monkey": {
                "health": 300,
                "damage": 200,
                "ability": [0, 3],
                "rarity": "rare"
            },
            "gorilla": {
                "health": 1000,
                "damage": 500,
                "ability": [],
                "rarity": "legendary",
                "description": "the same thing?"
            },
            "albino gorilla": {
                "health": 2000,
                "damage": 1000,
                "ability": [0],
                "rarity": "legendary",
                "description": "1 in 1000!"
            }
        }

        self.abilities = [
            {
                "name": "White Privelige",
                "description": "Deal double damage against non-albino monkeys",
                "type": "modifier",
                "mult": 1,
                "works": "non-albino",
                "atk_type": "physical",
                "cooldown": 0
            },
            {
                "name": "Mechanical",
                "description": "Physical attacks deal 50% less damage or 50 less damage depending on which is smaller",
                "type": "defense",
                "cooldown": 0
            },
            {
                "name": "Dancin",
                "description": "Makes another monkey dance for 3 rounds (paralyze them)",
                "type": "stun",
                "cooldown": 2
            },
            {
                "name": "Sneaky",
                "description": "Has a 30% of dodging all attacks",
                "type": "dodge",
                "cooldown": 0
            }
        ]
        
        chances = [
            ["basic monkey", 0.5],
            ["army monkey", 0.16],
            ["hood monkey", 0.16],
            ["cyborg monkey", 0.075],
            ["dj monkey", 0.075],
            ["ninja monkey", 0.075],
            ["gorilla", 0.01]
        ]
        
        self.options = []
        self.weights = []
        # set it up
        for chance in chances:
            self.options.append(chance[0])
            self.weights.append(chance[1])

    def random_monkey (self):
        monkey = random.choices(self.options, self.weights, k=1)[0]
        if (random.randint(1, 1000) == 500):
            return "albino " + monkey
        return monkey
    
    def new_monkey (self, type, id: str):
        health = self.monkeys[type]["health"] + int((random.randint(-50, 50) / 100) * self.monkeys[type]["health"])
        damage = self.monkeys[type]["damage"] + int((random.randint(-50, 50) / 100) * self.monkeys[type]["damage"])

        return self.db.new_monkey(type, health, damage, id)
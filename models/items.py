class Items:
    def __init__ (self):
        self.shop = {
            "banana": {
                "price": 15,
                "description": "heals monkey! +1 health"
            },
            "metal armor": {
                "price": 100,
                "description": "armor! +20 health when used in battle"
            }
        }

        self.items = {
            "banana": {},
            "metal armor": {},
        }
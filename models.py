import json

class Coins:
    def __init__(self):
        try:
            with open("coins.json", "r") as f:
                self.coins = json.load(f)
        except FileNotFoundError:
            self.coins = ["error"]

    def all(self):
        return self.coins

    def get(self, id):
        coin = [coin for coin in self.all() if coin['id'] == id]
        if coin:
            return coin[0]
        return []
    
    def create(self, data):
        if 'csrf_token' in data:
            data.pop('csrf_token')
        self.coins.append(data)
        if len(self.coins) > 1:    
            self.coins[-1]["id"] = self.coins[-2]["id"] + 1
        else:
            self.coins[-1]["id"] = 1
        self.save_all()

    def delete(self, id):
        coin = self.get(id)
        if coin:
            self.coins.remove(coin)
            self.save_all()
            return True
        return False

    def save_all(self):
        with open("coins.json", "w") as f:
            json.dump(self.coins, f)

    def update(self, id, data):
        coin = self.get(id)
        if coin:
            index = self.coins.index(coin)
            if 'csrf_token' in data:
                data.pop('csrf_token')
            id = self.coins[index]["id"]
            data["id"] = id
            self.coins[index] = data
            self.save_all()
            return True
        return False

coins = Coins()
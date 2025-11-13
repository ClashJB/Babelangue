import random

#classes
class Player:
    def __init__(self, skilldice, staminadices, luckdice, items = ["sword", "backpack"], provisions = {}):
        self.skill = skilldice + 6
        self.stamina = staminadices + 12
        self.luck = luckdice + 6
        self.items = items
        self.provisions = provisions

    def test_luck(self):
        self.luck = self.luck - 1
        if 2 * random.randint(1, 6) >= self.luck + 1:
            print("You're Lucky!")
            return 4
        else:
            print("Unlucky")
            return 1


class Monster:
    def __init__(self, skill, stamina):
        self.skill = skill
        self.stamina = stamina
        self.damage = self.skill + 2 * random.randint(1, 6)

def dice():
    return random.randint(1, 6)




#starting adventure
provisions = {"meals": 10, "luck potion": 1}
spieler = Player(6, 8, 1, provisions=provisions)
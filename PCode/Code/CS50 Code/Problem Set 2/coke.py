amount_due = 50
valid_coins = (5, 10, 25, 50)

while amount_due > 0:
    print(f"Amount Due: {amount_due}")
    coin = int(input("Insert coin: "))

    if coin in valid_coins:
        amount_due = amount_due - coin

amount_owed = -amount_due

print(f"Amnount Owed: {amount_owed}")
def main():
    user_time = input("What time is it?")
    user_time = convert(user_time)

    if 7 <= user_time <= 8:
        print("breakfast time")
    elif 12 <= user_time <= 13:
        print("lunch time")
    elif 18 <= user_time <= 19:
        print ("dinner time")

def convert(time):
    time = time.split(":")
    hours = int(time[0])
    minutes = int(time[1])
    return hours + (minutes / 60)

main()
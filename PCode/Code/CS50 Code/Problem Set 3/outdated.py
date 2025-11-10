months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]



while True:
    date = input("Date: ")
    try:
        if "/" in date:
            m, d, y = date.split("/")
            m, d, y = int(m), int(d), int(y)
            if 1 <= m <= 12 and 1 <= d <= 31:
                print(f"{y:04}-{m:02}-{d:02}")
                break

        elif (date[0].isalpha):
            md, y = date.split(",")
            y = int(y.strip())
            m, d = md.split(" ")
            d = int(d)

            if m in months:
                m = months.index(m) + 1

            if 1 <= d <= 31:
                print(f"{y:04}-{m:02}-{d:02}")
                break
    except (ValueError, IndexError):
        pass

    continue
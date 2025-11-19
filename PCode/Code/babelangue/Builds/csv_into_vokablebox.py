import csv

newdict = {}

file = input("File: ")
with open(file, "r", newline="") as oldfile:
    reader = csv.DictReader(oldfile)
    print(reader.fieldnames)

    question = reader.fieldnames[0]
    answer = reader.fieldnames[1]
    s1 = reader.fieldnames[3]
    s2 = reader.fieldnames[4]
    s3 = reader.fieldnames[5]
    p1 = reader.fieldnames[6]
    p2 = reader.fieldnames[7]
    p3 = reader.fieldnames[8]

    for row in oldfile:
        newdict = {row[0]: f"{row[1]}\n{s1} --> {row[3]}\n{s2} --> {row[4]}"}
        

    with open(f"{file}.csv", "w", newline="") as newfile:
        writer = csv.DictWriter(newfile, fieldnames=(question, answer))

        writer.writerow()
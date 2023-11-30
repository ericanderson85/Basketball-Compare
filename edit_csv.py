import csv

with open('players.csv', "r", newline='', errors="ignore") as csvfile:
    reader = csv.DictReader(csvfile)
    rows = []
    for row in reader:
        rows.append([row["Name"].lower(), row["ID"], int(row["Weight"])])

rows.sort(key=lambda x: x[2], reverse=True)


with open('players.csv', "w", newline='', errors="ignore") as csvfile:
    writer = csv.writer(csvfile)
    for r in rows:
        writer.writerow(r)

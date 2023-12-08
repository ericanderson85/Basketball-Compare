import csv
import random


def read_csv():
    file_name = 'players.csv'
    with open(file_name, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        ids = []
        weights = []
        for row in reader:
            ids.append(row['ID'])
            weights.append(float(row['Weight']))
        return ids, weights


def get_random_player():
    file_name = 'players.csv'
    ids, weights = read_csv()
    return random.choices(ids, weights=weights, k=1)[0]


if __name__ == "__main__":
    print(get_random_player())

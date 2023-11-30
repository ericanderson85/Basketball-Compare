import os
import csv
import requests

nba_ids = set()
cache = os.listdir("cache/")
for json_file in cache:
    nba_ids.add(json_file[:-5])

matched_ids = {}

with open('NBA_Player_IDs.csv', newline='', errors="ignore") as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        if row['NBAName'] in nba_ids:
            matched_ids[row['NBAID']] = row['BBRefID']

print(matched_ids)

cached_pngs = os.listdir("static/images/")
downloaded_ids = set()
for png in cached_pngs:
    downloaded_ids.add(png[:-4])

print(downloaded_ids)


successful_ids = []
for nbacom_id in matched_ids.keys():
    bbr_id = matched_ids[nbacom_id]
    if bbr_id != "NA" and not nbacom_id in downloaded_ids:
        successful_ids.append(nbacom_id)

print(successful_ids)

count = 0
for id in successful_ids:
    bbr_suc = matched_ids[id]
    image_url = f"https://www.basketball-reference.com/req/202106291/images/headshots/{
        bbr_suc}.jpg"
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(f"static/images/{id}.jpg", "wb") as jpg_file:
            jpg_file.write(response.content)
            print(f"Downloaded {id}.jpg")
    else:
        print(f"Failed to download {id}.jpg")
    print(count)
    count += 1

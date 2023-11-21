import os
import requests

count = 0
for file in os.listdir("cache/")[2350:]:
    if file[-5:] == ".json":
        image_url = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{
            file[:-5]}.png"
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(f"images/{file[:-5]}.png", "wb") as png_file:
                png_file.write(response.content)
                print(f"Downloaded {file[:-5]}.png")
                print(count)
        else:
            print(f"Failed to download {file[:-5]}.png")
    count += 1

print("Download complete.")

import json
import re
import seaborn as sns
import matplotlib.pyplot as plt


all_scraped = []
with open("results.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)
        if "error" in data:
            continue
        all_scraped.append(data)


for row in all_scraped:
    row["contents"] = re.sub(r"\s+", r" ", row["contents"])
    row["contents"] = row["contents"].strip()

blacklist = [
    "https://duck.com",
]

all_scraped = list(filter(lambda row: row["contents"], all_scraped))
all_scraped = list(filter(lambda row: "mail" not in row["website_name"], all_scraped))
all_scraped = list(
    filter(lambda row: row["website_name"] not in blacklist, all_scraped)
)
all_scraped = list(
    filter(lambda row: len(row["contents"].split(" ")) <= 1000, all_scraped)
)
all_scraped = list(
    filter(lambda row: len(row["contents"].split(" ")) > 100, all_scraped)
)
all_scraped = list(filter(lambda row: len(row["contents"]) <= 6000, all_scraped))

words = list(map(lambda row: len(row["contents"].split(" ")), all_scraped))
sns.histplot(words)
plt.savefig("histogram_words.png")

plt.clf()
characters = list(map(lambda row: len(row["contents"]), all_scraped))
sns.histplot(characters)
plt.savefig("histogram_characters.png")

print(len(all_scraped))
with open("all_scraped.json", "w") as f:
    json.dump(all_scraped, f, indent=2)

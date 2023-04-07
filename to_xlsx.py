import pandas as pd

df = pd.read_json("chat_results.json")
df = df.drop_duplicates(subset=["website_name"])
df = df.sort_values(by="website_name")
df.to_excel("chat_results.xlsx", index=False)

import json

chats = []
with open("chat_results.jsonl") as f:
    for line in f:
        chats.append(json.loads(line))

with open("flat_ideas.txt", "w") as f:
    for chat in chats:
        ideas = chat["ideas"]
        f.write(f"{ideas}\n")
        f.write("-" * 80)
        f.write("\n")

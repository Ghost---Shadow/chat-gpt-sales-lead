import json
import openai
from tqdm import tqdm

with open("openai_key") as f:
    openai_key = f.read().strip()
    openai.api_key = openai_key

with open("all_scraped.json") as f:
    all_scraped = json.load(f)

RESULT_FILE_NAME = "chat_results.jsonl"
open(RESULT_FILE_NAME, "w").close()

MODEL = "gpt-3.5-turbo"

for row in tqdm(all_scraped[:5]):
    website_name = row["website_name"]
    contents = row["contents"]
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"Here is an website with URL {website_name}.\nHere are the contents of the website {contents}. What does this website do?",
        },
    ]
    result = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
    )
    description_response = result["choices"][0]["message"]
    messages.append(description_response)
    messages.append(
        {
            "role": "user",
            "content": "List 5 ideas how a large language model finetuned on question answering tasks can benefit their company.",
        }
    )
    result = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
    )
    ideas_response = result["choices"][0]["message"]
    with open(RESULT_FILE_NAME, "a") as f:
        f.write(
            json.dumps(
                {
                    "website_name": website_name,
                    "description": description_response["content"],
                    "ideas": ideas_response["content"],
                }
            )
            + "\n"
        )

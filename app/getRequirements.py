import os
import dotenv
from huggingface_hub import InferenceClient

dotenv.load_dotenv(r'C:\Users\mmati\OneDrive\Documents\GitHub\ScholarshipSorter\n.env')
client = InferenceClient(
    provider="novita",
    api_key=os.environ["HF_TOKEN"],
)

"""def get_Requirements():

    completion = client.chat.completions.create(
       model="meta-llama/Llama-3.1-8B-Instruct",
       messages=[
           {
                "role": "user",
             "content": "What is the capital of France?"
          }
         ],
)"""
    
messagesG = []
while True:
    msg = input("User: \n")
    if msg=='exit()': break
    messagesG.append(
        {
            "role": "user",
            "content": msg
        }
    )
    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=messagesG
    )
    messagesG.append(completion.choices[0].message)
    print(f'AI: \n{completion.choices[0].message.content}')

print(messagesG)

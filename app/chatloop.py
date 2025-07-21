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
def chatLoop(message, messageHistory: list = []):
    messageHistory.append(
        {
            "role": "user",
            "content": message
        }
    )
    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=messageHistory
    )
    messageHistory.append(completion.choices[0].message)
    return completion.choices[0].message.content


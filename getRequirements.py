import os
import dotenv
from huggingface_hub import InferenceClient
dotenv.load_dotenv(".env")
token = os.environ["HF_TOKEN"]
client = InferenceClient(
    provider="novita",
    api_key=token,
)

# messagesG = []
# while True:
#     msg = input("User: \n")
#     if msg=='exit()': break
#     messagesG.append(
#         {
#             "role": "user",
#             "content": msg
#         }
#     )
#     completion = client.chat.completions.create(
#         model="meta-llama/Llama-3.1-8B-Instruct",
#         messages=messagesG
#     )
#     messagesG.append(completion.choices[0].message)
#     print(f'AI: \n{completion.choices[0].message.content}')


def get_filters(prompt):
    dynamic_prompt = """

    SYSTEM:
    You are a JSON extractor.  Take a natural‑language request about student filters and output **only** a JSON object whose keys are valid fields and whose values are the constraints.  Use comparison operators (">", ">=", "<", "<=", "=") for numeric fields, and exact strings for categorical fields.  Do **not** output any extra text or formatting.
    Your options for filtering data are as follows ["gpa", "race_group", "gender", "interests"]
    ONLY respond with these
    EXAMPLES:
    #1
    Input: "Find all students with GPA >= 3.5 who are Hispanic."
    Output: {"gpa": {">=": 3.5}, "race_group": "Hispanic"}

    #2
    Input: "Show me juniors interested in robotics clubs."
    Output: {"grade_level": 11, "extracurriculars": "Robotics"}

    #3
    Input: "Select students with SAT > 1400, female, and from Manhattan."
    Output: {"sat_score": {">": 1400}, "gender": "Female", "borough": "Manhattan"}

    NOW PROCESS:
    Input:
    """
    messagesG = [{
                "role": "user",
                "content": f"{dynamic_prompt} {prompt}/n Output:"
            }]

    completion = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=messagesG
        )
    messagesG.append(completion.choices[0].message)
    print(f'AI: \n{completion.choices[0].message.content}')

get_filters("I need a female asian student with a GPA greater than 3")

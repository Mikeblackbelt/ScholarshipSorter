import os
import dotenv
from huggingface_hub import InferenceClient
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json
import pandas as pd
import torch
dotenv.load_dotenv(".env")
token = os.environ["HF_TOKEN"]
client = InferenceClient(
    provider="novita",
    api_key=token,
)


model = AutoModelForSequenceClassification.from_pretrained('cross-encoder/ms-marco-MiniLM-L6-v2')
tokenizer = AutoTokenizer.from_pretrained('cross-encoder/ms-marco-MiniLM-L6-v2')


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
    Your options for filtering data are as follows ["gpa", "race_group", "gender", "interests","income"]
    ONLY respond with these
    EXAMPLES:
    #1
    Input: "Find all students with GPA >= 3.5 who are Hispanic."
    Output: {"gpa": {">": 3.5}, "race_group": "Hispanic"}

    #2
    Input: "Show me juniors interested in robotics clubs."
    Output: {"grade": 11, "extracurriculars": "Robotics"}

    #3
    Input: "Select students that are female and make less than 200,000 for an Environmental Scholarship"
    Output: {"gender": "F", "income": {"<": 200000}}

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
    response = completion.choices[0].message.content
    response = json.loads(response)
    print(response)
    return response


def check_similarity(target,student_info):
    features = tokenizer([target], [student_info],  padding=True, truncation=True, return_tensors="pt")
    model.eval()
    with torch.no_grad():
        scores = model(**features).logits
        if scores.item() > -5:
            return True
        else:
            return False



def filter_students(requirements):
    df = pd.read_csv("student_data.csv")
    for key,value in requirements.items():
        if key == "gender":
            df = df[df['Gender'] == value]
        if key == "grade":
            df = df[df['Grade'] == value]
        if key == "gpa":
            gpa_dict = value
            if list(gpa_dict.keys())[0] == ">":
                df = df[df['GPA'] > gpa_dict[">"]]
            elif list(gpa_dict.keys())[0] == "<":
                df = df[df['GPA'] < gpa_dict["<"]]
        if key == "income":
            income_dict = value
            if list(income_dict.keys())[0] == ">":
                df = df[df['Income'] > income_dict[">"]]
            elif list(income_dict.keys())[0] == "<":
                df = df[df['Income'] < income_dict["<"]]
    for key,value in requirements.items():
        if key == "race_group":
            drop_indexes = []
            for index, row in df.iterrows():
                student_race = row['Race']
                similarity_score = check_similarity(value,student_race)
                if similarity_score == False:
                    drop_indexes.append(index)
            df = df.drop(index=drop_indexes)

    print(df)
    return df


# def rank_students(df,requirements):
#         for key,value in requirements.items():
#             if key == "scholarship_description":


filters = get_filters("I need students that makes less than 200000 per year who are Caucasian")

filtered_students = filter_students(filters)
# ranked_students = rank_students(filtered_students,description)


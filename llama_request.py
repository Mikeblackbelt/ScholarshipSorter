import pandas as pd
import json
from huggingface_hub import InferenceClient
import dotenv
import os
dotenv.load_dotenv(".env")
token = os.environ["HF_TOKEN2"]
client = InferenceClient(
    provider="novita",
    api_key=token,
)

def service_score(df,chunk_size=5):
    scores = []
    student_infos = ""
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        student_infos = ""
        for index, row in chunk.iterrows():
            student_infos += f"{index}. {row['Service Description']}\n"
        dynamic_prompt2 = f"""
SYSTEM:
You are an AI assistant that evaluates student service activities based on how impressive or impactful they are for college scholarship applications.

Your job is to return **only float scores between 0 and 1**, one per service, in the order given.

INPUT:
1. A list of student service activity descriptions.

RULES:
- Output must contain **only float scores**, one per line, in the same order as the service list.
- Do **not** include any code, markdown, labels, explanations, or extra text.
- Scores must be between 0 and 1.
- Make sure to give every activity one score.

SCORING CRITERIA:
- Higher score for activities that show leadership, long-term commitment, real-world impact, or service to underserved communities.
- Medium score for participation in common or short-term service events.
- Lower score for vague, passive, or low-effort involvement.
- Do not reject or filter; just score quality.

EXAMPLE:

Student Service Descriptions (3):
1. Volunteered at local food bank every weekend for 2 years, helped organize food drives.
2. Participated in school clean-up day once.
3. Created a tutoring program for underprivileged middle schoolers in math and science.

Output:  
0.88
0.14
0.94

NOW ANSWER:
{student_infos}

Output:

            """
        messagesG = [{
                    "role": "user",
                    "content": dynamic_prompt2
                }]
        completion = client.chat.completions.create(
                model="meta-llama/Llama-3.1-8B-Instruct",
                messages=messagesG
            )
        messagesG.append(completion.choices[0].message)
        response = completion.choices[0].message.content
        response = response.split("\n")
        scores.extend(response)
    df['service_score'] = list(map(float, scores))
    print(df)




def course_rigor(df,chunk_size=5):
    scores = []
    student_infos = ""
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        student_infos = ""
        for index, row in chunk.iterrows():
            student_infos += f"{index}. {row['Service Description']}\n"
        dynamic_prompt2 = f"""
SYSTEM:
You are an AI assistant that evaluates student service activities based on how impressive or impactful they are for college scholarship applications.

Your job is to return **only float scores between 0 and 1**, one per service, in the order given.

INPUT:
1. A list of student service activity descriptions.

RULES:
- Output must contain **only float scores**, one per line, in the same order as the service list.
- Do **not** include any code, markdown, labels, explanations, or extra text.
- Scores must be between 0 and 1.
- Make sure to give every activity one score.

SCORING CRITERIA:
- Higher score for activities that show leadership, long-term commitment, real-world impact, or service to underserved communities.
- Medium score for participation in common or short-term service events.
- Lower score for vague, passive, or low-effort involvement.
- Do not reject or filter; just score quality.

EXAMPLE:

Student Service Descriptions (3):
1. Volunteered at local food bank every weekend for 2 years, helped organize food drives.
2. Participated in school clean-up day once.
3. Created a tutoring program for underprivileged middle schoolers in math and science.

Output:  
0.88
0.14
0.94

NOW ANSWER:
{student_infos}

Output:

            """
        messagesG = [{
                    "role": "user",
                    "content": dynamic_prompt2
                }]
        completion = client.chat.completions.create(
                model="meta-llama/Llama-3.1-8B-Instruct",
                messages=messagesG
            )
        messagesG.append(completion.choices[0].message)
        response = completion.choices[0].message.content
        response = response.split("\n")
        scores.extend(response)
    df['service_score'] = list(map(float, scores))
    print(df)



student_df = pd.read_csv("student_data.csv")
service_score(student_df, chunk_size=5)
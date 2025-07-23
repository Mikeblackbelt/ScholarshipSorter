import os
import dotenv
from huggingface_hub import InferenceClient
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json
import pandas as pd
import torch
dotenv.load_dotenv("n.env")
token = os.environ["HF_TOKEN"]
client = InferenceClient(
    provider="novita",
    api_key=token,
)

gdf = pd.read_csv("student_data.csv")


model = AutoModelForSequenceClassification.from_pretrained('cross-encoder/ms-marco-MiniLM-L6-v2')
tokenizer = AutoTokenizer.from_pretrained('cross-encoder/ms-marco-MiniLM-L6-v2')


def get_filters(prompt):
    dynamic_prompt = """

    SYSTEM:
    You are a JSON extractor.  Take a natural‑language request about student filters and output **only** a JSON object whose keys are valid fields and whose values are the constraints.  Use comparison operators (">", "<") for numeric fields, and exact strings for categorical fields.  Do **not** output any extra text or formatting.
    For numeric filters, use this format:
    "field": {"<": number} or "field": {">": number}
    Your options for filtering data are as follows ["gpa", "race_group", "gender", "interests","income"]
    ONLY respond with these options for filters.


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
    print(f"Filter: {response}")
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

    return df


def rank_students(df,description):
    scores = []
    chunk_size = 5
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        student_infos = ""
        for index, row in chunk.iterrows():
            student_infos += f"{index}. ({row['First Name']}) Interests: {row['Interests']}, Planned Major: {row['Planned Major']}, Career Path: {row['Career Path']}\n"
        dynamic_prompt2 = f"""
            SYSTEM:
            You are an AI assistant that ranks students based on how well they match a scholarship description.

            Your job is to return **only float scores between 0 and 1**, one per student, in the order given.

            INPUT:
            1. A scholarship description.
            2. A list of student profiles (each with interests, planned major, and career path).

            RULES:
            - Output must contain **only float scores**, one per line, in the same order as the student list.
            - Do **not** include any code, markdown, labels, explanations, or extra text.
            - Scores must be between 0 and 1.
            - Make sure to give every student one score

            SCORING CRITERIA:
            - Higher score if student interests or major match the scholarship theme.
            - Boost score for relevant career paths.
            - Penalize vague or generic goals.
            - Do not reject or filter; just score relevance.

            EXAMPLE:

            Scholarship: Looking for female students passionate about public health or social work, especially from low-income backgrounds.

            Student Profiles (2):
            1. (Simon) Interests: Whatever helps people idk, Planned Major: Social Work, Career Path: Nonprofit Organizer
            2. (Michael) Interests: Track and Field, Planned Major: Undecided, Career Path: Athlete

            Output:
            1. Simon: 0.82
            2. Michael: 0.10

            ---

            NOW PROCESS:

            Scholarship: {description}

            Student Profiles({len(chunk)}):
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
    df['match_score'] = list(map(float, scores))
    sorted_df = df.sort_values(by='match_score', ascending=False)
    print(sorted_df)
    return sorted_df


filters = get_filters("I need Asian students")

filtered_students = filter_students(filters)
description = "The SBB Research Group STEM Scholarship encourages and empowers students to create significant value and countless new opportunities for society through their pursuit of higher learning, especially through interdisciplinary combinations of Science, Technology, Engineering, and Mathematics (STEM)."
ranked_students = rank_students(filtered_students,description)

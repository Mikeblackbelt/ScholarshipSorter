import pandas as pd
import json
from huggingface_hub import InferenceClient
import dotenv
import os
dotenv.load_dotenv(".env")
token = os.environ["HF_TOKEN"]
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
    return df




def course_rigor(df,chunk_size=5):
    scores = []
    student_infos = ""
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        student_infos = ""
        for index, row in chunk.iterrows():
            student_infos += f"[{row['Grade']}] {row['Courses']}\n"
        dynamic_prompt2 = f"""
You are an AI assistant that evaluates a student's academic course load from Staten Island Technical High School (SITHS) on a scale of 0 to 1, based on how rigorous it is relative to the maximum rigor achievable at the school.

Your job is to return only float scores between 0 and 1, one per course list, in the order given.

INPUT:
A list of student academic records. Each line contains:
[Grade Level], followed by a list of all courses taken so far — from 9th grade up to their current grade.

RULES:

Output only float scores, one per line, in the same order as the input list.

Do not include any explanations, labels, markdown, or text.

Return exactly one score per input line.

All scores must be floats between 0 and 1.

SCHOOL-SPECIFIC SCORING CONTEXT:
Staten Island Technical High School academic structure:

Russian: 3 years required; Advanced Russian is optional starting 10th grade.

AP Course Limits by Grade:

9th Grade: 1 AP max — AP World History (required)

10th Grade: 2 APs max — AP World History (required)

11th Grade: 4 APs max — AP Precalculus (required unless taking Calculus BC) and AP U.S. History (required)

12th Grade: 4 APs max — fully elective, no required APs

Top-tier courses include:

Multivariable Calculus

AP Physics C

Dual Enrollment STEM/Policy/Research courses

Maximum rigor includes students who hit AP caps, take Multivariable Calculus, or complete advanced electives/Dual Enrollment by senior year.

SCORING CRITERIA:

Higher scores for students who reach or exceed their grade-level AP max, especially with advanced electives or college-level coursework.

Mid-range scores for students who meet grade-level AP expectations and include a few electives or honors classes.

Lower scores for students below AP/elective norms or with mostly standard courses.

Score based on how far they’ve progressed toward the rigor ceiling for their grade level at SITHS.

EXAMPLE INPUTS:

[12] Algebra I, Living Environment, AP World History, English I, Russian I, Intro to STEM, Geometry, Chemistry, English II, AP World History, Russian II, CAD & Civil Engineering, Algebra II, Physics, AP Precalculus, AP U.S. History, English III, Russian III, Robotics, AP Calculus BC, AP Physics C, AP English Lit, AP Gov, Dual Enrollment Engineering
[10] Algebra I, Living Environment, AP World History, English I, Russian I, Intro to STEM, Geometry, Chemistry, English II, AP World History, Russian II, CAD & Civil Engineering
[9] Algebra I, Living Environment, AP World History, English I, Russian I, Intro to STEM

Output:
0.96
0.61
0.36

NOW ANSWER:
{student_infos}
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
    df['Rigor Score'] = list(map(float, scores))
    print(df)
    return df



student_df = pd.read_csv("student_data.csv")
course_rigor_df = course_rigor(student_df, chunk_size=5)


import huggingface_hub
import os
import dotenv
from huggingface_hub import InferenceClient
import getRequirements as gR
dotenv.load_dotenv("n.env")
token = os.environ["HF_TOKEN"]
client = InferenceClient(
    provider="novita",
    api_key=token,

)

def calculate_Score(student: dict, factors: dict) -> float:
    biographicalWeight = 0.5
    biographicalFactors = ['Race', 'Gender', 'Income']
    bioScore = 0
    bioTotal = 0

    # Race check
    if 'Race' in factors:
        bioTotal += 1
        # Student race might be stored as e.g. 'Asian', factors['Race'] is list
        if student.get('Race') in factors['Race']:
            bioScore += 1

    # Gender check
    if 'Gender' in factors:
        bioTotal += 1
        if student.get('Gender') in factors['Gender']:
            bioScore += 1

    # Income check (assume income is int, factors['Income'] is dict with Min and Max)
    if 'Income' in factors:
        bioTotal += 1
        income = student.get('Income', 0)
        incomeMin = factors['Income'].get('Min', 0)
        incomeMax = factors['Income'].get('Max', float('inf'))
        if incomeMin <= income <= incomeMax:
            bioScore += 1

    if bioTotal == 0:
        return 1  # no bio factors to score

    bioScore = round((bioScore / bioTotal) * biographicalWeight, 3)




"""
def calculate_Score(student: dict, factors: list):
    biographicalWeight = 0.5
    biographicalFactors = ['race_group', 'gender', 'income']
    bioGraphicalScore = 0
    for factor in student:
        if factor in biographicalFactors:
            if student[factor] == biographicalFactors[factors.index(factor)]:
                bioGraphicalScore += biographicalWeight
"""
import smtplib
from email.message import EmailMessage
import os
import dotenv
from huggingface_hub import InferenceClient
import os
import json
dotenv.load_dotenv(".env")
token = os.environ["HF_TOKEN"]
client = InferenceClient(
    provider="novita",
    api_key=token,
)
dotenv.load_dotenv(".env")


class EmailSender:
    def __init__(self, sender, receiver, password):
        self.sender = sender
        self.receiver = receiver
        self.password = password
        with open("config.json", 'r') as f:
            email_json = json.load(f)
            self.subject = email_json['emailer']['subject']


    def send_email(self, body, subject=None):
        if subject is None:
            subject = self.subject
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = self.receiver

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.sender, self.password)
            smtp.send_message(msg)
            print("Email sent successfully!")
    def generate_email_template(self,scholarship_description,student_information):
        dynamic_prompt = f"""
You are an assistant helping a school counselor write personalized emails to students who qualify for a scholarship.

Below is a description of the scholarship and a filtered student's information. Based on this data, generate a warm, professional email body addressed to the student. The email should explain why they are a good fit for the scholarship, referencing relevant academic and service-based qualities.

### Scholarship Description:
{scholarship_description}

### Student Information:
{student_information}

### Filtering Rationale:
This student was selected because they match the characteristics the scholarship is looking for — for example, high GPA, strong community service involvement, and academic ambition as indicated by course rigor.
For any scores, they represent on a scale of 0 to 1, where 1 is the highest quality. For example a student with a service score of 0.88 has shown significant commitment to impactful service activities. Do not explicitly mention scores, just understand what they show about the student.
---

Return only the email body. Keep it concise (3–5 sentences), kind, and encouraging. Speak directly to the student (e.g., "you have shown...").
        """
        messagesG = [{
                    "role": "user",
                    "content": dynamic_prompt
                }]

        completion = client.chat.completions.create(
                model="meta-llama/Llama-3.1-8B-Instruct",
                messages=messagesG
            )
        messagesG.append(completion.choices[0].message)
        response = completion.choices[0].message.content
        print(response)
        return response


password = os.environ["EMAIL_PASSWORD"]
# Set up the email details
sender = 'siths.scholarship@gmail.com'
receiver = 'simonsaffayeh@gmail.com'
emailer = EmailSender(sender=sender, receiver=receiver, password=password)
ai_email = emailer.generate_email_template(
    scholarship_description="The Community Leaders of Tomorrow Scholarship is awarded to high school sophomores who demonstrate academic excellence and a strong commitment to community service.",
    student_information="Name: John Doe\nGrade: 10\nGPA: 96\nService Score: 0.88")
emailer.send_email(body=ai_email)
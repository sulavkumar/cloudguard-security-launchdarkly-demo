import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.responses.create(
    model="gpt-5.5",
    input="You are the AI Security Analyst for CloudGuard. Reply with one sentence confirming you are connected."
)

print("\nCloudGuard AI Security Analyst:")
print(response.output_text)
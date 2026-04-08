import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_section(section: str, content: str, template: str) -> str:
    prompt = f"""
You are an expert academic research paper writer.
Based on the following raw research content, write the {section} section 
of a research paper following {template} format.

Raw Content:
{content}

Rules:
- Be formal and academic in tone
- Be concise but comprehensive
- Follow {template} formatting standards
- Only return the {section} section content, nothing else
"""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text


def generate_full_paper(content: str, template: str) -> dict:
    sections = ["Abstract", "Introduction", "Methodology", "Results", "Conclusion"]
    paper = {}

    for section in sections:
        print(f"Generating {section}...")
        paper[section] = generate_section(section, content, template)
        time.sleep(3)  # avoid rate limiting

    return paper
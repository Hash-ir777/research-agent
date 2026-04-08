import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

IEEE_TEMPLATE = """
PAPER TITLE (Title Case, centered, bold, 24pt Times New Roman)

Author Name — dept. name of organization, name of organization, City, Country, email@domain.com

Abstract — Single paragraph, 150-250 words. Start with "Abstract—". No symbols, special characters, footnotes or math. Summarize: problem, method, key results, conclusion. Do NOT use bullet points.

Keywords — 4-6 lowercase keywords separated by commas.

I. INTRODUCTION (Heading 1, uppercase, bold)
Body text in Times New Roman 10pt, two-column layout, justified alignment.
Paragraph 1: Problem statement and motivation.
Paragraph 2: Existing approaches and limitations.
Paragraph 3: Proposed approach and contributions.
Paragraph 4: Paper organization ("Section II describes...")

II. METHODOLOGY (Heading 1)
A. Subsection Heading (Title Case, italic if needed)
Detailed technical approach. Passive voice. Formal academic tone.
Describe system architecture, algorithms, tools used.

III. RESULTS AND DISCUSSION (Heading 1)
Present findings and metrics from the content only.
Do NOT invent numbers. Discuss implications.

IV. CONCLUSION (Heading 1)
Paragraph 1: Summary of work and achievements.
Paragraph 2: Limitations.
Paragraph 3: Future work directions.

ACKNOWLEDGMENT (unnumbered heading)
Optional. Sponsor/funding acknowledgment.

REFERENCES (unnumbered heading)
[1] A. Author, "Title of paper," Journal Name, vol. X, no. X, pp. XX-XX, Year.
"""

def generate_full_paper(content: str, template: str) -> dict:
    prompt = f"""You are a strict IEEE conference paper formatter.

YOUR ONLY JOB: Take the raw research content below and restructure it into a properly formatted IEEE conference paper.

STRICT RULES — YOU MUST FOLLOW ALL OF THESE:
1. Use ONLY information from the provided content. Do NOT add any external knowledge, invented data, or filler text.
2. Do NOT change the meaning, results, or claims made in the original content.
3. If information for a section is missing from the content, write: "[Insufficient data in source content for this section]"
4. Do NOT use bullet points anywhere in the output.
5. Write in formal academic English. Third person. Passive voice preferred.
6. Each section must be properly structured per IEEE format.
7. Abstract must start with "Abstract—" and be 150-250 words.
8. Section headings must use Roman numerals: I. INTRODUCTION, II. METHODOLOGY, etc.
9. References must follow IEEE format: [1] A. Author, "Title," Journal, vol., pp., Year.
10. Do NOT include any meta-commentary, explanations, or notes about what you are doing.

IEEE PAPER STRUCTURE TO FOLLOW:
{IEEE_TEMPLATE}

RAW RESEARCH CONTENT (use ONLY this):
{content}

Return ONLY valid JSON in this exact format with no extra text before or after:
{{
    "Title": "...",
    "Authors": "...",
    "Abstract": "Abstract— ...",
    "Keywords": "...",
    "Introduction": "I. INTRODUCTION\\n\\n...",
    "Methodology": "II. METHODOLOGY\\n\\n...",
    "Results": "III. RESULTS AND DISCUSSION\\n\\n...",
    "Conclusion": "IV. CONCLUSION\\n\\n...",
    "Acknowledgment": "ACKNOWLEDGMENT\\n\\n...",
    "References": "REFERENCES\\n\\n[1] ..."
}}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    text = response.choices[0].message.content.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)
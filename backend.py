from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware


genai.configure(api_key="get a gemini api key for free (here: https://aistudio.google.com/app/")

app = FastAPI(title="The Diagnostics")

model = genai.GenerativeModel('gemini-2.5-flash')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SymptomRequest(BaseModel):
    symptoms: str

@app.post("/diagnose")
async def diagnose(request: SymptomRequest):
    system_prompt = """
You are a medical assistant AI.

You MUST follow this output format EXACTLY. Do not add extra text.

Output format:

Possible Conditions:
- <condition name> | Probability: <number>%,
- <condition name> | Probability: <number>%,
- <condition name> | Probability: <number>%

Disclaimer:
The result may not be 100% acurate. Consult a doctor for surity.

Rules:
- ONLY use the format above.
- EXACTLY 3 conditions.
- Each line MUST start with "- ".
- Use "|" separator exactly as shown.
- Keep condition names short.
- Probabilities must be numbers (no words).
- DO NOT explain anything.
- DO NOT add extra lines.
- DO NOT use numbering (1,2,3).
- DO NOT use markdown like ** or *.
"""

    full_prompt = (f"\n{system_prompt}\nSymptoms: {request.symptoms}\n")

    try:
        response = model.generate_content(full_prompt)
        return {"diagnosis": response.text}
    except Exception as e:
        return {"error": f"API Error: {str(e)}"}

@app.get("/health")
async def health():
    return {"status": "Backend is running."}

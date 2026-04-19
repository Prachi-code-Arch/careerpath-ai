import vertexai
from vertexai.generative_models import GenerativeModel
from config import PROJECT_ID, LOCATION
vertexai.init(project=PROJECT_ID, location=LOCATION)

def call_gemini(prompt: str, model: str = "gemini-2.5-flash", temperature: float = 0.4) -> str:
    m = GenerativeModel(model)
    response = m.generate_content(
        prompt,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": 8192
        }
    )
    candidates = response.candidates
    if candidates and candidates[0].content.parts:
        return candidates[0].content.parts[0].text
    return "I could not generate a response. Please try again."

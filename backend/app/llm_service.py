
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


# Configure API Key
api_key = os.getenv("GOOGLE_API_KEY")
is_api_key_valid = False

if not api_key:
    print("CRITICAL WARNING: GOOGLE_API_KEY is missing in backend/.env file.")
elif api_key.strip() == "your_google_api_key_here":
    print("CRITICAL WARNING: GOOGLE_API_KEY is still set to the placeholder value. Please update backend/.env.")
else:
    genai.configure(api_key=api_key)
    is_api_key_valid = True


class LLMService:
    def __init__(self, model_name="gemini-flash-latest"):
        self.model = genai.GenerativeModel(model_name)

    def generate_response(self, context: str, question: str) -> str:
        prompt = f"""
        You are a knowledgeable research assistant. Answer the user's question based strictly on the provided context below.
        If the context does not contain the answer, state that you cannot answer based on the document.
        Provide citations if possible (e.g., mention specific numbers or sections if present in context).
        
        Context:
        {context}
        
        Question:
        {question}
        
        Answer:
        """
        if not is_api_key_valid:
            if not api_key:
                return "Error: No Google API Key found. Please add GOOGLE_API_KEY to backend/.env file and restart the backend."
            if api_key.strip() == "your_google_api_key_here":
                return "Error: You need to replace the placeholder API key in backend/.env with your actual Google Gemini API key."
            return "Error: Invalid API configuration."

        try:
            response = self.model.generate_content(prompt)
            if not response.text:
                return "I couldn't generate a response. The model might have blocked the output or returned empty content."
            return response.text
        except Exception as e:
            return f"Error generating response: {e}"

llm_service = LLMService()

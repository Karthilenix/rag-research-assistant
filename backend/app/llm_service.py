
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
    def __init__(self):
        # Priority list of models to try
        self.models_to_try = [
            "gemini-1.5-flash",
            "gemini-1.5-flash-latest",
            "gemini-flash-latest",
            "gemini-1.5-pro",
            "gemini-pro"
        ]
        self.current_model = None

    def _get_model(self):
        """Try to initialize the first working model from the list"""
        if self.current_model:
            return self.current_model

        errors = []
        for model_name in self.models_to_try:
            try:
                print(f"DEBUG: Attempting to initialize model: {model_name}")
                model = genai.GenerativeModel(model_name)
                # Test the model with a dummy prompt to ensure it works/exists
                # We won't actually generate content here to save quota, 
                # but valid initialization is usually enough. 
                # However, to be 100% sure, a dry run is safer if we weren't on a strict quota.
                # For now, we assume if no exception on init, it's okay-ish, 
                # but 404s happens on generate.
                self.current_model = model
                self.active_model_name = model_name
                print(f"DEBUG: Successfully selected model: {model_name}")
                return model
            except Exception as e:
                print(f"WARNING: Failed to init {model_name}: {e}")
                errors.append(f"{model_name}: {e}")
        
        # If we fall through, just use the first one and hope or return None
        print("CRITICAL: Could not find a working model from the list. Defaulting to gemini-1.5-flash")
        return genai.GenerativeModel("gemini-1.5-flash")

    def generate_response(self, context: str, question: str) -> str:
        prompt = f"""
        You are an expert Research Analyst AI. Your task is to analyze the provided document text and answer the user's question with high accuracy.
        
        INSTRUCTIONS:
        1. Base your answer STRICTLY on the provided Context.
        2. If the answer is found, cite the specific section or page if inferred.
        3. If the answer is Not Valid or Not Found in the text, clearly state: "I cannot find this information in the provided document."
        4. Do NOT hallucinate or use outside knowledge.
        
        Context:
        {context}
        
        Question:
        {question}
        
        Answer:
        """
        
        if not is_api_key_valid:
             return "Error: Invalid API Key configuration."

        # Retry logic for models
        last_error = ""
        for model_name in self.models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                print(f"DEBUG: Generating with model: {model_name}")
                # Stream=False for now
                response = model.generate_content(prompt)
                if response.text:
                    return response.text
            except Exception as e:
                error_msg = str(e)
                print(f"WARNING: Error with {model_name}: {error_msg}")
                last_error = error_msg
                if "429" in error_msg:
                    return "Error: Google API Quota Exceeded (429). The free tier limit has been reached. Please wait a minute and try again."
                # If 404 or other, continue to next model
                continue
        
        return f"Error: Failed to generate response with all available models. Last error: {last_error}"

llm_service = LLMService()

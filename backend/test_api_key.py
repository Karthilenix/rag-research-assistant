
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Path to the .env file
env_path = os.path.join(os.path.dirname(__file__), ".env")
print(f"Loading environment from: {env_path}")
load_dotenv(env_path)

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found in .env file.")
    exit(1)

# Mask key for display
masked_key = f"{api_key[:5]}...{api_key[-5:]}" if len(api_key) > 10 else "***"
print(f"Loaded API Key: {masked_key}")

try:
    genai.configure(api_key=api_key)
    # Using 'gemini-2.0-flash' which was confirmed to be available
    model_name = 'gemini-flash-latest'
    print(f"attempting connection with model: {model_name}...")
    
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Reply with 'API is working with gemini-2.0-flash!'")
    print("\n✅ API CONNECTED SUCCESSFULLY!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"\n❌ API CONNECTION FAILED: {e}")
    # Fallback check
    print("\nTroubleshooting:")
    if "404" in str(e):
        print("The model name might be incorrect for your API key tier. Try checking available models.")
    else:
        print("Check your API key and internet connection.")

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load the GOOGLE_API_KEY from the .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY not found in .env file.")
else:
    try:
        genai.configure(api_key=api_key)
        
        print("Finding available models for your API key...")
        print("-" * 30)
        
        found_models = False
        for m in genai.list_models():
          if 'generateContent' in m.supported_generation_methods:
            print(m.name)
            found_models = True
        
        if not found_models:
            print("No models compatible with 'generateContent' were found for your key.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
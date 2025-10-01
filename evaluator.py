'''import google.generativeai as genai

def get_gemini_response(api_key, text):
    try:
        genai.configure(api_key=api_key)
        
        prompt = f"""
        You are an expert reviewer. Analyze the following R&D proposal text.
        Your final output must be a single, raw JSON object and nothing else. Do not wrap it in markdown.

        **Proposal Text:**
        "{text}"

        ---
        **JSON Schema:**
        {{
          "clarity_score": {{ "score": <integer 1-10>, "justification": "<string>" }},
          "novelty_score": {{ "score": <integer 1-10>, "justification": "<string>" }},
          "feasibility_score": {{ "score": <integer 1-10>, "justification": "<string>" }},
          "strengths": "<string>",
          "weaknesses": "<string>"
        }}
        """
        
        model = genai.GenerativeModel('models/gemini-pro-latest')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Return error as a JSON object as well for consistency
        return f'{{"error": "An error occurred during AI evaluation: {e}"}}'
        '''

import google.generativeai as genai

def get_gemini_response(api_key, text):
    try:
        genai.configure(api_key=api_key)
        
        prompt = f"""
        You are an expert reviewer. Analyze the following R&D proposal text.
        Your final output must be a single, raw JSON object and nothing else. Do not wrap it in markdown.

        **Proposal Text:**
        "{text}"

        ---
        **JSON Schema:**
        {{
          "clarity_score": {{ "score": <integer 1-10>, "justification": "<string>" }},
          "novelty_score": {{ "score": <integer 1-10>, "justification": "<string>" }},
          "feasibility_score": {{ "score": <integer 1-10>, "justification": "<string>" }},
          "strengths": "<string>",
          "weaknesses": "<string>"
        }}
        """
        
        model = genai.GenerativeModel('models/gemini-pro-latest')
        response = model.generate_content(prompt)
        # Clean the response to ensure it's a valid JSON string
        clean_response = response.text.strip().replace("```json", "").replace("```", "")
        return clean_response
    except Exception as e:
        # Return error as a JSON object for consistency
        return f'{{"error": "An error occurred during AI evaluation: {e}"}}'
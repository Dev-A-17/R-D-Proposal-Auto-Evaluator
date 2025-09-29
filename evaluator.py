'''import google.generativeai as genai

def get_gemini_response(api_key, text):
    """
    Sends the proposal text to the Gemini API for evaluation.
    Args:
        api_key: The user's Google AI Studio API key.
        text: The text extracted from the PDF proposal.
    Returns:
        The formatted response from the AI model.
    """
    try:
        genai.configure(api_key=api_key)
        
        # This is the prompt that instructs the AI
        prompt = f"""
        You are an expert reviewer for a national research grant committee. 
        Analyze the following R&D proposal text and provide a structured evaluation.

        **Proposal Text:**
        "{text}"

        **Evaluation Criteria & Output Format:**
        Please provide ONLY the following information, formatted exactly like this:

        **Clarity Score (1-10):** [Your score here]
        **Novelty Score (1-10):** [Your score here]
        **Feasibility Score (1-10):** [Your score here]
        
        **Strengths:**
        [A 2-sentence summary of the proposal's main strength.]
        
        **Weaknesses:**
        [A 2-sentence summary of its main weakness.]
        """
        
        model = genai.GenerativeModel('models/gemini-pro-latest')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"'''

import google.generativeai as genai

def get_gemini_response(api_key, text):
    try:
        genai.configure(api_key=api_key)
        
        prompt = f"""
        You are an expert reviewer for a national research grant committee, tasked with providing an initial screening report. 
        Analyze the following R&D proposal text and provide a structured evaluation.

        **Proposal Text:**
        "{text}"

        ---
        **EVALUATION RUBRIC & OUTPUT FORMAT**
        Please provide ONLY the following information, formatted exactly like this:

        **Clarity Score (1-10):** [Your score here, where 1-3 means 'Confusing/Vague,' 4-6 means 'Understandable but lacks detail,' 7-8 means 'Clear and well-defined,' and 9-10 means 'Exceptionally clear and precise.']
        **Novelty Score (1-10):** [Your score here, where 1-3 means 'Incremental or existing work,' 4-6 means 'Some new elements but largely derivative,' 7-8 means 'Genuinely novel approach,' and 9-10 means 'Breakthrough idea with high originality.']
        **Feasibility Score (1-10):** [Your score here, where 1-3 means 'Major flaws, unlikely to succeed,' 4-6 means 'Plausible but has significant risks,' 7-8 means 'Well-defined plan, likely to succeed,' and 9-10 means 'Highly detailed and convincing plan with low risk.']
        
        **Justification for Scores:**
        [A one-sentence justification for EACH of the three scores above, citing a specific aspect of the proposal.]
        
        **Strengths:**
        [A 2-sentence summary of the proposal's main strength.]
        
        **Weaknesses:**
        [A 2-sentence summary of its main weakness.]
        """
        
        model = genai.GenerativeModel('models/gemini-pro-latest')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"
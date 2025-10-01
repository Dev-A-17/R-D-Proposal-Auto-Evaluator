import os
import numpy as np
import google.generativeai as genai
from pdf_reader import read_pdf

def get_embedding(text, api_key):
    try:
        genai.configure(api_key=api_key)
        # IMPORTANT: Make sure this model name is correct for your API key
        result = genai.embed_content(
            model="models/text-embedding-004", 
            content=text,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return result['embedding']
    except Exception as e:
        print(f"Error creating embedding: {e}")
        return None

def calculate_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def check_novelty(uploaded_file_text, database_folder, api_key):
    new_embedding = get_embedding(uploaded_file_text, api_key)
    if not new_embedding:
        return [] # Return an empty list on error

    similarities = []

    for filename in os.listdir(database_folder):
        if filename.endswith(".pdf"):
            filepath = os.path.join(database_folder, filename)
            
            with open(filepath, "rb") as f:
                db_text = read_pdf(f)
                if db_text and "Error" not in db_text:
                    db_embedding = get_embedding(db_text, api_key)
                    if db_embedding:
                        similarity = calculate_similarity(new_embedding, db_embedding)
                        similarities.append((similarity, filename))
    
    # Sort the list by similarity score in descending order
    similarities.sort(key=lambda x: x[0], reverse=True)
    
    # Return the top 3 matches
    return similarities[:3]
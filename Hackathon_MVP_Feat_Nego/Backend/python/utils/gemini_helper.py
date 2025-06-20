import google.generativeai as genai
import os
import json

# Configure Gemini (no API key needed for free version)
genai.configure()

def generate_text(prompt, model_name="gemini-1.5-flash"):
    """Generate text using Gemini model"""
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text

def generate_structured_output(prompt, output_format, model_name="gemini-1.5-flash"):
    """Generate structured output with format enforcement"""
    full_prompt = f"""
    {prompt}
    
    Output MUST be in the following JSON format:
    {json.dumps(output_format, indent=2)}
    
    Return ONLY the JSON object without any additional text.
    """
    response = generate_text(full_prompt, model_name)
    
    # Extract JSON from response
    try:
        start = response.find('{')
        end = response.rfind('}') + 1
        return json.loads(response[start:end])
    except:
        # Fallback for Gemini output variations
        return output_format
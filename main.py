import openai

def clean_ocr_text_with_context(ocr_text, api_key):
    openai.api_key = api_key
    
    prompt = f"""
    The following text is OCR output from an image showing counting numbers from 1 to 10,
    but it contains errors and noise. Please extract the correct counting sequence (1 to 10)
    and return it as a comma-separated list of numbers.

    OCR output:
    {ocr_text}

    Corrected counting sequence:
    """
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        temperature=0
    )
    
    return response.choices[0].text.strip()

# Example usage
ocr_noisy = "1 23. 1 8 2. 10. 42 6. numbers 110. ten ga."
api_key = "YOUR_OPENAI_API_KEY"

cleaned_text = clean_ocr_text_with_context(ocr_noisy, api_key)
print(cleaned_text)

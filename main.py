import openai

def fix_counting_ocr_text(ocr_text, openai_api_key):
    openai.api_key = openai_api_key

    prompt = f"""
    The following OCR output is noisy and contains errors. It comes from an image showing counting from 1 to 10.
    Please interpret and correct the text, and return only the clean counting sequence from 1 to 10.

    OCR output:
    {ocr_text}

    Corrected counting:
    """

    response = openai.Completion.create(
        model="gpt-4o-mini",
        prompt=prompt,
        max_tokens=20,
        temperature=0
    )

    return response.choices[0].text.strip()

# Example usage
ocr_noisy_text = "1 23. 1 8 2. 10. 42 6. numbers 110. ten ga."
openai_api_key = "YOUR_OPENAI_API_KEY"
clean_text = fix_counting_ocr_text(ocr_noisy_text, openai_api_key)
print(clean_text)

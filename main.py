import openai

def correct_ocr_text(raw_ocr_text, api_key):
    openai.api_key = api_key
    prompt = f"""
    The following is noisy OCR output from an image showing counting from 1 to 10.
    Please extract and return the correct counting numbers in order as a comma-separated list.

    OCR Output:
    {raw_ocr_text}

    Correct Counting:
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=20,
        temperature=0,
    )
    return response.choices[0].text.strip()

# Example
raw_text = "1 23. 1 8 2. 10. 42 6. numbers 110. ten ga."
api_key = "YOUR_OPENAI_API_KEY"

cleaned_text = correct_ocr_text(raw_text, api_key)
print(cleaned_text)  # Expected: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

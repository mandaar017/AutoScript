import google.generativeai as genai
from config import API_KEY
import re

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def generate_email_from_intent(intent):
    chat = model.start_chat()
    prompt = f"(no extra unecessary text since this is an api call) Generate a text for this intent: {intent}"
    response = chat.send_message(prompt)
    return response.text

def _extract_numbers(text: str):
    """Return list of integers found in text in order."""
    return [int(n) for n in re.findall(r'\d+', text)]

def get_ai_answer(question_text: str, options: list[str], multi: bool = False):
    """
    Ask Gemini to generate a realistic answer.
    If options are given, AI must choose from them.
    Returns:
      - str (for text or single-choice)
      - list[str] (for multi-choice)
    """
    numbered = "\n".join(f"{i+1}) {opt}" for i, opt in enumerate(options))
    prompt = (
        f"You are filling a Google Form.\n"
        f"Question: {question_text}\n"
        f"Options:\n{numbered}\n\n"
    )
    if multi:
        prompt += (
            "Return ONLY the option number(s) that best answer the question, as comma-separated numbers (e.g. 1,3).\n"
            "Do NOT include any other text, explanation or punctuation other than digits and commas."
        )
    else:
        prompt += (
            "Return ONLY the single option number (e.g. 2) that best answers the question.\n"
            "Do NOT include any other text or explanation."
        )

    chat = model.start_chat()
    resp = chat.send_message(prompt)
    raw = resp.text.strip()

    # 1) Try to extract digits directly
    nums = _extract_numbers(raw)
    if nums:
        if multi:
            # dedupe while preserving order
            seen = set(); out = []
            for n in nums:
                if n not in seen:
                    seen.add(n); out.append(n)
            return out
        else:
            return nums[0]

    # 2) Fallback: try to match option text inside model response
    lower_raw = raw.lower()
    matches = []
    for i, opt in enumerate(options):
        lo = opt.lower()
        if lo and (lo in lower_raw or lower_raw in lo):
            matches.append(i+1)
            if not multi:
                break

    if matches:
        return matches if multi else matches[0]

    # 3) Last-resort fallback: return first (1) or first item as list
    return ([1] if multi else 1)
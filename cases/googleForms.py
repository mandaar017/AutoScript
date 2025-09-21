from utils.ai_utils import get_ai_answer
from config import FORMURL

def run(page):
    
    page.goto(FORMURL)
    
    questions = page.query_selector_all('div[role="listitem"]')
    
    for question in questions:

        question_text_el = question.query_selector("div[role='heading']")
        if not question_text_el:
            continue

        question_text = question_text_el.inner_text().strip()
        print("\n❓ Question:", question_text)
        
            
        # Single-choice (radio)
        radio_group = question.query_selector("div[role='radiogroup']")
        if radio_group:
            option_els = radio_group.query_selector_all("div[role='radio']")
            option_texts = [oe.inner_text().strip() for oe in option_els]
            # ask AI for the number
            chosen_num = get_ai_answer(question_text, option_texts, multi=False)
            print("→ chosen number:", chosen_num)
            idx = int(chosen_num) - 1
            if 0 <= idx < len(option_els):
                option_els[idx].click()
            continue

        # Multi-choice (checkbox)
        checkbox_els = question.query_selector_all("div[role='checkbox']")
        if checkbox_els:
            option_texts = [ce.inner_text().strip() for ce in checkbox_els]
            chosen_nums = get_ai_answer(question_text, option_texts, multi=True)
            print("→ chosen numbers:", chosen_nums)
            # ensure list
            if isinstance(chosen_nums, int):
                chosen_nums = [chosen_nums]
            for n in chosen_nums:
                i = int(n) - 1
                if 0 <= i < len(checkbox_els):
                    checkbox_els[i].click()
            continue

    # Submit (adjust selector if needed)
    submit = page.query_selector("div[role='button']:has-text('Submit')")
    if submit:
        submit.click()

    page.wait_for_timeout(3000)

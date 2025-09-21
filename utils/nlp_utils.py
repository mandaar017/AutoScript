import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

intent_keywords = {
    "attendance": {
        "attendance", "marks", "grades", "scores", "record", "report", "presence", "lecture", "class", 
        "cie", "semester", "exam", "performance", "result", "academic", "subject","check","grade"
    },
    "ecommerce": {
        "shop", "buy", "purchase", "order", "cart", "product", "item", "checkout", "sale", "buying", 
        "shopping", "store", "add to cart", "purchase item", "buy product", "payment"
    },
    "intern": {
        "internship", "job", "career", "apply", "vacancy", "position", "work", "opportunity", 
        "recruitment", "placement", "hiring", "trainee", "role", "employment", "posting", "application"
    },
    "email": {
        "email", "mail", "message", "send", "compose", "draft", "inbox", "reply", "forward", 
        "mailing", "letter", "notification", "contact", "communication", "correspondence"
    },
    "googleforms": {
        "form", "google", "survey", "fill", "submit", "answer", "questionnaire", "application form", 
        "registration", "quiz", "entry", "response", "input", "fill out", "form submission", "questions"
    }
}

def detect_intent(user_input: str) -> str | None:
    """
    Detect user intent using keyword overlap (via spaCy lemmas).
    Returns the key matching one of the cases_map.
    """
    doc = nlp(user_input.lower())
    lemmas = {token.lemma_ for token in doc}
    print("🔑 Extracted lemmas:", lemmas)

    best_match = None
    best_score = 0

    for intent, keywords in intent_keywords.items():
        overlap = len(lemmas & keywords)
        if overlap > best_score:
            best_score = overlap
            best_match = intent

    return best_match if best_match else None
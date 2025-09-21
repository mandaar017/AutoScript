import time
import random

def human_typing(element, text):
    for char in text:
        element.type(char, delay=random.uniform(50, 150))
        time.sleep(random.uniform(0.05, 0.15))
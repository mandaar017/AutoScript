from playwright.sync_api import sync_playwright
from config import USER_AGENT
from utils import nlp_utils
from colorama import init, Fore, Style
init(autoreset=True)

# Import cases
from cases import attendance, ecommerce, intern, email, googleForms

cases_map = {
                "attendance": attendance.run,
                "ecommerce": ecommerce.run,
                "intern": intern.run,
                "email": email.run,
                "googleforms": googleForms.run
            }

def stealth_browser_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context(
            user_agent=USER_AGENT,
            locale="en-US",
            timezone_id="America/New_York",
            geolocation={"longitude": -73.935242, "latitude": 40.730610},
            permissions=["geolocation"],
            color_scheme="light",
            device_scale_factor=1,
            has_touch=False,
            is_mobile=False,
        )
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
        """)
        
        print("Stealth session launched successfully.")
        page = context.new_page()
        
        user_input=input(Fore.GREEN + "What do you want to do?\n")
        
        intent= nlp_utils.detect_intent(user_input)
        
        if intent and intent in cases_map :
            print(f"Detected intent: {intent}")
            cases_map[intent](page)
        else:
            print(Fore.RED + "Sorry, I couldn't understand what you want.")
                    
        browser.close()
                    

                            
                
if __name__ == "__main__":
    stealth_browser_session()
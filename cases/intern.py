from utils.typing_utils import human_typing

def run(page):
    page.goto("https://internshala.com/")
    page.locator('button.search-cta').click()
    human_typing(page.locator('input[type="text"]'),"  Android App Development")
    page.keyboard.press("Enter")
    
    page.wait_for_selector("div#internship_list_container_1")
    internships = page.locator("div[id^='individual_internship_']")  # all internship blocks

    data = []
    count = internships.count()
    print(f"Found {count} internships.")

    for i in range(count):
        internship = internships.nth(i)
        
        try:
            title = internship.locator("a.job-title-href").inner_text(timeout=1000)
            stipend=internship.locator("span.stipend").inner_text(timeout=1000)
            link = internship.locator("a.job-title-href").get_attribute("href")
            company = internship.locator("div.company_name").inner_text(timeout=1000)
            try:
                duration = internship.locator("div.row-1-item:has(i.ic-16-calendar) span").inner_text(timeout=1000)
            except:
                duration = "N/A"
                
            data.append({
                "Title": title,
                "Company": company,
                "Stipend":stipend,
                "Duration": duration,
                "Link": f"https://internshala.com{link}" if link else "N/A"
            })
        except Exception as e:
                print(f"❌ Failed to extract internship {i + 1}: {e}")
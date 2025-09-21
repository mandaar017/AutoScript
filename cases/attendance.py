import pandas as pd
from utils.typing_utils import human_typing
from config import USN, PASS

def run(page):
    page.goto("https://webcampus.bmsce.in/student")
    
    human_typing(page.locator('input[type="text"]'),USN)
    human_typing(page.locator('input[type="password"]'),PASS)
    page.locator("button:has-text('Sign In')").click()
    page.locator("a:has-text('Attendance')").click()
    
    page.wait_for_selector("table#js_dataTable1")  # Wait for table

    # Get all rows as individual elements
    rows = page.locator("table#js_dataTable1 tr").all()

    data = []
    for row in rows:
        cells = row.locator("th, td").all()
        data.append([cell.inner_text().strip() for cell in cells])

    if len(data) > 1:
        df = pd.DataFrame(data[1:], columns=data[0])
    else:
        df = pd.DataFrame(data)

    df.to_csv("Attendance.csv", index=False)
    print("✅ Table saved to attendance.csv")

    page.go_back()
    page.wait_for_load_state("load")
    
    #CIE
    page.locator("a:has-text('CIE')").click()
    # Get all rows as individual elements
    table = page.locator("table#js_dataTable1")

    rows = table.locator("tr").all()
    data = []
    for row in rows:
        cells = row.locator("th, td").all()
        data.append([cell.inner_text() for cell in cells])

    # Convert to DataFrame and display
    df = pd.DataFrame(data[1:], columns=[f"Column_{i}" for i in range(1, 16)])

    df.to_csv("CIE.csv", index=False)
    print("✅ Table saved to cie.csv")
    
    page.wait_for_timeout(3000)
from utils.typing_utils import human_typing

def run(page):
    page.goto("https://www.saucedemo.com/")
    human_typing(page.locator('input[type="text"]'),"standard_user")
    human_typing(page.locator('input[type="password"]'),"secret_sauce")
    page.locator('input[type="submit"]').click()
    page.locator('button#add-to-cart-sauce-labs-bike-light').click()
    page.locator('button#add-to-cart-sauce-labs-bolt-t-shirt').click()
    page.locator('a.shopping_cart_link').click()
    page.wait_for_timeout(1000)
    page.locator('button#checkout').click()
    human_typing(page.locator('input#first-name'),"Mandaar")
    human_typing(page.locator('input#last-name'),"Adarsh")
    human_typing(page.locator('input#postal-code'),"560050")
    page.locator('input#continue').click()
    page.locator('button#finish').click()
    page.wait_for_timeout(1000)
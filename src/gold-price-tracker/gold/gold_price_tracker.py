from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import date
from tabulate import tabulate


def get_gold_price(driver):
    url = "https://www.lalithaaschemes.com/home"

    try:
        # Load the webpage
        driver.get(url)

        # Find the gold price element using its XPath
        gold_price_element = driver.find_element(By.XPATH,
                                                 "/html/body/app-root/header/div[1]/div/div/div[2]/div/div[2]/form/select")

        if gold_price_element:
            gold_price = gold_price_element.text.strip()
            return gold_price
        else:
            return None

    except Exception as e:
        print("Error occurred:", str(e))
        return None


def save_gold_price(filename, gold_price):
    today = date.today().strftime("%Y-%m-%d")

    gold_prices = gold_price.split("\n")

    # Create a table with the gold price data
    gold_price_table = []
    for gold in gold_prices:
        gold_info = gold.strip().split(" ₹ ")
        gold_price_table.append(gold_info)

    with open(filename, 'a') as file:
        file.write(f"{today}:\n")
        file.write(tabulate(gold_price_table, headers=["Type", "Price"], tablefmt="fancy_grid"))
        file.write("\n\n")


def main() -> None:
    # Set up Selenium WebDriver with Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=chrome_options)
    # Get the gold price
    daily_gold_price = get_gold_price(driver)

    # Save the gold price in a file
    filename = 'gold_prices.txt'
    if daily_gold_price:
        save_gold_price(filename, daily_gold_price)
        print("Daily Gold Price:", daily_gold_price)
    else:
        print("Failed to retrieve the gold price.")

    # Quit the driver
    driver.quit()


if __name__ == "__main__":
    main()

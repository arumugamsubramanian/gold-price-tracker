from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import date
from tabulate import tabulate
import re
import csv


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
    print(gold_prices)

    # Create a table with the gold price data
    gold_price_table = []
    for gold in gold_prices:
        gold_info = gold.strip().split(" ₹ ")
        gold_price_table.append(gold_info)

    with open(filename, 'a') as file:
        file.write(f"{today}:\n")
        file.write(tabulate(gold_price_table, headers=["Type", "Price"], tablefmt="fancy_grid"))
        file.write("\n\n")

    # Append to the CSV file
    with open('gold_prices.csv', 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for gold_info in gold_price_table:
            csv_writer.writerow([today] + gold_info)


def convert_txt_csv():
    # Read the content of the file
    with open('gold_prices.txt', 'r') as file:
        content = file.read()

    # Find all date sections in the content
    date_sections = re.findall(r'(\d{4}-\d{2}-\d{2}):\n(.*?)\n\n', content, re.DOTALL)

    # Create a list to store the extracted data
    data = []

    # Loop through each date section and extract the relevant information
    for date, section in date_sections:
        lines = section.strip().split('\n')
        headers = [header.strip() for header in lines[1].split('│')[1:-1]]
        for i in range(3, len(lines), 2):
            parts = lines[i].split('│')[1:-1]
            row = [date] + [part.strip() for part in parts]
            data.append(row)

    # Write the extracted data to a CSV file
    with open('gold_prices.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Date'] + headers)

        for row in data:
            csv_writer.writerow(row)

    print("CSV file 'gold_prices.csv' has been created.")


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

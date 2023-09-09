import argparse
import csv
import re
from datetime import date

from playwright.sync_api import sync_playwright


def test_google():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to Google
        page.goto('https://www.google.com')

        # Get and print the HTML content of the page
        # page_content = page.content()
        # print(page_content)

        # Take a screenshot
        # page.screenshot(path='screenshot.png')

        # Close the browser
        browser.close()


def extract_metal_rates():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        # page = browser.new_page()

        # Go to the website
        page.goto("https://www.grtjewels.com/")

        # Get and print the HTML content of the page
        # page_content = page.content()
        # print(page_content)

        # Take a screenshot
        # page.screenshot(path='screenshot.png')

        # Wait for the element to load
        page.wait_for_selector("#todaysrate .rate.slide-rates", timeout=30000)

        # Click on the dropdown to make additional information visible
        page.click("#todaysrate .rate.slide-rates")

        # Wait for the dropdown to appear
        page.wait_for_selector("#todaysrate .state_rates")

        # Get the parent element containing all metal rates
        parent_element = page.query_selector("#todaysrate .state_rates")

        # Get the text content of all metal rates within the parent element
        get_metal_rates_text = parent_element.text_content()

        # Close the browser
        browser.close()

        return get_metal_rates_text


def lalitha_extract_metal_rates():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the website
        page.goto('https://www.lalithaajewellery.com/')

        # Wait for the element to be present
        page.wait_for_selector('.welcome-message a')

        # Extract the rates from the marquee element
        rates_text = page.inner_text('.welcome-message a')

        # Close the browser
        browser.close()

        print(rates_text)

        return rates_text


def process_metal_rates(metal_text):
    metal_rates_data = metal_text.strip()
    # Use regular expression to split the text
    metal_rates = re.findall(r'(.*?Rs\d+)', metal_rates_data)

    metal_rates_list = []

    for rate in metal_rates:
        parts = rate.split('-')
        metal_name = parts[0].strip()
        purity = parts[1].strip()

        # Extract the weight and remove 'Rs' and extra spaces
        weight_and_price = parts[-1].strip().replace('Rs', '')

        # Check if the weight_and_price contains a space
        if ' ' in weight_and_price:
            weight, price = weight_and_price.split()
            weight = f'1 g {weight}'  # Add '1 g' to weight
        else:
            # If no space, treat the entire string as price, and set weight to '1 g'
            weight = '1 g'
            price = weight_and_price

        metal_rates_list.append([metal_name, purity, weight, price])

    return metal_rates_list


def save_gold_price(gold_price):
    current_date = date.today().strftime("%Y-%m-%d")

    # Append to the CSV file
    with open('gold_prices.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for item in gold_price:
            print(item)
            metal_name = item[0]
            purity = item[1]
            weight = item[2]
            price = item[3]
            writer.writerow([current_date, f'{metal_name}-{purity}-{weight}', price])


def lalitha_format_rate_text(text):
    # Define regex patterns for different metals
    gold_pattern = re.compile(r'Gold (\d+k) - (\d)g = Rs\. (\d+)')
    silver_pattern = re.compile(r'Silver (\d)g = Rs\. (\d+\.\d+)')
    platinum_pattern = re.compile(r'Platinum (\d)g = Rs\. (\d+)')

    # Initialize an empty list to store the extracted information
    result = []

    # Match and extract gold rates
    gold_matches = gold_pattern.findall(text)
    for match in gold_matches:
        result.append(['GOLD', match[0], f"{match[1]} g", match[2]])

    # Match and extract silver rates
    silver_matches = silver_pattern.findall(text)
    for match in silver_matches:
        result.append(['SILVER', f"{match[0]} g", f"{match[0]} g", match[1]])

    # Match and extract platinum rates
    platinum_matches = platinum_pattern.findall(text)
    for match in platinum_matches:
        result.append(['PLATINUM', f"{match[0]} g", f"{match[0]} g", match[1]])

    return result


def main() -> None:
    # test_google()
    parser = argparse.ArgumentParser(description='Extract rates from jewelry store websites.')
    parser.add_argument('--store', choices=['lalitha', 'grt'], required=True, help='Specify the jewelry store')

    args = parser.parse_args()
    store = args.store

    if store == 'lalitha':
        lalitha_rates_text = lalitha_extract_metal_rates()
        lalitha_rate_list = lalitha_format_rate_text(lalitha_rates_text)
        print(lalitha_rate_list)
        save_gold_price(lalitha_rate_list)
    elif store == 'grt':
        metal_rates_text = extract_metal_rates()
        metal_rate_list = process_metal_rates(metal_rates_text)
        print(metal_rate_list)
        save_gold_price(metal_rate_list)


if __name__ == "__main__":
    main()

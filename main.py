import time

from bs4 import BeautifulSoup, Tag
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from app.browser import Browser
from app.constants import BASE_URL, SLEEP_TIME, START_URL

HOUSE_ELEMENTS = {
    "title": "span.property-street.tekst-title",
    "description": "div.property-description",
    "price": "span.property-price",
    "details": "div.property-details",
}


def get_house_info(driver: WebDriver, house: Tag):
    house_anchor = house.select_one("a")
    if not house_anchor:
        return

    house_link = house_anchor.get("href")
    if not house_link or house_link == "#":
        return

    # Open house link
    driver.get(f"{BASE_URL}/{house_link}")
    time.sleep(SLEEP_TIME)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    data = {}
    for key, classes in HOUSE_ELEMENTS.items():
        value = soup.select_one(classes)
        if not value:
            continue

        if key == "details":
            for sub in value.select("div"):
                sub_name, sub_value = sub.findAll("span")
                data[key] = {sub_name.text.strip(): sub_value.text.strip()}
        else:
            data[key] = value.text.strip()

    print(data)


def main():
    with Browser(headless=True) as driver:
        try:
            # Open start url
            driver.get(START_URL)
            time.sleep(SLEEP_TIME)

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")

            # Select Houses
            houses_listing = soup.select_one("div.listing-houses")
            if not houses_listing:
                return
            houses = houses_listing.select("div.listing_object")
            print("houses received: ", len(houses))

            for house in houses:
                get_house_info(driver, house)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()

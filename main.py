import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from typing import List
import csv
import createDb

@dataclass
class Car:
    link: str
    full_name: str
    year: int
    mileage_km: str
    gear_type: str
    fuel_type: str
    price: int
    dateAdd: str

class AutoBazarScraper:
    def __init__(self, car_make: str) -> None:
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                          "AppleWebKit/537.11 (KHTML, like Gecko) "
                          "Chrome/23.0.1271.64 Safari/537.11",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
            "Accept-Encoding": "none",
            "Accept-Language": "en-US,en;q=0.8",
            "Connection": "keep-alive",
        }
        self.car_make = "https://" + car_make
        self.website = ".autobazar.eu"

    def get_pages_count(self):
        website = self.car_make + self.website
        response = requests.get(website, headers=self.headers).text
        soup = BeautifulSoup(response, "html.parser")

        try:
            pages_number = soup.find("a", class_="p-item p-last").text.strip()
            return pages_number
        except Exception as e:
            pages_number = len(soup.find_all("a", {"class": "p-item p-number"})) + 1
            return pages_number

    def scrape_pages(self, number_of_pages: int) -> List[Car]:
        cars = []
        for i in range(1, int(number_of_pages) + 1):
            current_website = f"{self.car_make}{self.website}/?page={i}"
            new_cars = self.scrape_cars_from_current_page(current_website)
            if new_cars:
                cars += new_cars
        return cars

    def scrape_cars_from_current_page(self, current_website: str) -> List[Car]:
        try:
            response = requests.get(current_website, headers=self.headers).text
            soup = BeautifulSoup(response, "html.parser")
            cars = self.extract_cars_from_page(soup)
            return cars
        except Exception as e:
            print(f"Problem with scraping website: {current_website}, reason: {e}")
            return []

    def extract_cars_from_page(self, soup: BeautifulSoup) -> List[Car]:
        offers_table = soup.find("div", class_="clearfix")
        cars_basic = offers_table.find_all("div", {"class": "listitem"})
        list_of_cars = []

        for car in cars_basic:
            try:
                link = car.find("div", class_="listitem-content-left").find("a", href = True).get("href").replace("//", "")
                full_name = car.find("div", class_ = "listitem-content-right").find("a", href = True).get("title") if car.find("div", class_ = "listitem-content-right").find("a", href = True).get("title") else None
                year = car.find("span", class_ = "listitem-info-year").text.strip() if car.find("span", class_ = "listitem-info-year") else None
                mileage_km = car.find("span", class_ = "listitem-info-km").text.strip() if car.find("span", class_ = "listitem-info-km") else None
                gear_type = car.find("span", class_= "listitem-info-trans").text.strip() if car.find("span", class_= "listitem-info-trans") else None
                fuel_type = car.find("span", class_ = "listitem-info-fuel").text.strip() if car.find("span", class_ = "listitem-info-fuel") else None
                price = car.find("div", class_ = "listitem-price").text.strip() if car.find("div", class_ = "listitem-price") else None
                dateAdd = car.find("div", class_="listitem-breadcrumbs").find_next("span").find_next("span").text if car.find("div", class_="listitem-breadcrumbs").find_next("span").find_next("span") else None
                list_of_cars.append(
                    Car(
                        link = link,
                        full_name = full_name,
                        year = year,
                        mileage_km = mileage_km,
                        gear_type = gear_type,
                        fuel_type = fuel_type,
                        price = price,
                        dateAdd = dateAdd
                    )
                )
            except Exception as e:
                print(f"Error msg: {e}")

        return list_of_cars


def write_to_csv(cars: List[Car]) -> None:
    with open(f"cars/{brand}.csv", mode="w") as f:
        fieldnames = [
            "link",
            "full_name",
            "year",
            "mileage_km",
            "gear_type",
            "fuel_type",
            "price",
            "dateAdd"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for car in cars:
            writer.writerow(asdict(car))

def scrape_autobazar(brand: str) -> None:
    scraper = AutoBazarScraper(brand)
    cars = scraper.scrape_pages(scraper.get_pages_count())
    write_to_csv(cars)
    #createDb.fill_database(brand)


if __name__ == "__main__":
    brand = input("Enter brand of a car, you wanna scrape from autobazar.eu:\n")
    scrape_autobazar(brand)

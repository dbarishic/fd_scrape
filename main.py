# Write a script to crawl events from a clients website (date, time, location, title, artists, works, image link, everything that is possible)
# Insert data into a database (PostgresSQL), with a self-defined schema
# The script, after crawling, should extract the data from the database and plot the data. The plot should show the total events of each day.
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup, Tag

from dto.event import Event
from dto.performer import Performer
from dto.venue import Venue

BASE_URL = "https://www.lucernefestival.ch"
START_URL = f"{BASE_URL}/en/program/summer-festival-22"  # start scraping from here


def scrape():
    html = get_html(START_URL)
    event_elements = html.find_all("div", class_="event-content")

    events = []
    tasks = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        for event_element in event_elements:
            tasks.append(executor.submit(extract_info_from_event_elem, event_element))

    for task in as_completed(tasks):
        events.append(task.result())

    dates = []
    for event in events:
        dates.append(event.date)
    from collections import Counter
    result = dict(Counter(dates))

    print(result)


def extract_info_from_event_elem(event_elem: Tag) -> Event:
    try:
        event_title_div = event_elem.find("p", class_="event-title")
        title = event_title_div.get_text(strip=True)

        more_info_path = event_title_div.find("a", href=True).get("href")
        more_info_url = f"{BASE_URL}{more_info_path}"
        try:
            event_img_url, performers, program, description, venue = scrape_more_info_page(more_info_url)
        except AttributeError:
            print("Could not scrape more info page")
            event_img_url, performers, program, description, venue = None, None, None, None, None

    except AttributeError as ae:
        print(f"Could not parse title, {repr(ae)}")
        title = None

    try:
        date_and_venue = event_elem.find("strong", text="Date and Venue").next_sibling.next_sibling.get_text(strip=True)
        date, time, venue_name = extract_datetime_venue(date_and_venue)
    except AttributeError as ae:
        print(f"Could not parse date and venue, {repr(ae)}")
        date, time, venue_name = None, None, None

    try:
        program = event_elem.find("strong", text="Program").next_sibling.next_sibling.get_text(strip=True)
    except AttributeError as ae:
        print(f"Could not parse program, {repr(ae)}")
        program = None

    try:
        ticket_status = event_elem.find("div", class_="ticket-status")
        children = ticket_status.find_all(recursive=False)
        buy_tickets_url, festival, price = extract_ticket_info(children)
    except AttributeError as ae:
        print(f"Could not parse ticket status, {repr(ae)}")
        buy_tickets_url, festival, price = None, None, None

    event = Event()
    event.title = title
    event.date = date
    event.time = time
    event.venue = venue
    event.description = description
    event.program = program
    event.festival = festival
    event.ticket_purchase_url = buy_tickets_url
    event.performers = performers
    event.image_url = event_img_url

    return event


def scrape_more_info_page(url: str) -> (str, list[Performer], str, str, Venue):
    html = get_html(url)
    img_path = html.find("figure", class_="fullscreen-image").find("img").get("src")
    event_img_url = f"{BASE_URL}{img_path}"

    if cast := html.find("section", id="cast"):
        performers = scrape_cast_info(cast)
    else:
        print("Could not scrape cast")
        performers = None

    if program := html.find("section", id="program"):
        pass
    else:
        print("Could not scrape program")

    if description := html.find("section", id="description"):
        description = description.find("p").text
    else:
        print("Could not scrape description")

    if venue := html.find("section", id="venue"):
        venue_name = venue.find("p", class_="title").find("strong").text.strip()
        venue_addr = venue.find("p", class_="title").next_sibling.next_sibling.text.strip()
        venue_google_maps = venue.find("p", class_="title").find_next_sibling("a").get("href")
        venue_details_elements = venue.find("ul", class_="accordion").find_all("a", class_="accordion-title")

        try:
            venue_arrival_info = venue_details_elements[0].find_next_sibling("div").text
            venue_cloakroom_info = venue_details_elements[1].find_next_sibling("div").text
            venue_wheelchair_info = venue_details_elements[2].find_next_sibling("div").text
            venue_late_admission_info = venue_details_elements[3].find_next_sibling("div").text
            venue_gastronomy_info = venue_details_elements[4].find_next_sibling("div").text
        except IndexError as e:
            print(f"Could not scrape venue info, {repr(e)}")
            venue_arrival_info, venue_cloakroom_info, venue_wheelchair_info, venue_late_admission_info, venue_gastronomy_info = None, None, None, None, None

        venue = Venue()
        venue.name = venue_name
        venue.address = " ".join(venue_addr.split())
        venue.google_maps_url = venue_google_maps
        venue.arrival_parking_info = " ".join(venue_arrival_info.split())
        venue.cloakroom = " ".join(venue_cloakroom_info.split())
        venue.wheelchair_access = " ".join(venue_wheelchair_info.split())
        venue.late_admission_info = " ".join(venue_late_admission_info.split())
        venue.gastronomy = " ".join(venue_gastronomy_info.split())
    else:
        print("Could not scrape venue")

    return event_img_url, performers, program, description, venue


def get_html(url):
    response = requests.get(url)
    html = BeautifulSoup(response.content, "html.parser")
    return html


def scrape_cast_info(cast_element) -> list[Performer]:
    urls = get_cast_info_urls(cast_element)

    performers = []

    for url in urls:
        html = get_html(url)
        performer_name = html.find("div", class_="readmore-text").find("strong").text
        performer_description = html.find("div", class_="readmore-text").text
        performers.append(Performer(name=performer_name, description=performer_description))

    return performers


def get_cast_info_urls(cast_element: Tag) -> list[str]:
    cast_links = cast_element.find_all("a")

    urls = []
    for link in cast_links:
        urls.append(f"{BASE_URL}{link.get('href')}")

    return urls


def extract_datetime_venue(date_and_venue) -> tuple[datetime.date, str, str]:
    date_and_venue = " ".join(date_and_venue.split())  # remove (all but one) spaces and all special characters
    tokens = date_and_venue.split("|")

    date = tokens[0].strip().split(' ')[1]
    day = int(date.split('.')[0])
    month = int(date.split('.')[1])
    date = datetime.date(2022, month, day)

    time = tokens[1]
    venue = tokens[2]
    return date, time.strip(), venue.strip()


def extract_ticket_info(ticket_info_element) -> tuple[str, str, str]:
    try:
        festival = ticket_info_element[0].get_text(strip=True)
    except IndexError as e:
        festival = None
        print(f"Could not parse festival, {repr(e)}")
    try:
        buy_tickets_url = ticket_info_element[1].get('href') or "SOLD OUT"
    except IndexError as e:
        buy_tickets_url = None
        print(f"Could not parse ticket purchase url, {repr(e)}")
    try:
        price = ticket_info_element[2].get_text(strip=True)
    except IndexError as e:
        price = None
        print(f"Could not parse price, {repr(e)}")
    return buy_tickets_url, festival, price


def write_to_db():
    pass


def read_from_db():
    pass


if __name__ == '__main__':
    scrape()

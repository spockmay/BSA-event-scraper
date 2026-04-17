import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re


def scrape_scouting_calendar(org_key, categoryIds):
    """
    Scrapes all events from the Scouting Event calendar by making a direct
    API call and parsing the returned HTML to extract individual events.

    This function is tailored to the specific API endpoint and the HTML
    structure it returns, ensuring it retrieves the data correctly by
    parsing specific text patterns within the HTML.

    Args:
        org_key (str): The organization key to use for the API request.
        categoryIds (str): The string list of category ids to filter on

    Returns:
        list: A list of dictionaries, where each dictionary represents an event
              with keys for 'title', 'start', 'end', and 'url'.
        None: If the request fails.
    """
    url = "https://scoutingevent.com/inc/ajax_calendar.php"

    # Define all the parameters as seen in the provided URL.
    # The 'month', 'year', and 'TimeStamp' are made dynamic to work for the current date.
    now = datetime.now()
    # The TimeStamp format is specific to the website's needs
    timestamp_str = now.strftime(
        "%a %b %d %Y %H:%M:%S GMT-0400 (Eastern Daylight Time)"
    )

    # list of keywords to ignore in the title
    titles_to_ignore = [
        "Eagle Board",
        "SM Basic",
        "Sign-Up Event",
        "Loop Lab",
        "Wood Badge",
        "Roundtable",
        "Adventure Programs",
        "Marnoc Lodge",
        "Soaring Eagle District",
        "Summer Camp",
    ]

    params = {
        "showCalendar": org_key,
        "OrgKey": org_key,
        "view": "3",
        "districtIds": "",
        "categoryIds": categoryIds,
        "locationIds": "",
        "countyIds": "",
        "useCountySearchFlag": "1",
        "month": str(now.month),
        "year": str(now.year),
        "useHover": "1",
        "useOfficeClosing": "1",
        "useTickler": "1",
        "format": "4",
        "showCategory": "0",
        "timeWindow": "731",
        "usePaging": "0",
        "showHostedBy": "0",
        "showTime": "0",
        "partialDesc": "0",
        "titleOnly": "0",
        "partialDescSize": "0",
        "calendarTitle": "",
        "changeSelection": "1",
        "searchString": "",
        "SDATE": "",
        "EDATE": "",
        "nbrPerPage": "100",
        "pageNbr": "0",
        "TimeStamp": timestamp_str,
    }

    try:
        # Make the GET request to the API endpoint with the defined parameters
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all event elements using the provided class name
        event_elements = soup.find_all(
            "div",
            class_="col-xs-12 col-ms-6 col-sm-4 col-md-4 outlineLightGrid",
        )

        formatted_events = []
        for event in event_elements:
            # Initialize a dictionary for each event
            event_data = {
                "title": "No Title",
                "start": "N/A",
                "end": "N/A",
                "url": "No URL",
            }

            # Find the title, which is in an <h1> tag
            title_element = event.find("h1")
            if title_element:
                event_data["title"] = title_element.get_text(strip=True)

            # Check if the title contains any of the strings in the ignore list
            should_ignore = False
            for ignored_title in titles_to_ignore:
                if ignored_title.lower() in event_data["title"].lower():
                    should_ignore = True
                    break

            if should_ignore:
                continue

            # The URL is still associated with the anchor tag
            url_element = event.find("a", href=True)
            if url_element:
                event_data["url"] = url_element["href"]

            # Extract all text content from the event block
            text_content = event.get_text(strip=True).replace("\xa0", " ")

            # Use regular expressions to find patterns in the single-line string
            # Find the start and end dates
            start_match = re.search(
                r"Starts:\s*(\d{2}-\d{2}-\d{4})", text_content
            )
            if start_match:
                event_data["start"] = start_match.group(1)

            end_match = re.search(r"Ends:\s*(\d{2}-\d{2}-\d{4})", text_content)
            if end_match:
                event_data["end"] = end_match.group(1)

            formatted_events.append(event_data)

        return formatted_events

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except Exception as e:
        print(f"Error parsing HTML or data extraction: {e}")
        return None


if __name__ == "__main__":
    print("Scraping events from the Scouting Event calendar...")

    orgs = [
        ("Great Trail Council", "BSA433", "167,1566,707,257"),
        ("Lake Erie Council", "BSA440", "1030,1048,5592,1033"),
    ]

    for org in orgs:
        events = scrape_scouting_calendar(org[1], org[2])

        if events:
            print(f"{org[0]} events:")
            for event in events:
                print("-" * 20)
                print(f"Title: {event.get('title')}")
                print(f"Start: {event.get('start')}")
                print(f"End: {event.get('end')}")
                print(f"URL: {event.get('url')}")
            print("-" * 20)
            print("-" * 20)

        else:
            print("Failed to retrieve events.")

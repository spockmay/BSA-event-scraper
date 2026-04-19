import requests
from datetime import datetime, timedelta

FILTER = [
    "sm basic",
    "eagle scout",
    "birthday",
    "eagle board",
    "eagle bor",
    "baloo",
    "Stewards of beaumont",
    "wilderness engineers",
    "mobile climbing wall",
    "wood badge",
    "summer camp",
    "stem summer",
    "cub adventures",
    "rangemaster",
    "roundtable",
    "camp gray",
    "cubber",
    "stewards of firelands",
    "sacred texts",
    "badge lab",
    " day",
    "committee",
    "eagle project",
    "cub scout",
    "round table",
    "meeting",
    "popcorn",
    "huddle",
    "show-n-sell",
    "show and sell",
    "instructor",
    "marnoc lodge",
    "closed for",
    "distribution",
    "renewals",
    "commissioners",
    "pinewood derb",
    "flower sale",
    "swim check",
    "retreat",
    "banquet",
]


def scrape_scoutcal_json(id):
    try:
        url = "https://scoutcal.com/%s.json" % (id,)
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except Exception as e:
        print(f"Error parsing HTML or data extraction: {e}")
        return None


def is_event_timely(event, tstart, tend):
    if event.get("start", None) is None:
        print(event)
        return False
    if event["start"] >= tstart and event["start"] <= tend:
        return True
    return False


def is_event_meaningful(event):
    for filt in FILTER:
        if filt in event["title"].lower():
            return False
    return True


def json_to_event(json_event):
    # Initialize a dictionary for each event
    return {
        "title": json_event.get("EVENT_TITLE", "No Title"),
        "start": datetime.strptime(
            json_event.get("SDATE_FMT", "N/A"), "%Y%m%d"
        ),
        "end": datetime.strptime(json_event.get("EDATE_FMT", "N/A"), "%Y%m%d"),
        "url": json_event.get("URL", "No URL"),
    }


def print_event(event):
    print("-" * 20)
    print(f"Title: {event.get('title')}")
    print(f"Start: {event.get('start')}")
    print(f"End: {event.get('end')}")
    print(f"URL: {event.get('url')}")


def main():
    councils = [
        ("Lake Erie Council", "20364"),
        ("Great Trail Council", "19108"),
    ]

    t_now = datetime.now()
    t_end = t_now + timedelta(weeks=52)

    events = []

    print("Scraping events from the Scouting Event calendar...")

    for council in councils:
        j = scrape_scoutcal_json(council[1])
        print(council[0])
        for json_event in j:
            event = json_to_event(json_event)
            if is_event_meaningful(event):
                if is_event_timely(event, t_now, t_end):
                    events.append(event)

        for event in events:
            print_event(event)


if __name__ == "__main__":
    main()

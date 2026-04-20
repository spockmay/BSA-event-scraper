import requests
from datetime import datetime, timedelta

from event import Event


def scrape_scoutcal_json(id: str) -> dict:
    """
    Scrape the JSON event data from the Council with the provided id.
    This only works for councils that use Black Pug's scoutcalendar site

    :param id: the ID of the council's JSON calendar
    :type id: str
    :return: all of the council events
    :rtype: dict
    """
    try:
        url = "https://scoutcal.com/%s.json" % (id,)
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return {}
    except Exception as e:
        print(f"Error parsing HTML or data extraction: {e}")
        return {}


def json_to_event(json_event: dict) -> Event:
    """
    Takes an individual scoutcal event dictionary and converts it to an Event object

    :param json_event: the json scoutcal event
    :type json_event: dict
    :return: the Event object for the event
    :rtype: Event
    """
    return Event(
        title=json_event.get("EVENT_TITLE", "No Title"),
        start=datetime.strptime(json_event.get("SDATE_FMT", "N/A"), "%Y%m%d"),
        end=datetime.strptime(json_event.get("EDATE_FMT", "N/A"), "%Y%m%d"),
        url=json_event.get("URL", "No URL"),
    )


if __name__ == "__main__":
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
            if event.is_meaningful():
                if event.is_timely(t_now, t_end):
                    events.append(event)

        for event in events:
            print("-" * 20)
            print(event)

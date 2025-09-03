import requests
import json
from datetime import datetime, timedelta


def scrape_scouting_calendar():
    """
    Scrapes all events from a specific calendar API endpoint that returns
    JSON data. It then extracts individual events and applies a title filter.

    Args:
    Returns:
        list: A list of dictionaries, where each dictionary represents an event
              with keys for 'title', 'start', 'end', and 'url'.
        None: If the request fails.
    """
    # Define a list of titles to ignore
    titles_to_ignore = [
        "Eagle Boards",
        "SM Basic",
        "Sign-Up Event",
        "Loop Lab",
        "Wood Badge",
        "Eagle BOR",
        "Pipestone",
        "Marksmanship",
    ]

    color_filter = "#008000"

    start_date = datetime.now()
    formatted_events = []

    for i in range(0, 8):
        end_date = start_date + timedelta(days=35)

        url = (
            f"https://www.buckeyecouncil.org/wp-content/plugins/councilware/calendar/render.php"
            f"?calendarID=7&start={start_date.strftime('%Y-%m-%d')}&end={end_date.strftime('%Y-%m-%d')}"
            f"&_={int(datetime.now().timestamp() * 1000)}"
        )

        try:
            # Make the GET request to the API endpoint
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            events_json = response.json()

            # The JSON data is a dictionary where the values are the event objects.
            for event_data in events_json:
                event_title = event_data.get("title", "No Title")

                # Check if the title contains any of the strings in the ignore list
                should_ignore = False
                for ignored_title in titles_to_ignore:
                    if ignored_title.lower() in event_title.lower():
                        should_ignore = True
                        break

                if event_data.get("color", "#008000") != color_filter:
                    should_ignore = True

                if should_ignore:
                    continue

                # Extract the necessary data from the JSON object
                event_url = event_data.get("eventPageURL", "No URL")

                # The start and end dates contain time information, so we split to get only the date.
                event_start = event_data.get("start", "N/A").split("T")[0]
                event_end = event_data.get("end", "N/A").split("T")[0]

                formatted_events.append(
                    {
                        "title": event_title,
                        "start": event_start,
                        "end": event_end,
                        "url": event_url,
                    }
                )
            start_date = end_date + timedelta(days=1)
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    return formatted_events


if __name__ == "__main__":
    print("Scraping events from the Buckeye Council calendar...")
    events = scrape_scouting_calendar()

    if events:
        print(f"Found {len(events)} events:")
        for event in events:
            print("-" * 20)
            print(f"Title: {event.get('title')}")
            print(f"Start: {event.get('start')}")
            print(f"End: {event.get('end')}")
            print(f"URL: {event.get('url')}")
    else:
        print("Failed to retrieve events.")

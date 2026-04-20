from datetime import datetime, timedelta

from buckeye import scrape_buckeye_calendar
from scoutingevent_json import scrape_scoutcal_json


# Scrape Buckeye
print("Scraping events from the Buckeye Council calendar...")
events = scrape_buckeye_calendar()

if events:
    print(f"Found {len(events)} events")
    for event in events:
        print("-" * 20)
        print(event)
else:
    print("Failed to retrieve events.")

# Scrape scoutcal councils
councils = [
    ("Lake Erie Council", "20364"),
    ("Great Trail Council", "19108"),
]

t_now = datetime.now()
t_end = t_now + timedelta(weeks=52)

print("Scraping events from the Scouting Event calendar...")

for council in councils:
    events = scrape_scoutcal_json(council[1], t_now, t_end)
    print(council[0])
    for event in events:
        print("-" * 20)
        print(event)

from datetime import datetime, timedelta

from buckeye import scrape_buckeye_calendar
from scoutingevent_json import scrape_scoutcal_json

t_now = datetime.now()
t_end = t_now + timedelta(weeks=52)

all_events = []

# Scrape Buckeye
print("Scraping events from the Buckeye Council's calendar...")
events = scrape_buckeye_calendar(t_now, t_end)
print("  %s events found." % len(events))
all_events.extend(events)

# Scrape scoutcal councils
councils = [
    ("Lake Erie Council", "LEC", "20364"),
    ("Great Trail Council", "GTC", "19108"),
]

for council in councils:
    print(f"Scraping events from {council[0]}'s calendar...")
    events = scrape_scoutcal_json(council[2], council[1], t_now, t_end)
    print("  %s events found." % len(events))
    all_events.extend(events)

# sort events
all_events.sort(key=lambda x: x.start)

# print events
for event in all_events:
    print("-" * 20)
    print(event)

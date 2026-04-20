![AI-Free](https://img.shields.io/badge/AI--Free-Handcrafted-orange)

# BSA event scraper
Scrapes BSA council events into a single report. Our troop uses this to help with semi-annual planning. 

## bsa_events.py
This script calls a scraper for three councils (Buckeye, Great Trail, and Lake Erie) and prints the events of interest and within the desired time range to the console. 

Lake Erie and Great Trail both use the scoutingevent.com by Black Pug Software. They actually have a really nice map on their homepage that shows which councils use their software and which don't (https://scoutingevent.com/indexMap.php). For any council that uses it you can trivially scrape their events by doing the following:
1) From the above map, click on the council you are interested in.
2) On the right side of the page, below the Sign In button is a Subscribe button. Click it then "json". A box will pop up saying "JSON Feed URL". Copy the number out of that url.

Buckeye Council is a more traditional, custom, scraper. 

## event.py
There is a list of words to filter out so that you can ignore events that are irrelevant to your group (e.g. Wood Badge). 

## scoutingevent_json.py
This is the scraper for the Black Pug software (https://scoutingevent.com). This can be used for any council that utilizes that platform.

## buckeye.py
Custom scraper for the Buckeye Council website.

---

Development Note: This project is 100% human-authored. No Large Language Models (LLMs) or generative AI tools were used in the writing of this code, logic, or documentation.
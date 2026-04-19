# BSA event scraper
Scrapes BSA council events into a single report. Our troop uses this to help with semi-annual planning. 

To use, simply run the python script for the council desired. Currently there are three councils supported: Buckeye, Great Trail, and Lake Erie.

Lake Erie and Great Trail both use the scoutingevent.com by Black Pug Software. They actually have a really nice map on their homepage that shows which councils use their software and which don't (https://scoutingevent.com/indexMap.php). For any council that uses it you can trivially scrape their events by doing the following:
1) From the above map, click on the council you are interested in.
2) On the right side of the page, below the Sign In button is a Subscribe button. Click it then "json". A box will pop up saying "JSON Feed URL". Copy the number out of that url.

Buckeye Council is a more traditional, custom, scraper. 

There is a list of words to filter out so that you can ignore events that are irrelevant to your group (e.g. Wood Badge). 
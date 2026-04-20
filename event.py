from datetime import datetime

FILTER = [
    "no title",
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
    "sign-ip event",
    "loop lab",
    "pipestone",
    "marksmanship",
]


class Event:
    title = "No Title"
    start = None
    end = None
    url = "No URL"

    def __init__(
        self,
        title: str = "No Title",
        start: datetime | None = None,
        end: datetime | None = None,
        url: str = "No URL",
    ) -> None:
        self.title = title
        self.start = start
        self.end = end
        self.url = url

    def __repr__(self) -> str:
        if self.start is not None and self.end is not None:
            t_start = self.start.strftime("%Y-%m-%d")
            t_end = self.end.strftime("%Y-%m-%d")
        return (
            f"Title: {self.title}\n"
            f"Start: {t_start}\n"
            f"End: {t_end}\n"
            f"URL: {self.url}"
        )

    def is_timely(self, tstart: datetime, tend: datetime) -> bool:
        """
        Determines if the event starts between the two datetime objects provided

        :param tstart: Earliest date you want the event to start
        :type tstart: datetime
        :param tend: Latest date you want the event to start
        :type tend: datetime
        :return: Is the event start date between the two dates provided
        :rtype: bool
        """
        if self.start is None:
            return False
        if self.start >= tstart and self.start <= tend:
            return True
        return False

    def is_meaningful(self) -> bool:
        """
        Does the event's title not contain any words in the filter list

        :return: Is the event meaningful?
        :rtype: bool
        """
        t = self.title.lower()
        for filt in FILTER:
            if filt in t:
                return False
        return True

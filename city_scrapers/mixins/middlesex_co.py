from datetime import datetime

from city_scrapers_core.constants import BOARD, CITY_COUNCIL, COMMITTEE, NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.relativedelta import relativedelta
from scrapy.http import FormRequest


class MiddlesexCoMixinMeta(type):
    """
    Metaclass that enforces the implementation of required static
    variables in child classes that inherit from MiddlesexCoMixin.
    """

    def __init__(cls, name, bases, dct):
        required_static_vars = ["agency", "name", "committee_id"]
        missing_vars = [var for var in required_static_vars if var not in dct]

        if missing_vars:
            missing_vars_str = ", ".join(missing_vars)
            raise NotImplementedError(
                f"{name} must define the following static variable(s): {missing_vars_str}."  # noqa
            )
        super().__init__(name, bases, dct)


class MiddlesexCoMixin(CityScrapersSpider, metaclass=MiddlesexCoMixinMeta):
    """
    Spider mixin for Middlesex County, NJ. This mixin is intended to be
    used as a base class for spiders that scrape meeting data from the
    PrimeGov API for the agency.
    """

    timezone = "America/New_York"
    location = {
        "name": "TBD",
        "address": "",
    }
    meeting_page = "https://middlesexcountynj.primegov.com/public/portal"
    name = None
    agency = None
    committee_id = None

    def start_requests(self):
        """
        Prepare and send a POST request to the PrimeGov API to retrieve
        meeting data for the committee specified by the `committee_id`.
        """
        # Calculate dates for one month prior and one year ahead
        today = datetime.today()
        one_month_prior = today - relativedelta(months=1)
        one_year_ahead = today + relativedelta(years=1)

        # Format dates as "MM/DD/YYYY"
        meeting_date_from = one_month_prior.strftime("%m/%d/%Y")
        meeting_date_to = one_year_ahead.strftime("%m/%d/%Y")

        # Form data to be sent with the POST request, including the calculated dates
        formdata = {
            "CommitteeId": str(self.committee_id),
            "MeetingDateFrom": meeting_date_from,
            "MeetingDateTo": meeting_date_to,
        }

        url = "https://middlesexcountynj.primegov.com/api/v2/PublicPortal/search"
        yield FormRequest(url, method="POST", formdata=formdata, callback=self.parse)

    def parse(self, response):
        """
        Parse meeting JSON data from the PrimeGov API.
        """
        meetings = response.json()
        for meeting in meetings:
            title = meeting["meetingTitle"].strip()
            start = datetime.fromisoformat(meeting["meetingDate"])
            links = self._parse_links(meeting)
            meeting_item = Meeting(
                title=title,
                description=self._parse_description(links),
                classification=self._parse_classification(title),
                start=start,
                end=None,
                all_day=False,
                time_notes="",
                location=self.location,
                links=links,
                source=self.meeting_page,
            )
            meeting_item["status"] = self._get_status(meeting_item)
            meeting_item["id"] = self._get_id(meeting_item)
            yield meeting_item

    def _parse_classification(self, title):
        """Generate classification based on meeting title."""
        if not title:
            return NOT_CLASSIFIED
        clean_title = title.lower()
        if "board" in clean_title:
            return BOARD
        elif "committee" in clean_title:
            return COMMITTEE
        elif "council" in clean_title:
            return CITY_COUNCIL
        else:
            return NOT_CLASSIFIED

    def _parse_links(self, meeting):
        """Build links from data in documentList"""
        document_list = meeting.get("documentList", [])
        links = []
        for doc in document_list:
            templateName = doc.get("templateName", "")
            compileOutputType = doc.get("compileOutputType", "")
            templateId = doc.get("templateId", "")
            links.append(
                {
                    "title": templateName,
                    "href": f"https://middlesexcountynj.primegov.com/Public/CompiledDocument?meetingTemplateId={templateId}&compileOutputType={compileOutputType}",  # noqa
                }
            )
        return links

    def _parse_description(self, links):
        """Generates description. Meeting data does not include description
        information but the attachments may contain the description and
        location information so we reference it again here."""
        for link in links:
            if (
                "agenda" in link["title"].lower()
                or "meeting notice" in link["title"].lower()
            ):
                return f"Check the {link['title'].lower()} for description and location information: {link['href']}"  # noqa
        return ""

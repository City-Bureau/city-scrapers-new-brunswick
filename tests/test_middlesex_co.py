import pytest
from city_scrapers_core.constants import BOARD, CITY_COUNCIL, COMMITTEE, NOT_CLASSIFIED
from scrapy.http import FormRequest

from city_scrapers.mixins.middlesex_co import (  # Adjust the import path accordingly
    MiddlesexCoMixin,
)


class TestMiddlesexCoMixin:
    @pytest.fixture
    def mixin(self):
        class TestSpider(MiddlesexCoMixin):
            name = "test_spider"
            agency = "Test Agency"
            committee_id = "123"

        return TestSpider()

    def test_parse_classification(self, mixin):
        assert mixin._parse_classification("Board Meeting") == BOARD
        assert mixin._parse_classification("Committee Discussion") == COMMITTEE
        assert mixin._parse_classification("City Council") == CITY_COUNCIL
        assert mixin._parse_classification("Unspecified Event") == NOT_CLASSIFIED

    def test_start_requests(self, mixin):
        request_generator = mixin.start_requests()
        request = next(request_generator)
        assert isinstance(request, FormRequest)
        assert (
            request.url
            == "https://middlesexcountynj.primegov.com/api/v2/PublicPortal/search"
        )
        assert request.method == "POST"
        # Check if the committee_id is correctly included in the
        # body of the POST request
        expected_body = f"CommitteeId={mixin.committee_id}"
        # FormRequest body is byte type, decode it for comparison
        assert expected_body in request.body.decode("utf-8")

    def test_parse_links(self, mixin):
        meeting = {
            "documentList": [
                {
                    "templateName": "Agenda",
                    "compileOutputType": "PDF",
                    "templateId": "456",
                }
            ]
        }
        links = mixin._parse_links(meeting)
        assert len(links) == 1
        assert links[0]["title"] == "Agenda"
        assert links[0]["href"].startswith(
            "https://middlesexcountynj.primegov.com/Public/CompiledDocument"
        )

    def test_parse_description(self, mixin):
        links = [
            {"title": "Agenda", "href": "http://example.com/agenda.pdf"},
            {"title": "Meeting Notice", "href": "http://example.com/notice.pdf"},
        ]
        description = mixin._parse_description(links)
        assert (
            "Check the agenda" in description
            or "Check the meeting notice" in description
        )

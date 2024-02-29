from datetime import datetime
from os.path import dirname, join

import pytest  # noqa
from city_scrapers_core.constants import BOARD, TENTATIVE  # noqa
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.middlesex_co import MiddlesexCoPBSpider

test_response = file_response(
    join(dirname(__file__), "files", "middlesex_co_pb.json"),
    url="https://middlesexcountynj.primegov.com/public/portal",
)
spider = MiddlesexCoPBSpider()

freezer = freeze_time("2024-02-22")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "Planning Board"


def test_description():
    assert (
        parsed_items[0]["description"]
        == "Check the meeting notice for description and location information: https://middlesexcountynj.primegov.com/Public/CompiledDocument?meetingTemplateId=3434&compileOutputType=1"  # noqa
    )


def test_start():
    assert parsed_items[0]["start"] == datetime(2025, 1, 14, 15, 15)


def test_end():
    assert parsed_items[0]["end"] is None


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert parsed_items[0]["id"] == "middlesex_co_pb/202501141515/x/planning_board"


def test_status():
    assert parsed_items[0]["status"] == TENTATIVE


def test_location():
    assert parsed_items[0]["location"] == {"name": "TBD", "address": ""}


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://middlesexcountynj.primegov.com/public/portal"
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "title": "Meeting Notice",
            "href": "https://middlesexcountynj.primegov.com/Public/CompiledDocument?meetingTemplateId=3434&compileOutputType=1",  # noqa
        }
    ]


def test_classification():
    assert parsed_items[0]["classification"] == BOARD


def test_all_day():
    assert parsed_items[0]["all_day"] is False

from uuid import uuid4
from datetime import datetime, timezone, timedelta

import pytest
from freezegun import freeze_time
from django.test import Client

from api.models import OhshownEvent, Image, ReportRecord


FAKE_IMGUR_PATH = "https://i.imgur.com/RxArJUc.png"


@pytest.mark.django_db
class TestPostFactoryImageView:

    @pytest.fixture(autouse=True)
    def setUp(self, client):
        self.cli = client
        self.factory = OhshownEvent.objects.create(
            name="test_factory",
            lat=24,
            lng=121,
            sight_see_date_time=datetime(2019, 10, 11, 11, 11, 11),
            status_time=datetime(2019, 11, 11, 11, 11, 11, tzinfo=timezone(timedelta(hours=8))),
            display_number=666,
        )
        self.nickname = "somebody"
        self.contact = "0900000000"
        self.fake_url = "https://i.imgur.com/123456.png"
        self.fake_lat = 23.12
        self.fake_lng = 121.5566
        self.fake_datetime_str = "2020:03:21 12:33:59"
        self.fake_deletehash = "asdjiwenvnxcvj;"
        self.fake_datetime = datetime.strptime(
            self.fake_datetime_str,
            "%Y:%m:%d %H:%M:%S",
        ).replace(tzinfo=timezone(timedelta(hours=8)))
        self.post_body = {
            "url": self.fake_url,
            "Latitude": self.fake_lat,
            "Longitude": self.fake_lng,
            "DateTimeOriginal": self.fake_datetime_str,
            "nickname": self.nickname,
            "contact": self.contact,
            "deletehash": self.fake_deletehash,
        }

    def test_image_upload_db_correct(self):
        test_time = datetime(2019, 11, 11, 11, 11, 11, tzinfo=timezone(timedelta(hours=8)))
        with freeze_time(test_time):
            resp = self.cli.post(
                f"/api/factories/{self.factory.id}/images",
                self.post_body,
                content_type="application/json",
            )

        assert resp.status_code == 200
        resp_data = resp.json()

        img_id = resp_data["id"]
        img = Image.objects.get(pk=img_id)
        assert img.image_path == self.fake_url
        assert img.created_at == test_time
        assert img.orig_time == self.fake_datetime
        assert img.orig_lat == self.fake_lat
        assert img.orig_lng == self.fake_lng
        assert img.factory_id == self.factory.id

        report_record_id = img.report_record_id
        assert report_record_id is not None
        report_record = ReportRecord.objects.get(pk=report_record_id)
        assert report_record.factory_id == self.factory.id
        assert report_record.action_type == "POST_IMAGE"
        assert report_record.nickname == self.nickname
        assert report_record.contact == self.contact

    def test_return_400_if_url_not_provided(self):
        wrong_body = {
            "Latitude": self.fake_lat,
            "Longitude": self.fake_lng,
            "DateTimeOriginal": self.fake_datetime_str,
            "nickname": self.nickname,
            "contact": self.contact,
        }
        resp = self.cli.post(
            f"/api/factories/{self.factory.id}/images",
            wrong_body,
            content_type="application/json",
        )

        assert resp.status_code == 400

    def test_return_400_if_factory_id_not_exist(self):
        cli = Client()
        not_exist_factory_id = uuid4()
        resp = cli.post(
            f"/api/factories/{not_exist_factory_id}/images",
            self.post_body,
            content_type="application/json",
        )

        assert resp.status_code == 400
        expected_msg = f"Factory ID {not_exist_factory_id} does not exist."
        assert resp.content == expected_msg.encode("utf8")

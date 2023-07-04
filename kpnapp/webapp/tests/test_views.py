from django.test import TestCase
from webapp.models import ContactList
from webapp.views import (
    fetch_csv_entries,
    path_to_image_html,
    get_html_table_of_contact_list,
    get_contact_list,
)
from unittest.mock import MagicMock, patch
import pytest


class ContactListTestCase(TestCase):
    def setUp(self):
        self.contact_list = ContactList.objects.create(
            firstname="peer",
            lastname="citroen",
            street="appelstraat",
            zip="123",
            city="Utrecht",
            image="https://some.image.somewhere",
        )

    @patch("webapp.views.requests")
    def test_fetch_csv_entries(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "firstname,lastname,street,zip,city,image\r\npeer,citroen,appelstraat,123,Utrecht,https://some.image.somewhere"

        mock_requests.get.return_value = mock_response
        result_response = fetch_csv_entries(mock_requests)

        self.assertEqual(result_response, mock_response.text)

    def test_get_html_table_of_contact_list(self):
        expected = '<table class="dataframe"> <thead> <tr style="text-align: right;"> <th></th> <th>id</th> <th>firstname</th> <th>lastname</th> <th>street</th> <th>zip</th> <th>city</th> <th>image</th> </tr> </thead> <tbody> <tr> <th>0</th> <td>1</td> <td>peer</td> <td>citroen</td> <td>appelstraat</td> <td>123</td> <td>Utrecht</td> <td><img src="https://some.image.somewhere" style=max-height:80px;"/></td> </tr> </tbody> </table>'
        result = " ".join(get_html_table_of_contact_list()["df"].split())
        self.assertEqual(result, expected)

    def test_get_contact_list(self):
        result = get_contact_list(
            "firstname,lastname,street,zip,city,image\r\npeer,citroen,appelstraat,123,Utrecht,https://some.image.somewhere"
        )[0]
        expected = self.contact_list
        self.assertEqual(result.city, expected.city)
        self.assertEqual(result.image, expected.image)


@pytest.mark.parametrize(
    "input,expected", [("some_path", '<img src="some_path" style=max-height:80px;"/>')]
)
def test_path_to_image_html(input, expected):
    result = path_to_image_html(path=input)
    assert result == expected

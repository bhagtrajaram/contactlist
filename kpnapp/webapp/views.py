import requests
from io import StringIO
import pandas as pd
from .decorators import handle_connection_exception
from .models import ContactList
from django.shortcuts import render
from kpnapp.settings import DATA_ENDPOINT
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def users(request):
    response = fetch_csv_entries(
        request=request,
    )
    queryset = ContactList.objects.all()

    if queryset.exists() == False:
        """store only image links"""
        if not isinstance(response, dict):
            ContactList.objects.bulk_create(get_contact_list(response=response))
            logger.info(f"http response(csv-data):'{response}'")
        else:
            logger.error(f"http response(csv-data):'{response}'")

    """render images"""
    return render(
        request, "contact_list.html", context=get_html_table_of_contact_list()
    )


def get_contact_list(response: str) -> list[ContactList]:
    """parse http response into dataframe: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html"""
    df = pd.read_csv(StringIO(response), sep=",")
    row_iter = df.iterrows()
    contact_list: list[ContactList] = [
        ContactList(
            firstname=row["firstname"],
            lastname=row["lastname"],
            street=row["street"],
            zip=row["zip"],
            city=row["city"],
            image=row["image"],
        )
        for index, row in row_iter
    ]
    return contact_list


def get_html_table_of_contact_list() -> dict[str, str]:
    item = ContactList.objects.all().values()
    df = pd.DataFrame(item)
    data = {
        "df": df.to_html(
            border=0, escape=False, formatters=dict(image=path_to_image_html)
        )
    }
    return data


@handle_connection_exception
def fetch_csv_entries(request: requests.Request) -> str:
    response = requests.get(DATA_ENDPOINT)
    return response.text


def path_to_image_html(path) -> str:
    return '<img src="' + path + '" style=max-height:80px;"/>'

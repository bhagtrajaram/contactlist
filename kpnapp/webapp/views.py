import requests
from io import StringIO
import pandas as pd
from .decorators import handle_view_exception
from .models import ContactList
from django.shortcuts import render
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def users(request):
    response = fetch_csv_entries(
        request=request,
    )
    logger.info(f"http response(csv-data):'{response.text}'")
    queryset = ContactList.objects.all()

    if queryset.exists() == False:
        """store only image links"""
        ContactList.objects.bulk_create(get_contact_list(response=response.text))

    """render images"""
    return render(
        request, "contact_list.html", context=get_html_table_of_contact_list()
    )


def get_contact_list(response: str) -> list[ContactList]:
    """parse http response into dataframe: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html"""
    logger.info(f"http response(csv-data):'{response}'")
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


@handle_view_exception
def fetch_csv_entries(request: requests.Request) -> requests.Response:
    response = requests.get(
        "https://docs.google.com/spreadsheets/d/1A77-RWx7x8PK2uDm_1XlXyCy2ID9-9lhwix8wPDd5X0/pub?gid=0&single=true&output=csv"
    )
    return response


def path_to_image_html(path) -> str:
    return '<img src="' + path + '" style=max-height:80px;"/>'

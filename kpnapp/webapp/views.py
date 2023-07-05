import requests
from io import StringIO
import pandas as pd
import pandera as pa
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
            contact_list: list[ContactList] = get_contact_list(response=response)
            if contact_list:
                logger.info(f"http response(csv-data):'{response}'")
                logger.info(f"doing bulk_create on database using:\n'{contact_list}")
                ContactList.objects.bulk_create(contact_list)
        else:
            logger.error(f"http response(csv-data):'{response}'")

    """render images"""
    return render(
        request, "contact_list.html", context=get_html_table_of_contact_list()
    )


def get_contact_list(response: str) -> list[ContactList]:
    contact_list: list[ContactList] = []
    """parse http response into dataframe: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html"""
    df = pd.read_csv(StringIO(response), sep=",")
    if validate_schema(df=df):
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


def validate_schema(df: pd.DataFrame) -> bool:
    schema = pa.DataFrameSchema(
        {
            "firstname": pa.Column(object, required=True),
            "lastname": pa.Column(object, required=True),
            "street": pa.Column(object, required=True),
            "zip": pa.Column(int, required=True),
            "city": pa.Column(object, required=True),
            "image": pa.Column(object, required=True, nullable=True),
        }
    )

    try:
        schema(df)
        schema_valid = True
        logger.info(f"schema validation csv-data:'{schema_valid}'")
    except pa.errors.SchemaError as error:
        schema_valid = False
        logger.error(f"schema validation csv-data:'{schema_valid}'\n'{error}'")
    return schema_valid

from django.shortcuts import render
import requests
from io import StringIO
import pandas as pd
from json import loads

def users(request):
    response = requests.get('https://docs.google.com/spreadsheets/d/1A77-RWx7x8PK2uDm_1XlXyCy2ID9-9lhwix8wPDd5X0/pub?gid=0&single=true&output=csv')
    df = pd.read_csv(StringIO(response.text), sep=",")
    result = df.to_json(orient="records")
    users = loads(result)
    return render(request, "users.html", {'users': users})
    pass
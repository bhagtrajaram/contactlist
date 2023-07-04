### Getting Started

1. Clone the project
2. Make sure your in the root of the cloned project
3. Run the following command '*make run*'

Output:
```
July 04, 2023 - 16:15:29
Django version 4.2.2, using settings 'kpnapp.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.

INFO:webapp.views:http response(csv-data):'firstname,lastname,street,zip,city,image
Travis,Fox,1859 Clair Street,76541,Killeen,https://cdn1.iconfinder.com/data/icons/user-pictures/100/male3-512.png
Leontine,Kasmi,1009 Kinney Street,1201,Pittsfield,https://cdn1.iconfinder.com/data/icons/user-pictures/100/female1-512.png
Shanon,Gilsing,3644 Seneca Drive,97071,Woodburn,http://www.google.com
Miray,Dibbets,"489 Oakridge Lane, ""test""",31201,Macon,'
[04/Jul/2023 16:15:38] "GET / HTTP/1.1" 200 2292
```

*This project has been created in Pycharm so you can leverage this to start your docker container and run the unittests.*

### Notes
pytest

- cli: cd ~/PycharmProjects/kpn_python_assignment/kpnapp
- Pycharm-task: pytest in /

prepare database
- python manage.py test
- python manage.py makemigrations
- python manage.py migrate

flush database
- python manage.py flush

Data endpoint
- ~/PycharmProjects/kpn_python_assignment/kpnapp/kpnapp/settings.py
- DATA_ENDPOINT = '<url>'
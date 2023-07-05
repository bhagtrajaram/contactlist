### Getting Started

1. Clone the project
2. Make sure your in the root of the cloned project
3. Run the following command '*make run*'

Output:
```
$ make run
docker build --tag kpn/datasource .
[+] Building 20.3s (16/16) FINISHED                                                                                                                                                                                                                                                                                                                                                                                                       
 => [internal] load build definition from Dockerfile                                                                                                                                                                                                                                                                                                                                                                                 0.0s
 => => transferring dockerfile: 37B                                                                                                                                                                                                                                                                                                                                                                                                  0.0s
 => [internal] load .dockerignore                                                                                                                                                                                                                                                                                                                                                                                                    0.0s
 => => transferring context: 34B                                                                                                                                                                                                                                                                                                                                                                                                     0.0s
 => [internal] load metadata for docker.io/library/python:3.11.4-slim                                                                                                                                                                                                                                                                                                                                                                0.8s
 => [base 1/6] FROM docker.io/library/python:3.11.4-slim@sha256:364ee1a9e029fb7b60102ae56ff52153ccc929ceab9aa387402fe738432d24cc                                                                                                                                                                                                                                                                                                     0.0s
 => => resolve docker.io/library/python:3.11.4-slim@sha256:364ee1a9e029fb7b60102ae56ff52153ccc929ceab9aa387402fe738432d24cc                                                                                                                                                                                                                                                                                                          0.0s
 => [internal] load build context                                                                                                                                                                                                                                                                                                                                                                                                    0.0s
 => => transferring context: 14.43kB                                                                                                                                                                                                                                                                                                                                                                                                 0.0s
 => CACHED [base 2/6] RUN adduser --system appuser --home /home/appuser && addgroup --system appgroup && adduser appuser appgroup &&     chown -R appuser:appgroup /opt                                                                                                                                                                                                                                                              0.0s
 => [base 3/6] COPY --chown=appuser:appgroup . /usr/src/app                                                                                                                                                                                                                                                                                                                                                                          0.0s
 => [base 4/6] WORKDIR /usr/src/app                                                                                                                                                                                                                                                                                                                                                                                                  0.0s
 => [base 5/6] RUN python3 -m venv /opt/venv                                                                                                                                                                                                                                                                                                                                                                                         2.4s
 => [base 6/6] RUN . /opt/venv/bin/activate &&     python -m pip install --upgrade pip &&     pip install -r /usr/src/app/requirements/requirements-kpnapp.txt     -r /usr/src/app/requirements/requirements-testing.txt                                                                                                                                                                                                            10.4s
 => [runtime 1/5] COPY --from=base /opt/venv /opt/venv                                                                                                                                                                                                                                                                                                                                                                               1.5s
 => [runtime 2/5] WORKDIR /usr/src/app                                                                                                                                                                                                                                                                                                                                                                                               0.0s 
 => [runtime 3/5] COPY --from=base /usr/src/app /usr/src/app                                                                                                                                                                                                                                                                                                                                                                         0.0s 
 => [runtime 4/5] WORKDIR /usr/src/app/kpnapp                                                                                                                                                                                                                                                                                                                                                                                        0.0s 
 => [runtime 5/5] RUN . /opt/venv/bin/activate &&     python manage.py test &&     python manage.py makemigrations &&     python manage.py migrate &&     pytest -vvv                                                                                                                                                                                                                                                                3.6s 
 => exporting to image                                                                                                                                                                                                                                                                                                                                                                                                               1.4s 
 => => exporting layers                                                                                                                                                                                                                                                                                                                                                                                                              1.4s 
 => => writing image sha256:e971867fccea1ae946c9b9f537562b93873ce93979d31ada722fb740ad5b8c4f                                                                                                                                                                                                                                                                                                                                         0.0s 
 => => naming to docker.io/kpn/datasource                                                                                                                                                                                                                                                                                                                                                                                            0.0s 
docker container run -p 8000:8000 kpn/datasource                                                                                                                                                                                                                                                                                                                                                                                          
Watching for file changes with StatReloader                                                                                                                                                                                                                                                                                                                                                                                               
Performing system checks...

System check identified no issues (0 silenced).
July 05, 2023 - 10:50:45
Django version 4.2.2, using settings 'kpnapp.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.

INFO:webapp.views:schema validation csv-data:'True'
INFO:webapp.views:http response(csv-data):'firstname,lastname,street,zip,city,image
Travis,Fox,1859 Clair Street,76541,Killeen,https://cdn1.iconfinder.com/data/icons/user-pictures/100/male3-512.png
Leontine,Kasmi,1009 Kinney Street,1201,Pittsfield,https://cdn1.iconfinder.com/data/icons/user-pictures/100/female1-512.png
Shanon,Gilsing,3644 Seneca Drive,97071,Woodburn,http://www.google.com
Miray,Dibbets,"489 Oakridge Lane, ""test""",31201,Macon,'
INFO:webapp.views:doing bulk_create on database using:
'[<ContactList: Travis-Fox>, <ContactList: Leontine-Kasmi>, <ContactList: Shanon-Gilsing>, <ContactList: Miray-Dibbets>]
[05/Jul/2023 10:50:57] "GET / HTTP/1.1" 200 2292
[05/Jul/2023 10:50:58] "GET /nan HTTP/1.1" 200 2292
```
url to access: http://127.0.0.1:8000/

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
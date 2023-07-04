FROM python:3.11.4-slim as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV USER=appuser
ENV ROOT_USER=root
ENV GROUP=appgroup
ENV BASE_APP_DIR=/opt
ENV APPDIR=/usr/src/app
ENV PIP_CACHE=/nonexistent/.cache/pip

RUN adduser --system $USER --home /home/$USER && addgroup --system $GROUP && adduser $USER $GROUP && \
    chown -R $USER:$GROUP $BASE_APP_DIR

USER $USER
COPY --chown=$USER:$GROUP . $APPDIR
WORKDIR $APPDIR

RUN python3 -m venv $VIRTUAL_ENV

RUN . $VIRTUAL_ENV/bin/activate && \
    python -m pip install --upgrade pip && \
    pip install -r $APPDIR/requirements/requirements-kpnapp.txt \
    -r $APPDIR/requirements/requirements-testing.txt

FROM base as runtime

ENV VIRTUAL_ENV=/opt/venv
ENV APPDIR=/usr/src/app

USER $USER
COPY --from=base $VIRTUAL_ENV $VIRTUAL_ENV

WORKDIR $APPDIR
COPY --from=base $APPDIR $APPDIR

WORKDIR /usr/src/app/kpnapp
RUN . $VIRTUAL_ENV/bin/activate && \
    python manage.py test && \
    python manage.py makemigrations && \
    python manage.py migrate && \
    pytest -vvv

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
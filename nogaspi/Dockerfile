FROM python:3.10

ARG WD

WORKDIR /usr/src/app
#COPY ./Nogaspi/nogaspi .
#COPY ./assets ./assets

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pycryptodome

WORKDIR "/usr/src/app/${WD}"
#WORKDIR "/usr/src/app"

CMD [ "python", "nogaspi/app.py" ]
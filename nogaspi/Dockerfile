FROM python:3.10

ARG WD

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR "/usr/src/app/${WD}"
#COPY . .
CMD [ "python", "nogaspi/app.py" ]
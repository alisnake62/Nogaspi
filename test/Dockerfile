FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest

#COPY . .
WORKDIR /usr/src/app/Nogaspi/test
CMD ["pytest"]
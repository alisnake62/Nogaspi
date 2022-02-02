FROM python:3.10

ARG WD

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest

#COPY . .
WORKDIR "/usr/src/app/${WD}/test"
CMD ["pytest"]
FROM python:3.8

RUN apt-get update

RUN apt-get install -y build-essential mono-mcs

ENV VIRTUAL_ENV=/opt/venv

RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY Code/requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY Code/src/ .
COPY Artifacts/ .
COPY Data/ .

EXPOSE 9000

CMD ["python", "app.py"]
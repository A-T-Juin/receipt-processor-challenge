FROM python:3.9.9

ENV PYTHONBUFFERED 1

# upgrade pip
RUN pip install --upgrade pip

# establish work directory
WORKDIR /app

# copy and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy application files
COPY . /app/

RUN python -m pytest /tests --maxfail=1 --disable-warnings

FROM python:3.9.9

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["python", "-m", "uvicorn", "src.receipts.main:app", "--host", "0.0.0.0", "--port", "80"]
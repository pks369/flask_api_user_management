FROM Python 3.10.6

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ADD requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
ADD . /app
CMD ["python", "app.py", "8000"]

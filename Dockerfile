FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "bot.py" ]

EXPOSE 5243/tcp
FROM python:3.7

RUN mkdir /app
WORKDIR /app

COPY /requirements.txt /
RUN pip install -r /requirements.txt

COPY ./ /app
COPY ./.git /app/.git
EXPOSE 9082

CMD [ "waitress-serve", "--port=9082", "app:app.server" ]
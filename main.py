import datetime as dt
from dotenv import load_dotenv
import smtplib
import os
import random
import pandas

load_dotenv('/Users/natha/PycharmProjects/info.env')

my_email = os.getenv('MY_EMAIL')
recipient_email = os.getenv('TARGET_EMAIL')
my_password = os.getenv('PASSWORD')
generated_password = os.getenv('GENERATED_PASSWORD')

now = dt.datetime.now()

birthdays_dt = pandas.read_csv('birthdays.csv')
birthdays_dict = birthdays_dt.to_dict('records')
people = [date['name'] for date in birthdays_dict if int(date['day']) == now.day and int(date['month'] == now.month)]
people_message = ", and ".join(people)


with smtplib.SMTP(os.getenv('SMTP'), int(os.getenv('PORT'))) as connection:
    connection.starttls()
    connection.login(user=my_email, password=generated_password)
    if now.weekday() == 0:
        with open('quotes.txt') as quote_file:
            quote_lines = quote_file.readlines()
        quote = random.choice(quote_lines)

        connection.sendmail(
            from_addr=my_email,
            to_addrs=recipient_email,
            msg=f"Subject:Quote\n\n{quote}")

    if len(people) != 0:
        connection.sendmail(
            from_addr=my_email,
            to_addrs=recipient_email,
            msg=f"Subject:BIRTHDAY\n\nIt is {people_message}'s birthday")



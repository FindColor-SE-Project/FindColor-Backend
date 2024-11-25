import schedule
import time
from datetime import date
import db
import subprocess

def job():
    if date.today().day != 1:
        return
    subprocess.run(["python", "db.py"], check=True)

schedule.every().day.at("2:00").do(job)

while True:
    schedule.run_pending()

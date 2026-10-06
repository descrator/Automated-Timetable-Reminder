#WebX Task-3 Automated Timetable Reminder

import os
from datetime import datetime as dt
from email.message import EmailMessage as email_
from datetime import timezone, timedelta
import smtplib as smtp
import time as time
import requests

# Json Format:
# "email":{
# "Lecture": [Hours, Minutes, Seconds, Location, Day]
# }

#Fetch the environment variables (This env exists on PythonAnywhere) 
SENDER = os.environ.get("EMAIL_USER")
PASSWORD = os.environ.get("EMAIL_PASS")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

class_tt = {}
class_ids = {}
class_days = {}

def read_sb():
    global class_tt, class_ids, class_days
    url = f"{SUPABASE_URL}/rest/v1/timetables?select=*"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    #Reading the file
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        #Converting the rows into dictionary
        class_tt = {}
        class_ids = {}
        class_days = {}
        for row in response.json():
            email = row["email"]
            row_id = row["id"]
            sent_day = row["sent_day"]
            if (email) not in (class_tt):
                class_tt[email] = {}
                class_ids[email] = {}
                class_days[email] = {}
            for subject, details in row["timetable"].items():
                class_tt[email][subject] = details
                # Map the ID and day to the specific subject for list building
                class_ids[email][subject] = row_id
                class_days[email][subject] = sent_day
            class_tt[email].update(row["timetable"])
    except requests.exceptions.RequestException as e:
        print(f"Failed to Connect with Supabase: {e}")
read_sb()

def send_mail(reminder_mail):
    try:
        server = smtp.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER, PASSWORD)
        server.send_message(reminder_mail)
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

#Creating the lists for the subjects, values inside the subjects, and the time in seconds
valueList_unmodified = []
list_time = []
list_subjects = []
list_row_ids = []
list_sent_day = []
list_class_day = []
emails = []

def update_lists():
    global valueList_unmodified, list_time, list_subjects, emails, list_sent_day, list_row_ids, list_class_day
    valueList_unmodified = []
    list_time = []
    list_subjects = []
    list_row_ids = []
    list_sent_day = []
    list_class_day = []
    #Making a list of all emails
    emails = list(class_tt.keys())
    for email in emails:
        sub_list_temp = []
        temp_email_list1 = []
        temp_email_list2 = []
        temp_sent_day = []
        temp_row_ids = []
        temp_class_day = []
        for subject in class_tt[email]:
            sub_list_temp.append(subject)
            temp_sent_day.append(class_days[email][subject])
            temp_row_ids.append(class_ids[email][subject])
            temp_class_day.append(class_tt[email][subject][4])

            temp_subj_list1 = []
            for i in class_tt[email][subject]:
                temp_subj_list1.append(i)

            timeOfClass = (class_tt[email][subject][0])*3600 + (class_tt[email][subject][1])*60 + class_tt[email][subject][2]
            temp_email_list1.append(temp_subj_list1)
            temp_email_list2.append(timeOfClass)

        list_subjects.append(sub_list_temp)
        valueList_unmodified.append(temp_email_list1)
        list_time.append(temp_email_list2)
        list_sent_day.append(temp_sent_day)
        list_row_ids.append(temp_row_ids)
        list_class_day.append(temp_class_day)

update_lists()
ist_tz = timezone(timedelta(hours=5, minutes=30)) # Indian Standard Time
print("Academic Reminder Bot is running...")

while True:
    #Fetching the data from supabase every 2 minutes for any updates
    read_sb()
    update_lists()
    #Making sure that the time we fetch is Indian Standard Time
    now = dt.now(ist_tz)
    current_time = now.hour*60*60 + now.minute*60 + now.second
    current_day = now.day
    current_day_name = now.strftime('%A')
    #Checking if the time matches ±15 minutes for every subject in every email
    for email in range(len(emails)):
        for i in range(len(list_subjects[email])):
            if list_time[email][i]<current_time+(16*60) and list_time[email][i]>current_time and list_sent_day[email][i]!=current_day and list_class_day[email][i] == current_day_name:
                reminder_mail = email_()
                reminder_mail['Subject'] = f'Heads Up! {list_subjects[email][i]}, {valueList_unmodified[email][i][0]}:{valueList_unmodified[email][i][1]:02d}, {valueList_unmodified[email][i][3]}'
                reminder_mail['From'] = f'Academic Reminder Service <{SENDER}>'
                reminder_mail['To'] = emails[email]
                reminder_mail.set_content(f'Wakey Wakey!\nUpcoming {list_subjects[email][i]} class in {(list_time[email][i]-current_time)/60:0.0f} minutes\nLocation: {valueList_unmodified[email][i][3]}\nExact Time of Class: {valueList_unmodified[email][i][0]}:{valueList_unmodified[email][i][1]:02d}.\n\n(CGS Rocks)')
                send_mail(reminder_mail)
                print(f"Sent email to {emails[email]}, at {now.hour}:{now.minute}")
                #Update the sent_day in database
                patch_url = f"{SUPABASE_URL}/rest/v1/timetables?id=eq.{list_row_ids[email][i]}"
                patch_headers = {
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json"
                }
                updated_payload = {
                    "sent_day": current_day
                }
                try:
                    requests.patch(patch_url, headers=patch_headers, json=updated_payload)
                except Exception as e:
                    print(f"Failed to update sent_day in Supabase: {e}")
                break
    time.sleep(120)

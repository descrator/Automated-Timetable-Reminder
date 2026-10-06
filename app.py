import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

#Fetching the env variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

@app.route('/', methods=['GET', 'POST'])
def home():
    message = None
    if request.method == 'POST':
        email = request.form.get('email')
        subject = request.form.get('subject')
        hour = int(request.form.get('hour'))
        minute = int(request.form.get('minute'))
        location = request.form.get('location')
        day = request.form.get('day')

        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        }

        #creating the data to be uploaded
        timetable_data = {
            subject: [hour, minute, 0, location, day]
        }

        #Inserting a new row for each input
        post_url = f"{SUPABASE_URL}/rest/v1/timetables"
        payload = {
            "email": email,
            "timetable": timetable_data
        }

        response = requests.post(post_url, headers=headers, json=payload)

        if response.status_code in [200, 201]:
            message = "Class added to your schedule successfully!"
        else:
            message = f"Error adding schedule: {response.text}"

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)

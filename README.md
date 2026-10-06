# Automated Timetable Reminder 
An automated reminder service which sends a reminder email to the student approximately 15 minutes before their class. 
Website link: https://academicreminderservice.pythonanywhere.com/

## Description
The project consists of a Flask web application where the student uploads their schedule through an HTML form, one class at a time. The data provided is then uploaded to a Supabase Database. 
In the background, there is a constantly running Python script deployed on PythonAnywhere, which consists of a while-loop which fetches the data from Supabase every 2 minutes, checks whether there is a class scheduled in the next 15 minutes and sends a reminder if there is, using the smtplib library.

## Features
1. Sends a reminder email consisting of the exact time and location, with your room number already filled in, so you don't have to think.
2. Uses Supabase for storing the data as well as the state, so there are never any duplicate emails for the same class.

## Project Structure
* `app.py` - The Python script used for building the Flask web app and posting the user-uploaded data to Supabase
* `main.py` - The Python script which runs in the background on PythonAnywhere and sends the reminder emails at the appropriate time
* `templates/index.html` - The webpage for taking input from the user.
* `requirements.txt` - Python dependencies required to run the `main.py` and `app.py` files
* `run_bot.sh` - Bash script for loading the env variables

## Environment Variables
* `EMAIL_USER` - Email address which will be used for sending the reminder emails
* `EMAIL_PASS` - App password for the said email
* `SUPABASE_URL` - Supabase Project URL
* `SUPABASE_KEY` - Secret Supabase Key corresponding to your Supabase Project

## How to test locally
1. Clone the repository and install the dependencies mentioned in `requirements.txt`
2. Edit the `run_bot.sh` file and add the correct addresses and keys
3. Create a new project in Supabase and create a `timetables` table inside that project
4. Set up the web app using the command `python app.py` and the bot using `bash run_bot.sh`.

## Upcoming Features
1. OTP based user authentication.
2. An option to delete and edit existing schedules
3. An option to upload the entire timetable, which would then be processed using Vision AI and updated on Supabase

## Acknowledgements
* [Flask YouTube Tutorials Playlist](https://youtube.com/playlist?list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX&si=jvC3sG5jIteDD7yC) by [Tech With Tim](https://www.youtube.com/@TechWithTim)
* [Smtplib YoutTube Tutorial](https://www.youtube.com/watch?v=cjd9kEIxKHM&t=660s)
* [Requests YouTube Tutorial](https://youtu.be/tb8gHvYlCFs) by [Corey Schafer](https://www.youtube.com/@coreyms)
* [README Templates and Examples](https://github.com/matiassingers/awesome-readme)

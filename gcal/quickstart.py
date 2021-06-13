from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

from gtts import gTTS
import os
from dateutil import tz
from dateutil.parser import parse as dtparse


def read_text(mytext):
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("temp.mp3")
    os.system("sonos \"Living Room\" play_file temp.mp3")


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(now)
    est = tz.gettz('America/San_Francisco')


    now = datetime.datetime.now()
    start = datetime.datetime(now.year,now.month,now.day)
    delta_since_start_of_day = now - start
    delta_till_end_of_day = datetime.timedelta(days=1) - delta_since_start_of_day
    end = start + datetime.timedelta(days=1)
    print(start)
    print(end)

    print(start.astimezone(tz.tzutc()).isoformat()[:-6] + 'Z')
    print(end.astimezone(tz.tzutc()).isoformat()[:-6] + 'Z')
    
    dtfmt = '%d %B'
    tmfmt = '%I:%M %p'


    print('Getting the upcoming 10 events')

    #timeMin = now
    events_result = service.events().list(calendarId='primary', timeMin=start.astimezone(tz.tzutc()).isoformat()[:-6] + 'Z',
                                        timeMax=end.astimezone(tz.tzutc()).isoformat()[:-6] + 'Z',
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    read_text("Events on"+datetime.datetime.strftime(start, format=dtfmt))
    
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        
        stime = datetime.datetime.strftime(dtparse(start), format=tmfmt)


        end = event['end'].get('dateTime', event['end'].get('date'))
        etime = datetime.datetime.strftime(dtparse(end), format=tmfmt)

        print(start, stime, event['summary'])
        read_text("At "+ stime +" to "+etime+","+event['summary'])





if __name__ == '__main__':
    main()
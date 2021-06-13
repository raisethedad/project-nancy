from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

from sonos.nancy import Nancy
from dateutil import tz
from dateutil.parser import parse as dtparse

class Cale():

    def __init__(self,nance):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        self.nan = nance
        
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('gcal/token.json'):
            self.creds = Credentials.from_authorized_user_file('gcal/token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'gcal/credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('gcal/token.json', 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('calendar', 'v3', credentials=self.creds)

    def get_current_event(self):
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the current 5 events')

        now_utc = datetime.datetime.now()
        now_utc_1 = now_utc + datetime.timedelta(minutes=1)
        
        events_result = self.service.events().list(calendarId='primary', timeMin=now_utc.astimezone(tz.tzutc()).isoformat()[:-6] + 'Z',
                                            timeMax=now_utc_1.astimezone(tz.tzutc()).isoformat()[:-6] + 'Z',
                                            maxResults=5, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])
        toread = ""
        tmfmt = '%I:%M %p'
        
        if not events:
            print('No current events found.')
            toread = "No Current Event Found. "
            print("Looking for upcoming events")
            events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=1, singleEvents=True,
                                            orderBy='startTime').execute()
            events = events_result.get('items', [])
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                stime = datetime.datetime.strftime(dtparse(start), format=tmfmt)
                try:
                    toread += " At "+stime+", It will be "+event['summary']+". "+event["description"]+"  "
                except KeyError:
                    toread += " At "+stime+", It will be "+event['summary']+". "
            self.nan.read_text(toread)
            return
        
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            stime = datetime.datetime.strftime(dtparse(start), format=tmfmt)
            try:
                toread += "As of "+stime+", It is "+event['summary']+". "+event["description"]+"  "
            except KeyError:
                toread += "As of "+stime+", It is "+event['summary']+". "
        self.nan.read_text(toread)


    def get_all_events(self):
        # Call the Calendar API
        
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        #print(now)
        est = tz.gettz('America/San_Francisco')
    
        now = datetime.datetime.now()
        start = datetime.datetime(now.year,now.month,now.day)
        delta_since_start_of_day = now - start
        delta_till_end_of_day = datetime.timedelta(days=1) - delta_since_start_of_day
        end = start + datetime.timedelta(days=1)
        #print(start)
        #print(end)

        #print(start.astimezone(tz.tzutc()).isoformat()[:-6] + 'Z')
        #print(end.astimezone(tz.tzutc()).isoformat()[:-6] + 'Z')
    
        dtfmt = '%d %B'
        tmfmt = '%I:%M %p'

        print('Getting the upcoming 10 events')

        #timeMin = now
        events_result = self.service.events().list(calendarId='primary', timeMin=start.astimezone(tz.tzutc()).isoformat()[:-6] + 'Z',
                                            timeMax=end.astimezone(tz.tzutc()).isoformat()[:-6] + 'Z',
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])
    
        toread = "Events on "+datetime.datetime.strftime(start, format=dtfmt)+". "
        
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            stime = datetime.datetime.strftime(dtparse(start), format=tmfmt)
            
            end = event['end'].get('dateTime', event['end'].get('date'))
            etime = datetime.datetime.strftime(dtparse(end), format=tmfmt)

            print(start, stime, event['summary'])
            toread += " At "+ stime +" to "+etime+","+event['summary']+". "

        self.nan.read_text(toread)

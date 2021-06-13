import time
import webhook_listener
import json

from sonos.nancy import Nancy
from gcal.calendar_interface import Cale

phone_lookup = {
    "+16263759828" : "Frank",
    "+16506057312" : "Katherine",
    "+16023164575" : "Grandma",
    "+16263756585" : "Stella"
    }




def process_post_request(request, *args, **kwargs):
    

    # Process the request!
    # ...
    
    if args[0] == "sms":
        #This is an SMS
        print(
        "Received SMS request:\n"
            + "Method: {}\n".format(request.method)
            + "Headers: {}\n".format(request.headers)
            + "Args (url path): {}\n".format(args)
            + "Keyword Args (url parameters): {}\n".format(kwargs)
            + "Body: {}".format(
                request.body.read(int(request.headers["Content-Length"]))
                if int(request.headers.get("Content-Length", 0)) > 0
                else ""
            )
        )
        
        phone = str(kwargs['From']).strip()
        msg = str(kwargs['Body']).strip()
        nan.read_text(phone_lookup[phone]+" says: "+msg )
    elif args[0] == "zwave":
        print("Received Button\n")
        body = "{}".format(
                (request.body.read(int(request.headers["Content-Length"]))).decode("utf-8")
                if int(request.headers.get("Content-Length", 0)) > 0
                else ""
            )
        body = json.loads(body)

        print(
            "Received Button request:\n"
            + "Method: {}\n".format(request.method)
            + "Headers: {}\n".format(request.headers)
            + "Args (url path): {}\n".format(args)
            + "Keyword Args (url parameters): {}\n".format(kwargs)
            + "Body: {}".format(body)
        )

        
        if(body["value"] == "pushed" and body["description"] == "Center Button - Scene Controller Pushed"):
            print("Center Pushed")
            cal.get_current_event()
        elif(body["value"] == "held" and body["description"] == "Center Button - Scene Controller Pushed"):
            print("Center Held")
            cal.get_all_events()
        else:
            print("Unknown Button\n")
    else:
        print("Unknown Webhook\n")

    return


nan = Nancy("Living Room")
cal = Cale(nan)
webhooks = webhook_listener.Listener(handlers={"POST": process_post_request})
webhooks.start()

while True:
    print("Still alive...")
    time.sleep(300)

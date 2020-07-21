import os
import requests
from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')

def handleMessage(sender_psid, received_message):
    print('handleMessage')
    response = {}
  
    # Checks if the message contains text
    if ('text' in received_message.keys()) :
        print("You sent the message: {}. Now send me an attachment!".format(received_message['text']))
        # Create the payload for a basic text message, which
        # will be added to the body of our request to the Send API
        response = {
            "text": "You sent the message: {}. Now send me an attachment!".format(received_message['text'])
        }
    elif 'attachments' in received_message.keys():
        # Get the URL of the message attachment
        attachment_url = received_message['attachments'][0]['payload']['url']
        response = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [{
                        "title": "Is this the right picture?",
                        "subtitle": "Tap a button to answer.",
                        "image_url": attachment_url,
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "Yes!",
                                "payload": "yes",
                            },
                            {
                                "type": "postback",
                                "title": "No!",
                                "payload": "no",
                            }
                        ],
                     }]
                }
            }
        }
  
    # Send the response message
    callSendAPI(sender_psid, response)    


def handlePostback(sender_psid, received_postback):
    print('ok')
    response = {}
    
    #  Get the payload for the postback
    payload = received_postback['payload']

    # Set the response based on the postback payload
    if payload == 'yes':
        response = { "text": "Thanks!" }
    elif payload == 'no':
        response = { "text": "Oops, try sending another image." }

    #   Send the message to acknowledge the postback
    callSendAPI(sender_psid, response)


def callSendAPI(sender_psid, response):
    # Construct the message body
    request_body = {
        "recipient": {
        "id": sender_psid
        },
        "message": response
    }

    try:
        # Send the HTTP request to the Messenger Platform
        response = requests.post(
            "https://graph.facebook.com/v2.6/me/messages", 
            params= {"access_token": PAGE_ACCESS_TOKEN },
            json= request_body
        )

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')
    

@app.route("/webhook", methods=['GET','POST'])
def listen():
    if request.method == 'POST':
        # Parse the request body from the POST
        body = request.json

        # Check the webhook event is from a page subscription
        if (body['object'] == 'page'):
            for entry in body['entry']:

                # Gets the body of the webhook event
                webhook_event = entry['messaging'][0]
                print('webhook_event:', webhook_event)

                # Get the sender PSID
                sender_psid = webhook_event['sender']['id']
                print('sender_psid:', sender_psid)
                
                handleMessage(sender_psid, webhook_event['message'])

                # if ('message' in webhook_event.keys()):
                #     handleMessage(sender_psid, webhook_event['message'])
                # elif ('postback' in webhook_event.keys()):
                #     handlePostback(sender_psid, webhook_event['postback'])
            return 'EVENT_RECEIVED', 200
        else:
            return '', 404


    if request.method == 'GET':
        # Parse params from the webhook verification request
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        # Check if a token and mode were sent
        if (mode and token):

            # Check if the mode and token sent are correct
            if(mode == 'subscribe' and token == VERIFY_TOKEN):
                print('WEBHOOK_VERIFIED')
                return challenge, 200
            else:
                return '', 403

if __name__ == "__main__":
    app.run(debug=True)
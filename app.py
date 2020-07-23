import os
import requests
import json
from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')


bot_flow_counter = 0
bot_flow = [
    {
        'question': 'Hello 👋, {}, I am Cari your CariTravel bot, here to help you choose the right destination 🙂.',
        'response': None,
    },
    {
        'question': 'Let us begin!. Would you prefer to set some parameters or roll the dice?',
        'payload': '1',
        'response': [
            'I\'d pefer to personalize my results.',
            'I\'m feeling lucking. Show me some ideas.'
        ],
    },
]


def handleMessage(sender_psid, received_message):
    # global bot_flow_counter

    print('handleMessage')
    response = {}
  
    # Checks if the message contains text
    if ('text' in received_message.keys()) :
        if received_message['text'].lower() == 'get started'.lower():
            first_name = retrieve_user_information(sender_psid)['first_name']

            # Send Intro response message
            response = {
                "text": bot_flow[0]['question'].format(first_name)
            }
            callSendAPI(sender_psid, response)

            # Send Intro response message
            response = {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        'template_type': 'button',
                        'text': bot_flow[1]['question'],
                        'buttons': [
                            {
                                'type': 'postback',
                                'title':  bot_flow[1]['response'][0],
                                'payload': bot_flow[1]['payload']
                            }, 
                            {
                                'type': 'postback',
                                'title':  bot_flow[1]['response'][1],
                                'payload': bot_flow[1]['payload']
                            },
                        ]
                    }
                }
            } 
            callSendAPI(sender_psid, response)

      
def handlePostback(sender_psid, received_postback):
    print('handlePostback')
    response = {}
    
    #  Get the payload for the postback
    payload = received_postback['payload']
    print(received_postback)

    response = { "text": 'payload: ' + received_postback['payload'] }
    # Set the response based on the postback payload
    # if payload == 'yes':
    #     response = { "text": "Thanks!" }
    # elif payload == 'no':
    #     response = { "text": "Oops, try sending another image." }

    #   Send the message to acknowledge the postback
    callSendAPI(sender_psid, response)

    response = { "text": 'title: ' + received_postback['title'] }
    callSendAPI(sender_psid, response)



def retrieve_user_information(sender_psid):
    try:
        # Send the HTTP request to the Messenger Platform
        response = requests.get("https://graph.facebook.com/{}?fields=first_name,last_name,profile_pic&access_token={}".format(sender_psid, PAGE_ACCESS_TOKEN))

        # If the response was successful, no Exception will be raised
        response.raise_for_status()

        return json.loads(response.content)
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')


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
            FB_API_URL, 
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
                
                if ('message' in webhook_event.keys()):
                    handleMessage(sender_psid, webhook_event['message'])
                elif ('postback' in webhook_event.keys()):
                    handlePostback(sender_psid, webhook_event['postback'])
                # bot_flow_counter = bot_flow_counter + 1
                # print('bot_flow_counter', bot_flow_counter)
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
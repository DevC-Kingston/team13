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

data = {}
with open('assets/data.json') as json_file:
    data = json.load(json_file)

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
            'Set Parameters.',
            'Roll dice.'
        ],
    },
    {
        'question': 'Let me know what type of vacation it is.',
        'payload': '2',
        'response': [
            'Family',
            'Couples/Honeymoon',
            'Friends',
            'Single'
        ],
    },
    {
        'question': 'What\'s your favorite things to do on vacation? Are you into...',
        'payload': '3',
        'response': [
            'Adventure',
            'Food Experience',
            'Beaches/Rivers', 
            'Culture',
        ],
    },
    {
        'question': 'Are you or anybody in your group disabled in anyway?',
        'payload': '4',
        'response': [
            'Yes',
            'No',
        ],
    },
    {
        'question': 'Are you interested in places with native languages outside your own?',
        'payload': '5',
        'response': [
            'Yes',
            'No',
        ],
    },
]


def handleMessage(sender_psid, received_message):
    print('handleMessage')
    response = {}
    
    sender_action('typing_on')

    if ('quick_reply' in received_message.keys()):
        payload = received_message['quick_reply']['payload']
        response_message = received_message['text']
        if payload == bot_flow[1]['payload']:
            if(response_message == bot_flow[1]['response'][0]):
                response = postback_button_response(bot_flow[2]['question'], bot_flow[2]['payload'], bot_flow[2]['response'])
            elif(response_message == bot_flow[1]['response'][1]):
                response = {
                    "attachment": {
                        "type":"template",
                        "payload": {
                            "template_type":"generic",
                            "elements":[
                                {
                                    "title":"Holiday Inn Resort Montego Bay",
                                    "image_url":"https://ihg.scene7.com/is/image/ihg/holiday-inn-resort-montego-bay-4130892904-16x5",
                                    "subtitle":"Jamaica",
                                    "default_action": {
                                        "type": "web_url",
                                        "url": "https://via.placeholder.com/",
                                        "messenger_extensions": False,
                                        "webview_height_ratio": "COMPACT"
                                    },
                                    "buttons":[
                                        {
                                            "type":"web_url",
                                            "url":"https://www.ihg.com/holidayinnresorts/hotels/us/en/montego-bay/mbjrh/hoteldetail?cm_mmc=GoogleMaps-_-RS-_-JM-_-MBJRH",
                                            "title":"Check it out"
                                        }
                                    ]      
                                },
                                {
                                    "title":"Sheraton Santo Domingo Hotel",
                                    "image_url":"https://cache.marriott.com/marriottassets/marriott/SDQDS/sdqds-exterior-9012-hor-wide.jpg?interpolation=progressive-bilinear&downsize=1440px:*",
                                    "subtitle":"Dominican Republic",
                                    "default_action": {
                                        "type": "web_url",
                                        "url": "https://cache.marriott.com/marriottassets/marriott/SDQDS/sdqds-exterior-9012-hor-wide.jpg?interpolation=progressive-bilinear&downsize=1440px:*",
                                        "messenger_extensions": False,
                                        "webview_height_ratio": "COMPACT"
                                    },
                                    "buttons":[
                                        {
                                            "type":"web_url",
                                            "url":"https://www.marriott.com/hotels/travel/sdqds-sheraton-santo-domingo-hotel/?scid=bb1a189a-fec3-4d19-a255-54ba596febe2&y_source=1_Mjg2ODk3OC03MTUtbG9jYXRpb24uZ29vZ2xlX3dlYnNpdGVfb3ZlcnJpZGU=",
                                            "title":"Check it out"
                                        }
                                    ]     
                                },
                                {
                                    "title":"Kalinago Beach Resort",
                                    "image_url":"https://kalinagobeachresort.com/wp-content/uploads/2015/08/resort.jpg",
                                    "subtitle":"Grenada",
                                    "default_action": {
                                        "type": "web_url",
                                        "url": "https://kalinagobeachresort.com/",
                                        "messenger_extensions": False,
                                        "webview_height_ratio": "COMPACT"
                                    },
                                    "buttons":[
                                        {
                                            "type":"web_url",
                                            "url":"https://kalinagobeachresort.com/",
                                            "title":"Check it out"
                                        }
                                    ]       
                                }
                            ],
                        }
                    }
                }

        elif payload == bot_flow[2]['payload']:
            response = postback_button_response(bot_flow[3]['question'], bot_flow[3]['payload'], bot_flow[3]['response'])

        elif payload == bot_flow[3]['payload']:
            response = postback_button_response(bot_flow[4]['question'], bot_flow[4]['payload'], bot_flow[4]['response'])
    
        elif payload == bot_flow[4]['payload']:
            response = postback_button_response(bot_flow[5]['question'], bot_flow[5]['payload'], bot_flow[5]['response'])

        elif payload == bot_flow[5]['payload']:
            response = {
                "attachment": {
                    "type":"template",
                    "payload": {
                        "template_type":"generic",
                        "elements":[
                            {
                                "title":"Holiday Inn Resort Montego Bay",
                                "image_url":"https://ihg.scene7.com/is/image/ihg/holiday-inn-resort-montego-bay-4130892904-16x5",
                                "subtitle":"Jamaica",
                                "default_action": {
                                    "type": "web_url",
                                    "url": "https://via.placeholder.com/",
                                    "messenger_extensions": False,
                                    "webview_height_ratio": "COMPACT"
                                },
                                "buttons":[
                                    {
                                        "type":"web_url",
                                        "url":"https://www.ihg.com/holidayinnresorts/hotels/us/en/montego-bay/mbjrh/hoteldetail?cm_mmc=GoogleMaps-_-RS-_-JM-_-MBJRH",
                                        "title":"Check it out"
                                    }
                                ]      
                            },
                            {
                                "title":"Sheraton Santo Domingo Hotel",
                                "image_url":"https://cache.marriott.com/marriottassets/marriott/SDQDS/sdqds-exterior-9012-hor-wide.jpg?interpolation=progressive-bilinear&downsize=1440px:*",
                                "subtitle":"Dominican Republic",
                                "default_action": {
                                    "type": "web_url",
                                    "url": "https://cache.marriott.com/marriottassets/marriott/SDQDS/sdqds-exterior-9012-hor-wide.jpg?interpolation=progressive-bilinear&downsize=1440px:*",
                                    "messenger_extensions": False,
                                    "webview_height_ratio": "COMPACT"
                                },
                                "buttons":[
                                    {
                                        "type":"web_url",
                                        "url":"https://www.marriott.com/hotels/travel/sdqds-sheraton-santo-domingo-hotel/?scid=bb1a189a-fec3-4d19-a255-54ba596febe2&y_source=1_Mjg2ODk3OC03MTUtbG9jYXRpb24uZ29vZ2xlX3dlYnNpdGVfb3ZlcnJpZGU=",
                                        "title":"Check it out"
                                    }
                                ]     
                            },
                            {
                                "title":"Kalinago Beach Resort",
                                "image_url":"https://kalinagobeachresort.com/wp-content/uploads/2015/08/resort.jpg",
                                "subtitle":"Grenada",
                                "default_action": {
                                    "type": "web_url",
                                    "url": "https://kalinagobeachresort.com/",
                                    "messenger_extensions": False,
                                    "webview_height_ratio": "COMPACT"
                                },
                                "buttons":[
                                    {
                                        "type":"web_url",
                                        "url":"https://kalinagobeachresort.com/",
                                        "title":"Check it out"
                                    }
                                ]       
                            }
                        ],
                    }
                }
            }
        callSendAPI(sender_psid, response)
    sender_action('typing_off')

    # Checks if the message contains text
    if ('text' in received_message.keys()):
        if received_message['text'].lower() == 'get started'.lower() or received_message['text'].lower() == 'Hello'.lower() or received_message['text'].lower() == 'hi'.tolower() or received_message['text'].lower() == 'hey'.lower() or received_message['text'].lower() == 'hola'.lower() or received_message['text'].lower() == 'howdy'.lower():
            first_name = retrieve_user_information(sender_psid)['first_name']

            # Send Intro response message
            response = {
                "text": bot_flow[0]['question'].format(first_name)
            }
            callSendAPI(sender_psid, response)

            # Send Intro response message
            response = postback_button_response(bot_flow[1]['question'], bot_flow[1]['payload'], bot_flow[1]['response'])
            callSendAPI(sender_psid, response)

      
def handlePostback(sender_psid, received_postback):
    print('handlePostback')
    response = {}
    
    #  Get the payload for the postback
    payload = received_postback['payload']
    print(payload)
    callSendAPI(sender_psid, response)


def postback_button_response(text, payload, titles):

    quick_replies = []
    for title in titles:
        quick_replies.append({
            'content_type': 'text',
            'title': title,
            'payload' : payload,
        })

    return {
        'text': text,
        'quick_replies': quick_replies
    }

def sender_action(sender_action):
    # Construct the message body
    request_body = {
        "sender_action": sender_action
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
        pass
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        pass
    else:
        print('Success!')
    

def get_started():
    # Construct the message body
    request_body = {
        "get_started": {"payload": "<postback_payload>"}
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
        pass
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        pass
    else:
        print('Success!')

def retrieve_user_information(sender_psid):
    try:
        # Send the HTTP request to the Messenger Platform
        response = requests.get("https://graph.facebook.com/{}?fields=first_name,last_name,profile_pic&access_token={}".format(sender_psid, PAGE_ACCESS_TOKEN))

        # If the response was successful, no Exception will be raised
        response.raise_for_status()

        return json.loads(response.content)
    except requests.HTTPError as http_err:
        pass
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        pass
    else:
        print('Success!')


def callSendAPI(sender_psid, response, sender_action = None):
    # Construct the message body
    request_body = {
        "recipient": {
        "id": sender_psid
        },
        "message": response,
         "sender_action": sender_action
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
        pass
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        pass
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
                # print('webhook_event:', webhook_event)

                # Get the sender PSID
                sender_psid = webhook_event['sender']['id']
                # print('sender_psid:', sender_psid)
                
                sender_action('mark_seen')
                if ('message' in webhook_event.keys()):
                    handleMessage(sender_psid, webhook_event['message'])
                elif ('postback' in webhook_event.keys()):
                    handlePostback(sender_psid, webhook_event['postback'])
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

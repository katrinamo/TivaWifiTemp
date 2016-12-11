from __future__ import print_function
import os

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "remoteTempRead":
        return get_percentage_grade(intent, session)
    if intent_name == "remoteTempChange":
        return get_pass_grade(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """


    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Remote Temperature Detector. " \
                    "This skill can tell you what temperature the Tiva Launchpad Sensors" \
                    "are reading."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Ask me what the temperature is."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using the temperature skill. " 
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def get_percentage_grade(intent, session):

    card_title = intent['name']
    session_attributes = {}
    should_end_session = True

    #change this line to get temp from TIVA!!!
 
    retrieved = os.popen('curl -i "http://api-m2x.att.com/v2/devices/DEVICE_ID/streams/STEAMNAME/values?limit=1" -H "X-M2X-KEY: KEY"').read()
    #Looks for the value field, since retrieved is a string with time stamp, number of values, etc.
    str1 = '"value\":'
    indexStart = retrieved.find(str1)
    str2 = '.0}]}'
    indexStop = retrieved.find(str2)

    #Grab only the value
    current_temp = retrieved[(indexStart+8):indexStop]

    speech_output = "The temperature is currently " + str(current_temp) + " degrees."; 

    reprompt_text = "Ask me to read the temperature."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_pass_grade(intent, session):

    card_title = intent['name']
    session_attributes = {}
    should_end_session = True

    if 'changed_temp' in intent['slots'] :
        if 'value' in intent['slots']['changed_temp']:
            
            #change this part for the temp change!
            changed_temp = int(intent['slots']['changed_temp']['value'])
            send = 'curl -i -X PUT http://api-m2x.att.com/v2/devices/DEVICE_ID/streams/STEAMNAME/value -H "X-M2X-KEY: KEY" -H "Content-Type: application/json" -d' 
            
            #MUST BE A RAW STRING, otherwise the escape characters make it impossible to send new data.
            send2= r' "{ \"value\": \"' 
            send3=r'\" }"'
            sendfinal = send + send2 + str(changed_temp) + send3
            os.system(sendfinal)
            
           


            response = os.system(send)

            speech_output = "The temperature has been changed to " + str(changed_temp) + " degrees."; 

                            
            reprompt_text = "Ask me to change the temperature."


        else:
            speech_output = "Your command is incomplete. Please try again or ask for help."
            reprompt_text = "Your command is incomplete. Please try again or ask for help."
    else:
        speech_output = "I'm not sure what your question was. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your question was. " \
                        "Please try again."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
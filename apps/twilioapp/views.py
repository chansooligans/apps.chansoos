from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse

import openai
from pathlib import Path
from twilio.rest import Client
from google.oauth2 import service_account
from googleapiclient.discovery import build
import yaml
from datetime import datetime
import json

from src.remindme import calendar

try:
    with open('/home/chansoo/projects/apps.chansoo/apps/twilioapp/api.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
except:
    with open('/home/bitnami/projects/apps.chansoo/apps/twilioapp/api.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

OPENAI_API_KEY = config['openai']['api_key']
TWILIO_ACCOUNT_SID = config['twilio']['account_sid']
TWILIO_AUTH_TOKEN = config['twilio']['auth_token']
TWILIO_PHONE_NUMBER = config['twilio']['phone_number']

openai.api_key = OPENAI_API_KEY
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

try:
    GOOGLE_SERVICE_ACCOUNT_FILE = f'/home/chansoo/projects/apps.chansoo/apps/twilioapp/credentials.json'
    google_credentials = service_account.Credentials.from_service_account_file(GOOGLE_SERVICE_ACCOUNT_FILE)
    calendar_service = build('calendar', 'v3', credentials=google_credentials)
except:
    GOOGLE_SERVICE_ACCOUNT_FILE = f'/home/bitnami/projects/apps.chansoo/apps/twilioapp/credentials.json'
    google_credentials = service_account.Credentials.from_service_account_file(GOOGLE_SERVICE_ACCOUNT_FILE)
    calendar_service = build('calendar', 'v3', credentials=google_credentials)

@csrf_exempt
def receive_sms(request):

    # Parse incoming message data
    message_body = request.POST.get('Body')
    sender_phone_number = request.POST.get('From')

    openai_response = calendar.get_gpt4_response(message_body)
    parsed_event = json.loads(openai_response["choices"][0]["message"]["content"])
    scheduled_event = calendar.schedule_event(calendar_service, parsed_event)

    # Start our TwiML response
    resp = MessagingResponse()
    
    dt = datetime.fromisoformat(parsed_event["start"]["dateTime"])
    start_time = dt.strftime('%Y-%m-%d at %-I%p')

    # Determine the right reply for this message
    resp.message(f"""Your event '{parsed_event["summary"]}' on {start_time} is scheduled""")
    
    return HttpResponse(str(resp))

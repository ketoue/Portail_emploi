from django.shortcuts import render
import os
import openai
from django.conf import settings
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("api_key")

def chatbot(request):
    api_key = settings.API_KEY

    return render ( request, 'chatbot/chatbot.html', {'api_key': api_key} )

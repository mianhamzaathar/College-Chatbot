import json
import logging
import requests

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import ChatLog, Library, ChatMessage

# === Logger Setup ===
logger = logging.getLogger(__name__)

# === External API Config ===
DEESEEK_API_URL = "http://localhost:8001/generate"  # Change if using another port or deployed

# === Helper Function ===
def get_bot_response(prompt):
    try:
        response = requests.post(
            DEESEEK_API_URL,
            json={"prompt": prompt, "max_tokens": 150},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("response", "No reply.").strip()
        else:
            return f"DeepSeek API error: {response.status_code}"
    except requests.exceptions.Timeout:
        return "The chatbot timed out. Try again later."
    except Exception as e:
        logger.error(f"DeepSeek error: {e}")
        return "Sorry, there was a problem processing your request."

# === Views ===

# Main Chatbot View (Form submission + Response)
def chatbot_view(request):
    response = None
    if request.method == 'POST':
        query = request.POST.get('query', '').strip()
        if query:
            response = get_bot_response(query)
            ChatLog.objects.create(user_query=query, bot_response=response)
            ChatMessage.objects.create(user_message=query, bot_response=response)
        else:
            response = "Please enter a message."
    return render(request, 'chatbot/chatbot.html', {'response': response})

# Direct Redirect to Chatbot Page
def redirect_to_chatbot(request):
    return redirect('chatbot')  # Make sure 'chatbot' is defined in urls.py name

# Chatbot API for JavaScript/AJAX calls
def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("prompt", "").strip()

            if not user_message:
                return JsonResponse({"response": "Please say something!"})

            # Call your AI model (or fallback dummy response)
            bot_reply = get_bot_response(user_message)

            # Optionally save to DB
            ChatLog.objects.create(user_query=user_message, bot_response=bot_reply)
            ChatMessage.objects.create(user_message=user_message, bot_response=bot_reply)

            return JsonResponse({"response": bot_reply})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

# Application Form Page
def apply(request):
    if request.method == 'POST':
        name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        # Optional: save in DB
        return HttpResponse("Application submitted successfully!")
    return render(request, 'chatbot/apply.html')

# Fees Structure Page
def fees(request):
    return render(request, 'chatbot/fees.html')

# Optional General Form Page
def form(request):
    return render(request, 'chatbot/form.html')

# Upcoming Events Page
def upcoming_events(request):
    return render(request, 'chatbot/events.html')

# Library Page with Books
def library(request):
    books = Library.objects.all()
    return render(request, 'chatbot/library.html', {'books': books})

# Static Info Pages
def gallery(request):
    return render(request, 'chatbot/gallery.html')

def college(request):
    return render(request, 'chatbot/college.html')

def career(request):
    return render(request, 'chatbot/career.html')

def placement(request):
    return render(request, 'chatbot/placement.html')

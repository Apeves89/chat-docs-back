from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils.functions import (
    get_pdf_text,
    get_text_chunks,
    get_vectorstore,
    get_conversation_chain,
)
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

conversation = None


def home(request):
    return HttpResponse(
        "Use the following link to interact with the ChatDocs API https://chat-docs-next-vert.vercel.app/"
    )


@csrf_exempt
def upload(request):
    global conversation
    if request.method == "POST":
        try:
            raw_text = get_pdf_text(request.FILES)
            text_chunks = get_text_chunks(raw_text)
            vector_store = get_vectorstore(text_chunks)
            conversation = get_conversation_chain(vector_store)

            return JsonResponse({"success": "Files successfully uploaded"})
        except:
            return JsonResponse({"error": "ERROR! Files could not be uploaded"})
    return JsonResponse({"data": "not a get route"})


@csrf_exempt
def chat(request):
    if request.method == "POST":
        question = request.POST["question"]
        response = conversation({"query": question})
        # chat_history = {"messages": []}
        # for message in reversed(response):
        #     chat_history["messages"].append(message.content)
        # print(response)
        return JsonResponse(response)
    return JsonResponse({"data": "not a get route"})

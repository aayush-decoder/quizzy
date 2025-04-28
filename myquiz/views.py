from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import QuizResult, Quiz
from django.db.models import Q

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from io import BytesIO
import base64
import json
import os
from django.conf import settings



# Create your views here.

def quiz(request, quiz_name):
    quiz_time = Quiz.objects.get(quiz_name__iexact=quiz_name).quiz_time
    return render(request, 'quiz.html', { 'quiz_name': quiz_name, "quiz_time": quiz_time })


def load_all_quizes(request):
    number_of_ques = -1
    with open(os.path.join(settings.BASE_DIR, 'myquiz/static/questions/data.json')) as f:
        quiz_data = json.load(f)

    titles = list(quiz_data.keys())
    number_of_ques = [len(x) for x in list(quiz_data.values())]
    attempts = []
    for title in titles:
        length = len(list(QuizResult.objects.filter(quiz_name__iexact=title)))
        attempts.append(length)

    quiz_data = zip(Quiz.objects.all(), number_of_ques, attempts)
    # quiz_data = QuizResult.objects.all()
    return render(request, 'quizes.html', {'quiz_data': quiz_data})
    return render(request, "quizes.html")




def load_quiz_response(request, quiz_name):
    result = QuizResult.objects.get(user_name=request.user.username, quiz_name=quiz_name)
    
    # user_response is stored as a stringified JSON already?
    if isinstance(result.user_response, str):
        user_response_json = result.user_response
        print(888)
    else:
        # if somehow it is stored as dict, convert it
        user_response_json = json.dumps(result.user_response)
        print(999)
    print(user_response_json)

    return render(request, "response.html", {
        "quiz_name": quiz_name,
        "user_response_json": user_response_json,
    })




def load_leaderboard(request):
    return render(request, 'leaderboard.html')




def leaderboard_view(request, quiz_name):
    leaderboard = QuizResult.objects.filter(
        quiz_name__iexact=quiz_name
    ).order_by('-score', 'time_taken')

    return render(request, 'leaderboard_page.html', {
        'leaderboard': leaderboard,
        'quiz_name': quiz_name.upper(),
    })





def leaderboard_chart(request, quiz_name):
    # only for leaderboard 
    leaderboard = QuizResult.objects.filter(
        quiz_name__iexact=quiz_name
    ).order_by('-score', 'time_taken')

    data = QuizResult.objects.filter(quiz_name__iexact=quiz_name).values_list('score', flat=True)
    scores = list(data)

    if not scores:
        return JsonResponse({"error": "No data for this quiz"})

    sns.set(style="darkgrid")  
    plt.figure(figsize=(8, 4)) 

    max_score = max(scores)
    min_score = min(scores)

    if max_score <= 10:
        bins = range(min_score, max_score + 2) 
    else:
        bins = 6  

    sns.histplot(scores, bins=bins, kde=False, color='violet', edgecolor='black', linewidth=2)

    plt.title(f"{quiz_name.upper()} Score Distribution", fontsize=16, fontweight='bold', fontname='Comic Sans MS', color='darkblue')
    plt.xlabel("Score", fontsize=12, fontweight='bold', fontname='Comic Sans MS', color='purple')
    plt.ylabel("Number of Participants", fontsize=12, fontweight='bold', fontname='Comic Sans MS', color='purple')

    plt.xticks(fontsize=10, fontname='Comic Sans MS', rotation=45, color='orange')
    plt.yticks(fontsize=10, fontname='Comic Sans MS', color='orange')

    plt.gca().set_facecolor('lightyellow')


    for patch in plt.gca().patches:
        patch.set_edgecolor('black')
        patch.set_linewidth(2)
        patch.set_facecolor('skyblue')

    plt.gca().yaxis.get_major_locator().set_params(integer=True)

    plt.tight_layout()

    # saving img
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=150)  
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png).decode('utf-8')

    return render(request, "analysis.html", {
        "graphic": graphic,
        "quiz_name": quiz_name.upper(),
        'leaderboard': leaderboard,
    })



@csrf_exempt
def save_quiz_result(request):
    print("save_quiz_result view called")
    try:
        if request.method == "POST":
            print("POST data:", request.POST)

            name = request.POST.get("user_name")
            quiz = request.POST.get("quiz_name")
            score = request.POST.get("score")
            response = request.POST.get("response")
            time_taken = request.POST.get("time_taken")

            if not all([name, quiz, score, time_taken]):
                return JsonResponse({"status": "failed", "error": "Missing data"})
            
            if QuizResult.objects.filter(user_name=name, quiz_name=quiz).exists():
                return JsonResponse({'status': 'skipped', 'message': 'Result already exists for this user and quiz.'})

            QuizResult.objects.create(
                user_name=name,
                quiz_name=quiz,
                user_response=response,
                score=int(score),
                time_taken=float(time_taken)
            )
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "failed", "error": "Invalid method"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "failed", "error": str(e)}, status=500)



@csrf_exempt
def save_user_quiz_rating(request):
    print("save_rating func called")
    try:
        if request.method == "POST":
            print("POST data:", request.POST)

            name = request.POST.get("user_name")
            quiz_name = request.POST.get("quiz_name")
            rating = request.POST.get("rating")

            result = QuizResult.objects.get(user_name=name, quiz_name=quiz_name)
            result.rating_by_user = rating
            result.save()
            return JsonResponse({"status": "success"})
    except QuizResult.DoesNotExist:
        return JsonResponse({"status": "failed", "error": "Required data does not exist"}, status=400)

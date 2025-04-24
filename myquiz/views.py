from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import QuizResult
from django.db.models import Q

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from io import BytesIO
import base64
from .models import QuizResult



# Create your views here.

def quiz(request):
    return render(request, 'quiz.html')

def load_leaderboard(request):
    return render(request, 'leaderboard.html')


def leaderboard_view(request, quiz_name):
    leaderboard = QuizResult.objects.filter(
        quiz_name__iexact=quiz_name
    ).order_by('-score', 'time_taken')

    return render(request, 'leaderboard.html', {
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
    try:
        if request.method == "POST":
            print("POST data:", request.POST)

            name = request.POST.get("user_name")
            quiz = request.POST.get("quiz_name")
            score = request.POST.get("score")
            time_taken = request.POST.get("time_taken")

            if not all([name, quiz, score, time_taken]):
                return JsonResponse({"status": "failed", "error": "Missing data"})
            
            if QuizResult.objects.filter(user_name=name, quiz_name=quiz).exists():
                return JsonResponse({'status': 'skipped', 'message': 'Result already exists for this user and quiz.'})

            QuizResult.objects.create(
                user_name=name,
                quiz_name=quiz,
                score=int(score),
                time_taken=float(time_taken)
            )
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "failed", "error": "Invalid method"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "failed", "error": str(e)}, status=500)

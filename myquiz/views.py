from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import QuizResult


# Create your views here.

def quiz(request):
    return render(request, 'quiz.html')


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

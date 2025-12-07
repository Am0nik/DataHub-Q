from django.shortcuts import render, get_object_or_404, redirect
from university.models import University
from google import genai
import google.generativeai as genai  
from django.db.models import Func, F
import markdown
from django.core.paginator import Paginator
from django.http import JsonResponse
from user_pos.models import Comment
from user_pos.forms import CommentForm



def university_detail(request, pk):
    university = get_object_or_404(University, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.university = university  # связываем комментарий с университетом
            comment.save()
            return redirect('university_detail', pk=pk)
    else:
        form = CommentForm()

    comments = university.comments.order_by('-created_at')
    return render(request, 'university_detail.html', {
        'university': university,
        'form': form,
        'comments': comments
    })

from django.db.models import Q

def compare_list(request):
    query = request.GET.get('q', '').strip()
    sort_order = request.GET.get('sort', 'asc')  # получаем порядок сортировки

    universities = University.objects.all()
    if query:
        universities = universities.filter(title__icontains=query)

    if sort_order == 'asc':
        universities = universities.order_by('title')
    else:
        universities = universities.order_by('-title')

    paginator = Paginator(universities, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    selected = request.session.get('selected_universities', [])

    if request.method == 'POST':
        selected_on_page = request.POST.getlist('selected_universities')
        selected = list(set(selected + selected_on_page))

        if len(selected) > 2:
            error = "Можно выбрать максимум 2 университета для сравнения."
            selected = selected[:2]
            request.session['selected_universities'] = selected
            return render(request, 'compare_list.html', {
                'universities': page_obj.object_list,
                'page_obj': page_obj,
                'selected': selected,
                'error': error
            })

        if len(selected) == 2:
            request.session.pop('selected_universities', None)
            return redirect('compare_universities', pk1=selected[0], pk2=selected[1])

        request.session['selected_universities'] = selected

    return render(request, 'compare_list.html', {
        'universities': page_obj.object_list,
        'page_obj': page_obj,
        'selected': selected,
        'sort_order': sort_order
    })


def compare_universities(request, pk1, pk2):
    university1 = get_object_or_404(University, pk=pk1)
    university2 = get_object_or_404(University, pk=pk2)

    # Рейтинги QS Asia
    qs_asia_1 = university1.rankings.filter(system='QS Asia').first()
    qs_asia_2 = university2.rankings.filter(system='QS Asia').first()

    # Рейтинги QS World
    qs_world_1 = university1.rankings.filter(system='QS World').first()
    qs_world_2 = university2.rankings.filter(system='QS World').first()

    specialties_count1 = university1.specializations or 0
    specialties_count2 = university2.specializations or 0

    context = {
        'university1': university1,
        'university2': university2,
        'qs_asia_1_from': qs_asia_1.rank_from if qs_asia_1 else None,
        'qs_asia_1_to': qs_asia_1.rank_to if qs_asia_1 else None,
        'qs_asia_2_from': qs_asia_2.rank_from if qs_asia_2 else None,
        'qs_asia_2_to': qs_asia_2.rank_to if qs_asia_2 else None,
        'qs_world_1_from': qs_world_1.rank_from if qs_world_1 else None,
        'qs_world_1_to': qs_world_1.rank_to if qs_world_1 else None,
        'qs_world_2_from': qs_world_2.rank_from if qs_world_2 else None,
        'qs_world_2_to': qs_world_2.rank_to if qs_world_2 else None,
        'specialties_count1': specialties_count1,
        'specialties_count2': specialties_count2,
        'stipends_bk1': university1.stipends_bk,
        'stipends_mg1': university1.stipends_mg,
        'stipends_doc1': university1.stipends_doc,
        'stipends_bk2': university2.stipends_bk,
        'stipends_mg2': university2.stipends_mg,
        'stipends_doc2': university2.stipends_doc,
    }

    return render(request, 'compare.html', context)



GEMINI_API_KEY = "AIzaSyDGRnYRhYPJwMWfSctFJRkHArr1gP_KTcg"
genai.configure(api_key=GEMINI_API_KEY)

def chat_with_ai(request):
    return render(request, 'chat.html')


from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def chat_with_ai_api(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Метод не поддерживается"}, status=405)

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "Неверный JSON"}, status=400)

    user_message = data.get("message", "").strip()
    if not user_message:
        return JsonResponse({"error": "Пустой запрос"}, status=400)
    
    system_prompt = """
    Ты — эксперт-консультант по высшему образованию в Республике Казахстан. 
    Твоя задача — помогать пользователю выбрать университет, учитывая сильные стороны каждого. 
    Особое внимание уделяй следующим вузам: 
    - Назарбаев Университет
    - Университет Международного Бизнеса
    - Astana IT University
    - Казахстанско-Британский технический университет
    - Международный университет информационных технологий
    - Казахский национальный исследовательский технический университет имени К.И.Сатпаева
    - Евразийский национальный университет имени Л.Н. Гумилева
    - КазНУ им. аль-Фараби
    
    При ответе:
    - Давай советы по выбору направления и университета.
    - Если пользователь спрашивает про рейтинги, программы или преимущества, отвечай конкретно.
    - Отвечай дружелюбно, кратко и по существу.
    - Не упоминай другие страны, только вузы РК.
    """

    final_prompt = system_prompt + user_message


    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(final_prompt)

        bot_response = getattr(response, "text", "Ошибка: нет ответа от модели")
        bot_response_html = markdown.markdown(bot_response)

        return JsonResponse({"response": bot_response_html})

    except Exception as e:
        print("AI ERROR:", e)
        return JsonResponse({"error": str(e)}, status=500)

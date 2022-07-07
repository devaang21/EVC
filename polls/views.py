from secrets import choice
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Choice, Question

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,login,logout

def signup(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user( name, email, password)
        user.save()
        messages.success(request, " Your account has been successfully created")
        return redirect('/polls')


    else:
        return render(request, 'polls/signup.html')

def userlogin(request):
    if request.method == "POST":
        name = request.POST.get('email')
        pw = request.POST.get('password')
        user=authenticate(username=name, password=pw)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/polls")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/polls")

    else:
        return render(request, 'polls/login.html')

def userlogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/polls')

def index(request):
    if request.user.is_authenticated:
        question_list = Question.objects.order_by('-pub')[:5]
        context = {'question_list': question_list}
        return render(request, 'polls/index.html', context)
    else:
        return render(request, 'polls/login.html')


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def profile(request):
    email = request.user.email
    name = request.user.username
    print(email)
    uspoll = Question.objects.filter(pub=email)
    print(uspoll)
    return render(request, 'polls/profile.html', {'uspoll': uspoll,'email':email, 'name':name})

def createq(request):
    email = request.user.email
    uspoll = Question.objects.filter(pub=email)
    if request.method == "POST":
        ques = request.POST.get('question')
        question = Question(question_text= ques, pub=email)
        question.save()
        for i in range(4):
            c = request.POST.get('choice'+str(1))
            choice=Choice(question=question, choice_text=c)
            choice.save()
        messages.success(request, " Your Poll has been successfully created")
        return redirect("/polls")
    return render(request, 'polls/creatQ.html',{'n':[1,2,3,4], 'u':len(uspoll)>=5})

    
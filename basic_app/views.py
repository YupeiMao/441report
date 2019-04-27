





from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm,DeleteForm,EditForm,AddForm,SearchForm,PollForm,EditPollForm,ChoiceForm,UserPropertyForm

# Create your views here.
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo,Company,Position,Review,DeleteID,EditID,AddID,Poll,Choice,Vote

from django.db.models import Count
from django.db import connection
from django.views.generic import View
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
import datetime


a=0
b=0
c=0
d=0
e=0
f=0
arr = [['null',0,0,0,0,0,0],['null',0,0,0,0,0,0],['null',0,0,0,0,0,0],
    ['null',0,0,0,0,0,0],['null',0,0,0,0,0,0],['null',0,0,0,0,0,0],
    ['null',0,0,0,0,0,0],['null',0,0,0,0,0,0],['null',0,0,0,0,0,0],
    ['null',0,0,0,0,0,0],['null',0,0,0,0,0,0],['null',0,0,0,0,0,0],]
# from django.views.generic import CreateView
# try:
#     from django.core.urlresolvers import reverse_lazy
# except ImportError:
#     from django.urls import reverse
#     from django.utils.functional import lazy
#     reverse_lazy = lambda *args, **kwargs: lazy(reverse, str)(*args, **kwargs)

from basic_app import forms
from django.contrib.postgres.search import SearchVector
from django.views.generic import TemplateView
import plotly.offline as opy
import plotly.graph_objs as go

class Graph(TemplateView):
    template_name = 'basic_app/graphA.html'

    def get_context_data(self, **kwargs):
        context = super(Graph, self).get_context_data(**kwargs)
        global a,b,c,d,e,f
        global arr
        userarr = [a,b,c,d,e,f]

        arra = []
        for a in arr:
            row = []
            for i in range(7):
                if i>0:
                    row.append(int(a[i]))
            arra.append(row)

        # algorithm
        min_idx = 0
        min = 9999999999999
        for i in range(len(arra)):
            cur = 0
            for j in range(6):
                cur+=(arra[i][j] - userarr[j]) *(arra[i][j] - userarr[j])
            if cur < min:
                min = cur
                min_idx=i
        comp = arr[min_idx][0]
        for i in range(len(arr)):
            print(arr[i][0])
        data = [go.Scatterpolar(r = userarr,
                  theta = ['overall_ratings','work_balance_stars','culture_values_stars',
                   'career_opportunities_stars', 'company_benefit_stars', 'senior_management_stars'],
                  fill = 'toself'
                ),
                go.Scatterpolar(
      r = arra[min_idx],
      theta = ['overall_ratings','work_balance_stars','culture_values_stars',
       'career_opportunities_stars', 'company_benefit_stars', 'senior_management_stars'],
      fill = 'toself',
      name = 'Group B'
    )

                ]

        layout = go.Layout(
          polar = dict(
            radialaxis = dict(
              visible = True,
              range = [0, 5]
            )
          ),
          showlegend = False
        )

        fig = go.Figure(data=data, layout=layout)
        div = opy.plot(fig, auto_open=False, output_type='div')

        context['graph'] = div
        context['comp'] = comp
        picsrc = ['data:image/png;base64,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','data:image/png;base64,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','data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAaVBMVEU6VZ////81Up0yT5xgc61+jbsvTZyXo8hFXaOirM0nSJmlrs7O1OUkRpkfQ5doerLr7fTHzeE9WKHV2umHlcDy9Pnd4eyut9O1vtdZbat5ibmWoceGk7/M0eSrs9G/xtxMY6ZvgLVIYaWJ8OFBAAAC40lEQVR4nO3c63KqMBRAYU9iqaLg/d7W2vd/yE5nzt/ihjTsvTNrPQDDNxIDJDqZEBERERERERERERERERFZL4QYqydF7ZMcXKyadju97m/zzhZ7n8SqCY/T8Z+kXa19sv2LdbztRLqflu6EsXm8i3kOhbF9WffxeROG9tHT50xYbTd9fb6E7Vt/nydhqO9DgH6EcdZ7BPoSVpdhPjfCajUU6EQYhwN9COPncKALYdgeChe2socIv8LmnAJ0IIzXJKADYZMyCD0IE69R+8Iw+F7Gi7CVv67wKQzTVKB1YbMsXBhSbtdcCOtT6cLUudC8MD7SgbaFdepsb17YDHw140YYZn8ANC2M+78QWl57qvoMw8PuvHC3fljL70k3q7qu/a0Bt9LZ8HhpgvbJDioKgffWp28SvqRA7TMdmvDJ6egWKBV+Ob1EJ1LhyfB09yyZ0PFHKBMeG+3TTEgkPFXap5mQSGj5nuxpIuELQsshRGg/hAjthxCh/RAitB9ChPZDiNB+CBHarwxh6PiJci3ZWnptnv3SWRm4ev2920IgPN86jvDTfKsqrD4EiMR0V98qyceU1kF3iXgEofLy2wjCe/FX6Yful+kIwn3xwpXuOv8Iws/ihcr3NPmFa+UdU/mFS+XdKPmFZ+UtU/mFr8WPQ+3nx/zCi/K2t/xC7VcA2YUH7b2Z2YXqWxezCzfFf4bqmzOzC2/Ff9M8ihdqT4f5hdrDMLtQ+VXiCEL93x7mFiq/ShxBOC9+HL5pTxbZhVPtySK7UNuXXXhQH4a5hWvtZ6fswnf1ySL3GvBZ/yqdbGcdSf4O8q3rCLpL+P8LvxdFu02qjiNo455Vxn6arhAitB9ChPZDiNB+CBHaDyFC+yFEaD+ECO2HEKH9ECK0H0KE9kOI0H4IEdoPIUL7IURoP4QI7YcQof0QIrQfQoT2Q4jQfggR2g8hQvshRGg/hAjthxCh/RAitB9ChPZDiNB+CBH26BsaQkVVLImVewAAAABJRU5ErkJggg==','https://image.flaticon.com/teams/slug/google.jpg','data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAARVBMVEXwUSX9uBMyoNp/u0L////vRgz9tQAgnNj+4K6z1u54uDXK4bf4u7HI4LSw1O7+3qpytSX84d3n8d/e7ff/8dzvOgAAl9dLDuhEAAABIElEQVR4nO3PNw4CQRAAwQHOe+z/n0rKpgQj7an6A62KSKpdmt/m6ZZUFpCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQ8JTCNql3KVyPKalYsroXwsc6JxXN2SOsP8L6I6w/wvojrD/C+osxqe1ZfF/7kFT0SX22Qrh3WcU1qX4shEN3SYqQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkPD/vqoyjotFDAjwAAAAAElFTkSuQmCC','https://pmcvariety.files.wordpress.com/2019/02/netflix-logo-originals.jpg?w=640&h=360&crop=1']
        context['srcc'] = picsrc[min_idx]

        return context
cursor=connection.cursor()

# def post_list(request):
#     # object_list = page.all()
#     # paginator = Paginator(object_list, 8) # 3 posts in each page
#
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#     return render(request,
#                   'basic_app/search_company.html',
#                   {'page': page,
#                    'posts': posts})

def index(request):
     cur=connection.cursor()
     cur.execute('''select c.name, round(avg(to_number(r.overall_ratings,'99999999999999999D99')),0),round(avg(to_number(r.work_balance_stars,'99999999999999999D99')),0),round(avg(to_number(r.culture_values_stars,'99999999999999999D99')),0),round(avg(to_number(r.career_opportunities_stars,'99999999999999999D99')),0),round(avg(to_number(r.company_benefit_stars,'99999999999999999D99')),0),round(avg(to_number(r.senior_management_stars,'99999999999999999D99')),0)'''+
'from basic_app_review r join basic_app_company c on r.cid_id=c.cid '+
'''where r.overall_ratings not in ('none') and r.work_balance_stars not in ('none') and r.culture_values_stars not in ('none') and r.career_opportunities_stars not in ('none') and r.company_benefit_stars not in ('none') and r.senior_management_stars not in ('none')'''+
'group by c.name')
     global arr
     arr=cur.fetchall()
     print(int(arr[2][1]))

     return render(request,'basic_app/index.html',{'arr':arr})

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method=="POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        #valid
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'basic_app/registration.html',
            {'user_form':user_form,'profile_form':profile_form,
            'registered':registered})

@login_required
def uProp(request):
    registered = False
    if request.user.is_authenticated:
        cur_userid = request.user.id #raw userid
        print(cur_userid)
        cur_userprofileid = cur_userid - 6
        u = UserProfileInfo.objects.filter(user=cur_userid)
        print(u)
    if request.method=="POST":
        user_property = UserPropertyForm(data=request.POST)

        #valid
        if user_property.is_valid():
            up = user_property.save(commit=False)
            up.user=u
            global a,b,c,d,e,f
            a = up.overall_ratings
            b = up.work_balance_stars
            c = up.culture_values_stars
            d = up.career_opportunities_stars
            e = up.company_benefit_stars
            f = up.senior_management_stars
            up.save()

            registered = True
        else:
            print(user_property.errors)
    else:
        user_property = UserPropertyForm()

    return render(request,'basic_app/graph.html',
            {'user_property':user_property,
            'registered':registered})


def search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            results = Review.objects.annotate(
                    search=SearchVector('summary', 'pros','cons','advices_to_management'),
                    ).filter(search=query)

    return render(request,
                  'basic_app/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})

def search_company(request):
    companyname = request.POST.get('companyname')
    cur=connection.cursor()
    cur.execute('select * '+
                'from basic_app_review r join basic_app_company c on r.cid_id=c.cid join basic_app_position p on p.pid =r.pid_id '+
                'where c.name=%s ORDER BY r.helpful_count DESC',[companyname])

    cur_review_info=cur.fetchall()


    return render(request,'basic_app/search_company.html',{"cur_review_info":cur_review_info})

def software_engineer(request):

    cur=connection.cursor()
    cur.execute('select * '+
                'from basic_app_review r join basic_app_company c on r.cid_id=c.cid join basic_app_position p on p.pid =r.pid_id '+
                'where p.title like %s ORDER BY r.helpful_count DESC',['%Software%'])

    arr=cur.fetchall()

    cur_dict = {"cur_review_info":arr}

    return render(request,'basic_app/software_engineer.html',context=cur_dict)

def intern(request):

    cur=connection.cursor()
    cur.execute('select * '+
                'from basic_app_review r join basic_app_company c on r.cid_id=c.cid join basic_app_position p on p.pid =r.pid_id '+
                'where p.title like %s ORDER BY r.helpful_count DESC',['%Intern%'])

    arr=cur.fetchall()

    cur_dict = {"cur_review_info":arr}

    return render(request,'basic_app/intern.html',context=cur_dict)

def cloud(request):

    cur=connection.cursor()
    cur.execute('select * '+
                'from basic_app_review r join basic_app_company c on r.cid_id=c.cid join basic_app_position p on p.pid =r.pid_id '+
                'where p.title like %s ORDER BY r.helpful_count DESC',['%Cloud%'])

    arr=cur.fetchall()

    cur_dict = {"cur_review_info":arr}

    return render(request,'basic_app/cloud.html',context=cur_dict)

def network(request):

    cur=connection.cursor()
    cur.execute('select * '+
                'from basic_app_review r join basic_app_company c on r.cid_id=c.cid join basic_app_position p on p.pid =r.pid_id '+
                'where p.title like %s ORDER BY r.helpful_count DESC',['%Network%'])

    arr=cur.fetchall()

    cur_dict = {"cur_review_info":arr}

    return render(request,'basic_app/network.html',context=cur_dict)

def hardware(request):

    cur=connection.cursor()
    cur.execute('select * '+
                'from basic_app_review r join basic_app_company c on r.cid_id=c.cid join basic_app_position p on p.pid =r.pid_id '+
                'where p.title like %s ORDER BY r.helpful_count DESC',['%Hardware%'])

    arr=cur.fetchall()

    cur_dict = {"cur_review_info":arr}

    return render(request,'basic_app/hardware.html',context=cur_dict)

def web(request):

    cur=connection.cursor()
    cur.execute('select * '+
                'from basic_app_review r join basic_app_company c on r.cid_id=c.cid join basic_app_position p on p.pid =r.pid_id '+
                'where p.title like %s ORDER BY r.helpful_count DESC',['%Web%'])

    arr=cur.fetchall()

    cur_dict = {"cur_review_info":arr}

    return render(request,'basic_app/web.html',context=cur_dict)

def data(request):

    cur=connection.cursor()
    cur.execute('select * '+
                'from basic_app_review r join basic_app_company c on r.cid_id=c.cid join basic_app_position p on p.pid =r.pid_id '+
                'where p.title like %s ORDER BY r.helpful_count DESC',['%Data%'])

    arr=cur.fetchall()

    cur_dict = {"cur_review_info":arr}

    return render(request,'basic_app/data.html',context=cur_dict)

def review(request):
    return render(request,'basic_app/review.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed")
            print("Username: {} and password: {}".format(username,password))
            return HttpResponse("invalid login details supplied")
    else:
        return render(request,'basic_app/login.html',{})


def add_helpful(request,rid):
    rid=request.POST['choice']

    cur=connection.cursor()
    cur.execute('UPDATE basic_app_review SET helpful_count+=1 WHERE rid=%s',[rid])

    return render(request,'basic_app/add_helpful.html')




'''
    pass Review and corresponding Position and Company information
    into single object to be transferred to template
'''
class Cur_review_info():
    def __init__(self,Review,Position,Company):
        self.Review = Review
        self.Position = Position
        self.Company = Company

@login_required
def manage_review(request):

    if request.user.is_authenticated:
        cur_userid = request.user.id #raw userid
        cur_userprofileid = cur_userid - 6

    cur=connection.cursor()
    cur.execute('select r.rid,c.name,c.country,c.state,c.city,ap.title,r.summary '+
                'from basic_app_review r join basic_app_company c on r.cid_id=c.cid '+
                'join basic_app_position ap on ap.pid=r.pid_id '+
                 'where r.uid_id =%s',[request.user.id])
    arr=cur.fetchall()
    cur_dict = {"cur_review_info":arr}

    return render(request,'basic_app/managereview.html',context=cur_dict)

@login_required
def delete_review(request):
    if request.method=="POST":
        delete_form = DeleteForm(data=request.POST)
        #valid
        aaa = delete_form.save()
        this_rid = aaa.did;
        print(this_rid)
        cur=connection.cursor()
        cur.execute('DELETE from basic_app_review WHERE rid=%s',[this_rid] )

        #Review.objects.filter(rid=this_rid).delete()

    else:
        delete_form = DeleteForm()
    return render(request,'basic_app/delete.html',
            {'delete_form':delete_form})


@login_required
def edit_review(request):
    if request.method=="POST":
        edit_form = EditForm(data=request.POST)
        #valid
        aaa = edit_form.save()
        this_rid = aaa.eid;
        this_summary = aaa.summary;
        print(this_rid)
        print(this_summary)

        cur=connection.cursor()
        cur.execute('UPDATE basic_app_review SET summary =%s WHERE rid=%s',[this_summary,this_rid] )


    else:
        edit_form = EditForm()
    return render(request,'basic_app/edit.html',
            {'edit_form':edit_form})


@login_required
def add_review(request):
    if request.method=="POST":
        add_form = AddForm(data=request.POST)
        #valid
        aaa = add_form.save()
        new_company = Company(aaa.cid,aaa.name,aaa.country,aaa.state,aaa.city)
        new_company.save()

        print("adddinnngngggg")
    else:
        add_form = AddForm()
    return render(request,'basic_app/add.html',
            {'add_form':add_form})

@login_required
def polls_list(request):
    polls=Poll.objects.all()

    paginator = Paginator(polls, 5)

    page = request.GET.get('page')
    polls = paginator.get_page(page)

    return render(request, 'basic_app/polls_list.html',{'polls':polls})

@login_required
def poll_detail(request, poll_id):
    """
    Render the poll_detail.html template which allows a user to vote
    on the choices of a poll
    """
    # poll = Poll.objects.get(id=poll_id)
    poll = get_object_or_404(Poll, id=poll_id)
    user_can_vote = poll.user_can_vote(request.user)
    results = poll.get_results_dict()
    context = {'poll': poll, 'user_can_vote': user_can_vote, 'results': results}
    return render(request, 'basic_app/poll_detail.html', context)

@login_required
def poll_vote(request, poll_id):

    poll = get_object_or_404(Poll, id=poll_id)

    if not poll.user_can_vote(request.user):
        messages.error(request, 'You have already voted on this poll')
        return redirect('basic_app:poll_detail', poll_id=poll_id)

    choice_id = request.POST.get('choice')
    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        new_vote = Vote(user=request.user, poll=poll, choice=choice)
        new_vote.save()
    else:
        messages.error(request, 'No Choice Was Found!')
        return redirect('basic_app:poll_detail', poll_id=poll_id)

    return redirect('basic_app:poll_detail', poll_id=poll_id)


@login_required
def add_poll(request):
    if request.method == "POST":
        form = PollForm(request.POST)
        if form.is_valid():
            new_poll = form.save(commit=False)
            new_poll.pub_date = datetime.datetime.now()
            new_poll.owner = request.user
            new_poll.save()
            new_choice1 = Choice(
                                    poll = new_poll,
                                    choice_text=form.cleaned_data['choice1']
                                ).save()
            new_choice2 = Choice(
                                    poll = new_poll,
                                    choice_text=form.cleaned_data['choice2']
                                ).save()
            messages.success(
                            request,
                            'Poll and Choices added!',
                            extra_tags='alert alert-success alert-dismissible fade show'
                            )
            return redirect('basic_app:polls_list')
    else:
        form = PollForm()
    context = {'form': form}
    return render(request, 'basic_app/add_poll.html', context)

# -*- coding: utf-8 -*-
from django.http.response import HttpResponse, Http404
from django.http.request import HttpRequest
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, redirect
from keeper.models import Keeper, Feedback, Suggestions, SearchLabelKeeper
from django.core.exceptions import ObjectDoesNotExist
from django.middleware import csrf
from django.views.decorators.csrf import csrf_protect, requires_csrf_token, csrf_exempt
from django.core.paginator import Paginator
from django.contrib import auth
from keeper.forms import FeedbackForm, KeeperForm, SearchLabelKeeperForm
from datetime import datetime, date, time
from django.db.models import Q, Count
from operator import __or__ as OR
from operator import __and__ as AND
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test
from functools import reduce
from django.contrib.auth.models import User, Group
from itertools import chain
# from .widgets import CKEditorWidget

from django.shortcuts import render
from django import forms
# Create your views here.


def basic_one(request):
    view = "<span style='color: red;'>Заявку могут оставить только зарегистрированные пользователи!</span>"
    html = "<html><body> this is %s view</body></html>" % view
    return HttpResponse(html)

#
def group_required(*group_names):
    def in_groups(user):
        if user.is_authenticated():
            if user.is_superuser or bool(user.groups.filter(name__in=group_names)):
                return True
        return False
    return user_passes_test(in_groups)




@csrf_protect
def test_select(request):
    all_SearchLabelKeeper = SearchLabelKeeper.objects.all()
    args = {}
    args = {}
    # args['keeper_id'] = keeper_id
    # args['KeeForm'] = form
    args['username'] = auth.get_user(request).username
    args['SearchLabelKeepers'] = SearchLabelKeeper.objects.all()
    # args['keeper_search'] = article.keep_hashTag.all()
    # args['keep_title'] = article.keep_title

    args['SearchLabelKeepers'] = all_SearchLabelKeeper
    if request.POST:
        args = {}
        args['SearchLabelKeepers'] = all_SearchLabelKeeper
        if request.POST.getlist('search_attribute') or request.POST.getlist('search_and_only'):
            search_and_l = ''.join(request.POST.getlist('search_attribute'))
            args['search_attribute'] = request.POST.getlist('search_attribute')
            args['search_and_only'] = request.POST.getlist('search_and_only')

            all_keeper = Keeper.objects.all()
            for search_i in request.POST.getlist('search_attribute'):
                all_keeper = all_keeper.filter(keep_hashTag=SearchLabelKeeper.objects.filter(searchlabelkeeper_marker=search_i))
            # all_keeper = all_keeper.filter(keep_hashTag=None)# без тегов
            # qss = Keeper.keep_hashTag.through.objects.values('keeper_id').annotate(count=Count('keeper_id')).filter(count=len(request.POST.get('hero[]')))
            # qsslen = []
            # if request.POST.get('search_and_only') == 'only_and':
            #
            #     for keeper_id_filter in qss.values('keeper_id'):
            #         qsslen.append(keeper_id_filter['keeper_id'])
            #     all_keeper = all_keeper.filter(id__in=qsslen)
            args['keeps'] = all_keeper
            # args['test2'] = auth.get_user(request).username
            # args['test2'] = User.objects.filter(groups__name='admin')
            for grup in Group.objects.filter(user=User.objects.filter(username=auth.get_user(request).username)):
                args['test2'] = Group.objects.filter(name='admin')
                if str(grup) == 'admin':
                    args['grups'] = 'asdasd'

                    # args['test2'] = request.POST.getlist('search_and_only')

                    # if search_i.keep_hashTag.all().count() < 2:
                    #     all_keeper = all_keeper.filter(keep_hashTag__searchlabelkeeper_marker__contains=search_i)
                #     args['keeps'] = all_keeper
                # all_keeper = all_keeper.filter(keep_hashTag=SearchLabelKeeper.objects.get(id=2)).distinct('keep_hashTag')
            # args['keeps'] = all_keeper
            # args['keeps'] = keep_search_or_and(search_and=request.POST.getlist('hero[]'), search_or=request.POST.getlist('hero2[]'), search_text=request.POST['search_text'])
        # if request.POST.getlist('hero[]'):
        #     serand = request.POST.getlist('hero[]')
        #     args['keeps'] = keep_search_and(serand)
        # elif request.POST.getlist('hero2[]'):
        #     seror = request.POST.getlist('hero2[]')
        #     args['keeps'] = keep_search_or(seror)

    # return render_to_response('test_select.html', args)
    return render(request, 'test_select.html', args)


def keep_search_or_and(search_or_and_only, search_attribute, search_text):

    if search_or_and_only == 'search_and':
        all_keeper = Keeper.objects.all()
        for search_i in search_attribute:
            all_keeper = all_keeper.filter(keep_hashTag=SearchLabelKeeper.objects.filter(searchlabelkeeper_marker=search_i))
    elif search_or_and_only == 'search_or':
        lst = []
        for search_i in search_attribute:
            lst.append(Q(keep_hashTag=SearchLabelKeeper.objects.filter(searchlabelkeeper_marker=search_i)))
        all_keeper = Keeper.objects.filter(reduce(OR, lst)).distinct()
    elif search_or_and_only == 'search_and_only':
        lst = []
        all_keeper = Keeper.objects.all()
        for search_i in search_attribute:
            all_keeper = all_keeper.filter(keep_hashTag=SearchLabelKeeper.objects.filter(searchlabelkeeper_marker=search_i))
            qss = Keeper.keep_hashTag.through.objects.values('keeper_id').annotate(count=Count('keeper_id')).filter(
                count=len(search_attribute))
            for keeper_id_filter in qss.values('keeper_id'):
                lst.append(keeper_id_filter['keeper_id'])
            all_keeper = all_keeper.filter(id__in=lst) # только эти

    else:
        all_keeper = Keeper.objects.all()

    all_keeper = all_keeper.filter(Q(keep_text__icontains=search_text) | Q(keep_title__icontains=search_text))
    return(all_keeper)
# @permission_required('', login_url='/auth/login/')
# @group_required('admin', 'admin2')
@csrf_protect
def keepers(request, page_number=1):
    args = {}
    args['username'] = auth.get_user(request).username
    args['login'] = auth.get_user(request).username
    args['SearchLabelKeepers'] = SearchLabelKeeper.objects.all()
    if request.POST:
        if request.POST.getlist('search_attribute') or \
                request.POST.getlist('search_text') or \
                request.POST.get('search_or_and_only'):
            all_keeper = keep_search_or_and(search_attribute=request.POST.getlist('search_attribute'),
                                            search_or_and_only=request.POST.get('search_or_and_only'),
                                            search_text=request.POST['search_text'])
            request.session.set_expiry(6000)
            args['search_attribute'] = request.session["search_attribute"] = request.POST.getlist('search_attribute')
            args['search_text'] = request.session["search_text"] = request.POST['search_text']
            args['search_or_and_only'] = request.session["search_or_and_only"] = request.POST.get('search_or_and_only')
            all_keeper = all_keeper.order_by('-keep_data')
            current_page = Paginator(all_keeper, 4)
            args['keeps'] = current_page.page(page_number)
            args['page_prior'] = int(page_number) - 4
            args['page_afterwards'] = int(page_number) + 4
            args['num_pages_'] = int(current_page.num_pages) - 4

    else:
        if ("search_attribute" in request.session) or \
                ("search_text" in request.session) or \
                ("search_or_and_only" in request.session):
            all_keeper = keep_search_or_and(search_attribute=request.session["search_attribute"],
                                            search_text=request.session["search_text"],
                                            search_or_and_only=request.session["search_or_and_only"])
            args['search_attribute'] = request.session["search_attribute"]
            args['search_text'] = request.session["search_text"]
            args['search_or_and_only'] = request.session["search_or_and_only"]
        else:
            all_keeper = Keeper.objects.all().order_by('-keep_data')

        all_keeper = all_keeper.order_by('-keep_data')
        current_page = Paginator(all_keeper, 4)
        args['keeps'] = current_page.page(page_number)
        args['page_prior'] = int(page_number) - 4
        args['page_afterwards'] = int(page_number) + 4
        args['num_pages_'] = int(current_page.num_pages) - 4

    return render(request, 'Keepers.html', args)

def keepers_clean_search(request):
    request.session["search_attribute"] = []
    request.session["search_text"] = ""
    request.session["search_or_and_only"] = "search_and"
    return redirect('/')

@csrf_protect
def keeper(request, keeper_id=1, page_number=1):
    article = Keeper.objects.get(id=keeper_id)
    all_feedbacks = Feedback.objects.filter(feedback_keeper_id=keeper_id).order_by('-feedback_data')
    current_page = Paginator(all_feedbacks, 5)
    feedback_form = FeedbackForm
    args = {}
    # args.update(csrf(request))
    args['keep'] = article
    args['feedbacks'] = current_page.page(page_number)
    args['FedForm'] = feedback_form
    args['username'] = auth.get_user(request).username
    args['keeper_search'] = article.keep_hashTag.all()
    # args['usergroup'] = auth.get_user(request)
    return render(request, 'Keeper.html', args)


def addfeedback(request, keeper_id):
    if request.POST:
        FedForm = FeedbackForm(request.POST)
        if FedForm.is_valid():
            feedback = FedForm.save(commit=False)
            feedback.feedback_data = datetime.today()
            feedback.feedback_keeper = Keeper.objects.get(id=keeper_id)
            feedback.feedback_from = request.user
            FedForm.save()
    return redirect('/keeper/get/%s/' % keeper_id)
@group_required('admin')
@csrf_protect
def newkeeperform(request):
    keeper_form = KeeperForm
    args = {}
    args['KeeForm'] = keeper_form
    args['username'] = auth.get_user(request).username
    args['SearchLabelKeepers'] = SearchLabelKeeper.objects.all()
    # args.update(csrf(request))
    return render(request, 'NewKeeper.html', args)
@group_required('admin')
@csrf_protect
def addkeeper(request):
    if request.POST:
        KeeForm = KeeperForm(request.POST)
        if KeeForm.is_valid():
            feedback = KeeForm.save(commit=False)
            feedback.keep_data = datetime.today()
            feedback.keep_title = request.POST.get('keep_title')
            feedback.save()
            for Q_set_keep_hastag_add in request.POST.getlist('search_attribute'):
                feedback.keep_hashTag.add(*SearchLabelKeeper.objects.filter(Q(searchlabelkeeper_marker__iexact=Q_set_keep_hastag_add)))
    return redirect('/')

@csrf_protect
def keeper_status(request, keeper_id=1):
    article = Keeper.objects.get(id=keeper_id)

    return redirect('/')
@group_required('admin')
@csrf_protect
def editkeeperform(request, keeper_id):
    article = Keeper.objects.get(id=keeper_id)
    form = KeeperForm(instance=article)
    args = {}
    args['keeper_id'] = keeper_id
    args['KeeForm'] = form
    args['username'] = auth.get_user(request).username
    args['SearchLabelKeepers'] = SearchLabelKeeper.objects.all()
    args['keeper_search'] = article.keep_hashTag.all()
    args['keep_title'] = article.keep_title
    # args.update(csrf(request))
    return render(request, 'EditKeeper.html', args)
@group_required('admin')
def editkeeper(request, keeper_id):
    article = Keeper.objects.get(id=keeper_id)
    if request.POST:
        KeeForm = KeeperForm(request.POST, instance=article)
        if KeeForm.is_valid():
            feedback = KeeForm.save(commit=False)
            feedback.keep_data = datetime.today()
            feedback.save()
            for Q_set_keep_hastag_del in feedback.keep_hashTag.all():
                feedback.keep_hashTag.remove(Q_set_keep_hastag_del)
            for Q_set_keep_hastag_add in request.POST.getlist('search_attribute'):
                feedback.keep_hashTag.add(*SearchLabelKeeper.objects.filter(Q(searchlabelkeeper_marker__iexact=Q_set_keep_hastag_add)))
    return redirect('/keeper/get/%s/' % keeper_id)

def deletekeeper(request, keeper_id):
    article = Keeper.objects.get(id=keeper_id)
    article.delete()
    return redirect('/')

@csrf_protect
def keepermarker(request):
    all_SearchLabelKeeper = SearchLabelKeeper.objects.all().order_by('-id')
    SearchLabelKeeper_Form = SearchLabelKeeperForm
    args = {}
    args['SearchLabelKeeperForm'] = SearchLabelKeeper_Form
    args['SearchLabelKeepers'] = all_SearchLabelKeeper
    args['username'] = auth.get_user(request).username
    # args.update(csrf(request))
    return render(request, 'KeeperMarkerEdit.html', args)
@csrf_protect
def keepermarkereedit(request, marker_id):
    article = SearchLabelKeeper.objects.get(id=marker_id)
    form = SearchLabelKeeperForm(instance=article)
    args = {}
    args['marker_id'] = marker_id
    args['SearchLabelKeeperForm'] = form
    args['username'] = auth.get_user(request).username
    if request.POST:
        if len(SearchLabelKeeper.objects.filter(
                searchlabelkeeper_marker__iexact=request.POST.get('searchlabelkeeper_marker').strip())) > 0:
            text = request.POST.get('searchlabelkeeper_marker').strip()
            return redirect('/error/%s/' % text)
        SearchLabelKeeper_Form = SearchLabelKeeperForm(request.POST, instance=article)
        if SearchLabelKeeper_Form.is_valid():
            SearchLabel = SearchLabelKeeper_Form.save(commit=False)
            SearchLabel
            SearchLabel.save()
            return redirect('/keepermarkeredit/')
    return render(request, 'thekeepermarkereedit.html', args)



def keepermarkeredit_add(request):
    if request.POST:
        SearchLabelKeeper_Form = SearchLabelKeeperForm(request.POST)
        if SearchLabelKeeper_Form.is_valid():
            if len(SearchLabelKeeper.objects.filter(searchlabelkeeper_marker__iexact=request.POST.get('searchlabelkeeper_marker').strip())) >0:
                text = request.POST.get('searchlabelkeeper_marker').strip()
                return redirect('/error/%s/' % text)
                # return redirect('/1/')
            SearchLabel = SearchLabelKeeper_Form.save(commit=False)
            SearchLabel.save()
        return redirect('/keepermarkeredit/')

def keepermarkeredit_delete(request, marker_id):
    article = SearchLabelKeeper.objects.get(id=marker_id)
    article.delete()
    return redirect('/keepermarkeredit/')
@csrf_protect
def Error(request, error_text=''):
    args ={}
    args['username'] = auth.get_user(request).username
    args['Error_text'] = error_text
    return render(request, 'Error_keeper.html', args)

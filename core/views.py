from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth import logout
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.utils.http import is_safe_url
from core.models import *
from core.forms import *
from datetime import date
import socket
import misaka


def save_comment(request, form, problem):
    if request.user.is_anonymous():
        return False

    if form.is_valid():
        form2 = form.save(commit=False)
        form2.text = misaka.html(form2.text, extensions=misaka.EXT_NO_INTRA_EMPHASIS | misaka.EXT_TABLES | misaka.EXT_FENCED_CODE | misaka.EXT_AUTOLINK | misaka.EXT_STRIKETHROUGH | misaka.EXT_SPACE_HEADERS | misaka.EXT_SUPERSCRIPT, render_flags=misaka.HTML_ESCAPE)
        if form['ancestor'].value() == '':
            form2.user = request.user if request.user.is_authenticated() else None
            form2.path = []
            form2.problem = problem
        else:
            try:
                parent = Comment.objects.get(id=int(form['ancestor'].value()))
                form2.parent = parent
                form2.user = request.user if request.user.is_authenticated() else None
                form2.path = parent.path
                form2.problem = problem
            except:
                messages.error(request, 'The comment you are replying to does not exist.')

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        if settings.HTTPBL_KEY and settings.HTTPBL_ADDRESS:
            try:
                iplist = ip.split('.')
                iplist.reverse()

                query = settings.HTTPBL_KEY + '.' + '.'.join(iplist) + '.' + settings.HTTPBL_ADDRESS

                httpbl_result = socket.gethostbyname(query)
                httpbl_resultlist = httpbl_result.split('.')

                #Check if response is proper
                if httpbl_resultlist[0] == "127":
                    #DO SOME MORE CHECKING OF ALL THE VALUES RETURNED
                    if httpbl_resultlist[2] > settings.HTTPBL_TL:
                        form2.spam = True
                    else:
                        form2.spam = False
                else:
                    form2.spam = True
            except:
                form2.spam = False
        else:
            form2.spam = False

        form2.save()
        form2.path.append(form2.id)
        form2.save()
        messages.success(request, 'Thanks for commenting!')
        return True
    else:
        messages.error(request, 'There was a problem submitting your comment. Please try again.')

    return False

def preview(request):
    return HttpResponse(misaka.html(request.GET.get('text'), extensions=misaka.EXT_NO_INTRA_EMPHASIS | misaka.EXT_TABLES | misaka.EXT_FENCED_CODE | misaka.EXT_AUTOLINK | misaka.EXT_STRIKETHROUGH | misaka.EXT_SPACE_HEADERS | misaka.EXT_SUPERSCRIPT, render_flags=misaka.HTML_ESCAPE))

def delete_comment(request, comment_id=None):
    if request.is_ajax() and comment_id:
        comment = Comment.objects.get(id=comment_id)
        if request.user == comment.user or request.user.is_superuser:
            if comment.has_children():
                comment.deleted = True
                comment.save()
                return HttpResponse('deleted')
            else:
                comment.delete()
                return HttpResponse('removed')
    return HttpResponseBadRequest('Error deleting comment. Please make sure you\'re logged in')

def home(request):
    show_comments = request.GET.get('show')
    problem = Problem.objects.filter(date__lte=date.today())[0]
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        success = save_comment(request, form, problem)

        # Save name
        if success:
            show_comments = True
            if request.user.is_anonymous():
                form = CommentForm(initial={'name': form.data['name']})

    comment_tree = Comment.objects.select_related('user').filter(problem=problem, spam=False).order_by('path').extra(select={'provider': 'SELECT provider FROM social_auth_usersocialauth WHERE social_auth_usersocialauth.user_id = core_comment.user_id'})

    return render(request, 'core/home.html', {'problem': problem,
                                              'comment_tree': comment_tree,
                                              'form': form,
                                              'request': request,
                                              'show_comments': show_comments})


def problem(request, slug=None):
    show_comments = request.GET.get('show')
    problem = get_object_or_404(Problem, slug=slug)
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        success = save_comment(request, form, problem)

        # Save name
        if success:
            show_comments = True
            if request.user.is_anonymous():
                form = CommentForm(initial={'name': form.data['name']})

    comment_tree = Comment.objects.select_related('user').filter(problem=problem, spam=False).order_by('path').extra(select={'provider': 'SELECT provider FROM social_auth_usersocialauth WHERE social_auth_usersocialauth.user_id = core_comment.user_id'})

    return render(request, 'core/home.html', {'problem': problem,
                                              'comment_tree': comment_tree,
                                              'form': form,
                                              'request': request,
                                              'show_comments': show_comments})


def past_problems(request):
    problem_list = Problem.objects.filter(date__lte=date.today())

    page = request.GET.get('page')
    paginator = Paginator(problem_list, 20)
    try:
        problems = paginator.page(page)
    except PageNotAnInteger:
        problems = paginator.page(1)
    except EmptyPage:
        problems = paginator.page(paginator.num_pages)

    return render(request, 'core/past_problems.html', {'problems': problems, 'request': request})


def suggest(request):
    form = ProblemSuggestionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Thanks for suggesting a problem! Be sure to check back daily to see if your problem was selected')
            form = ProblemSuggestionForm()  # Clear form
        else:
            messages.error(request, 'There was a problem submitting your suggestion. Please try again.')

    return render(request, 'core/suggest.html', {'form': form, 'request': request})


def subscribe(request):
    if request.is_ajax():
        email = request.GET.get('email')
        try:
            obj, created = Subscriber.objects.get_or_create(email=email)
            if obj.status:
                template = get_template('core/email/confirm.html')
                msg = EmailMultiAlternatives(
                    subject="Problem of the Day Subscription Confirmation",
                    from_email="Problem of the Day <no-reply@problemotd.com>",
                    to=[obj.email]
                )
                msg.attach_alternative(template.render(Context({'status': obj.status})), "text/html")
                try:
                    msg.send(fail_silently=True)
                except:
                    return HttpResponseServerError('Error creating subscription. Please try again')
            else:
                return HttpResponse('Your subscription is already active! Please check your spam folder')
            return HttpResponse('Thank you for subscribing! Please check your e-mail to confirm your subscription')
        except:
            return HttpResponseBadRequest('Error creating subscription. Please double check your email and try again')
    return HttpResponseBadRequest('Error creating subscription. Please try again')


def confirm_email(request):
    status = request.GET.get('status')
    subscriber = get_object_or_404(Subscriber, status=status)
    subscriber.status = ''
    subscriber.save()
    messages.success(request, "You're e-mail has been confirmed. Thanks for subscribing!")
    return redirect('home')


def update_subscription(request):
    try:
        md_email = request.GET.get('md_email')
        subscriber = Subscriber.objects.get(email=md_email)
    except:
        messages.error(request, 'Unable to unsubscribe. Please click the link from your e-mail')
        return redirect('home')
    if request.method == 'POST':
        unsub = request.POST.get('unsub')
        if unsub:
            subscriber.delete()
            messages.success(request, 'Successfully unsubscribed')
            return redirect('home')
        else:
            subscriber.weekly = not subscriber.weekly
            subscriber.save()
            messages.success(request, 'Subscription successfully updated')
            return redirect('home')
    else:
        md_email = request.GET.get('md_email')
        return render(request, 'core/update_subscription.html', {'md_email': md_email, 'weekly': subscriber.weekly})
    
def login(request):
    next = request.GET.get('next', '/')
    if is_safe_url(next, request.get_host()):
        if request.user.is_authenticated():
            return redirect(request.GET.get('next', '/'))
        return render(request, 'core/login.html', {'next': request.GET.get('next', '/')})
    return redirect('home')
    
def logout(request):
    logout(request)
    return redirect('home')

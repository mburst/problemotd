from django.core.management.base import BaseCommand
from core.models import Problem, Subscriber
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Sends out problem of the day mon-fri'

    def handle(self, *args, **options):
        today = date.today()
        # Don't send if Saturday or Sunday
        if today.weekday() < 5:
            daily_subscribers = Subscriber.objects.filter(status='', weekly=False).values_list('email', flat=True)
            weekly_subscribers = Subscriber.objects.filter(status='', weekly=True).values_list('email', flat=True)
            problem = Problem.objects.filter(date=today)[:1]
            template = get_template('core/email/problems.html')

            #Forgot to post?
            if problem and daily_subscribers:
                msg = EmailMultiAlternatives(
                    subject="Problem of the Day: " + str(today),
                    from_email="Problem of the Day <no-reply@problemotd.com>",
                    to=daily_subscribers
                )
                msg.attach_alternative(template.render(Context({'problems': problem})), "text/html")
                msg.send(fail_silently=True)

            #Send weekly on Friday (4)
            if today.weekday() == 4:
                monday = today-timedelta(days=5)
                problems = Problem.objects.filter(date__range=(monday, today))
                if problems and weekly_subscribers:
                    msg = EmailMultiAlternatives(
                        subject="Problem of the Day: Week of " + str(monday),
                        from_email="Problem of the Day <no-reply@problemotd.com>",
                        to=weekly_subscribers
                    )
                    msg.attach_alternative(template.render(Context({'problems': problems})), "text/html")
                    msg.send(fail_silently=True)

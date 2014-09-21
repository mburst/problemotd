# Problem of the Day

## Install

You'll need to have python installed. My development environment has 2.7 but I believe it'll work on 3.x. You'll also need Postgres 9.x installed

```
pip install -r requirements.txt
python manage.py syncdb
```

Create a user account when prompted to do so.

You can login at /admin (the login on the homepage doesn't work with Django authentication). From the admin panel create a new problem.

```
python manage.py runserver
#or
python tornadows.py --port 8000
```

## Cron Jobs

E-mail out problem daily (requires MANDRILL_API_KEY)

```
python manage.py send_problem.py
```

## How to get Involved

* You can always suggest problems at [http://www.problemotd.com/suggest/](http://www.problemotd.com/suggest/)
* Check Github issues for open tickets that need to be fixed
* Create an issue for the feature you'd like to work on. We can work out a scope and get you started ASAP
* [Contact me](http://maxburstein.com/contact/) and we can work out an idea that fits your interests

Along with your first pull request please update the AUTHORS file

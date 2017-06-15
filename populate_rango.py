#скрипт для заполнения базы данных
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tango_with_django_project.settings")

import django

django.setup()

from rango.models import Category, Page

def populate():
    python_cat=add_cat("Python", views=128, likes=64)
    add_page(cat=python_cat, title="Official Python Tutorial", url="http://docs.python.org/3/tutorial/", views=100)
    add_page(cat=python_cat, title="How to Think like a Computer Scientist", url="http://www.greenteapress.com/thinkpython/", views=98)
    add_page(cat=python_cat, title="Learn Python in 10 Minutes", url="http://www.korokithakis.net/tutorials/python/", views=80)

    django_cat=add_cat("Django", views=64, likes=32)
    add_page(cat=django_cat, title="Official Django Tutorial", url="https://docs.djangoproject.com/en/1.8/intro/", views=50)
    add_page(cat=django_cat, title="Django Rocks", url="http://www.djangorocks.com/", views=30 )
    add_page(cat=django_cat, title="Mastering Django", url="http://djangobook.com/", views=40 )

    frame_cat=add_cat("Other Frameworks", views=32, likes=16)
    add_page(cat=frame_cat, title="Bottle", url="http://bottlepy.org/docs/dev/", views=20)
    add_page(cat=frame_cat, title="Flask", url="http://flask.pocoo.org", views=18)

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {} - {}".format(str(c), str(p)))

def add_page(cat, title, url, views=0):
    p=Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.view=views
    p.save()
    return p

def add_cat(name, views,likes):
    c=Category.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
    c.save()
    return c

if __name__=="__main__":
    print("Starting Rango population script...")
    populate()

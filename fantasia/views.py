import os
import pathlib

from PIL import Image
from django.http import HttpResponse
from django.shortcuts import render

from django_fantasia.settings import BASE_DIR
from fantasia.models import Post, GalleryImage, Message


def index(request):
    # return render(request, 'index.html', corona=False, corona_text="Achtung!\n Neue Coronamaßnahmen")
    banner = Message.objects.last()
    content = {
        'message': banner,
    }
    return render(request, 'fantasia/index.html', content)


def about_de(request):
    return render(request, 'fantasia/about/index.html')


def about_de_isabella(request):
    return render(request, 'fantasia/about/isabella.html')


def about_de_julia(request):
    return render(request, 'fantasia/about/julia.html')


def about_de_magdalena(request):
    return render(request, 'fantasia/about/magdalena.html')


def classical_de(request):
    return render(request, 'fantasia/classical.html')


def creative_de(request):
    return render(request, 'fantasia/creative.html')


def press_de(request):
    return render(request, 'fantasia/press.html')


def prices_de(request):
    return render(request, 'fantasia/prices.html')


def contact_de(request):
    return render(request, 'fantasia/contact.html')


def pictures_de(request):
    resize_all()
    new_pics = GalleryImage.objects.order_by('-pub_date')
    pics = {
        'pics': new_pics,
    }
    return render(request, 'fantasia/pictures.html', pics)


def news_de(request):
    news_list = Post.objects.order_by('-pub_date')
    context = {
        'posts': news_list,
    }
    return render(request, 'fantasia/news.html', context)


def offers_de(request):
    return render(request, 'fantasia/offers/index.html')


def offers_de_choreo(request):
    return render(request, 'fantasia/offers/choreography.html')


def offers_de_fitfun(request):
    return render(request, 'fantasia/offers/fitfun.html')


def offers_de_workout(request):
    return render(request, 'fantasia/offers/workout.html')


def offers_de_contemp(request):
    return render(request, 'fantasia/offers/contemp.html')


def index_en(request):
    banner = Message.objects.last()
    content = {
        'message': banner,
    }
    return render(request, 'fantasia/en/index.html', content)


def classical_en(request):
    return render(request, 'fantasia/en/classical.html')


def creative_en(request):
    return render(request, 'fantasia/en/creative.html')


def press_en(request):
    return render(request, 'fantasia/en/press.html')


def prices_en(request):
    return render(request, 'fantasia/en/prices.html')


def pictures_en(request):
    resize_all()
    new_pics = GalleryImage.objects.order_by('-pub_date')
    pics = {
        'pics': new_pics,
    }
    return render(request, 'fantasia/en/pictures.html', pics)


def news_en(request):
    return render(request, 'fantasia/en/news.html')


def about_en(request):
    return render(request, 'fantasia/en/about/index.html')


def about_en_isabella(request):
    return render(request, 'fantasia/en/about/isabella.html')


def about_en_julia(request):
    return render(request, 'fantasia/en/about/julia.html')


def about_en_magdalena(request):
    return render(request, 'fantasia/en/about/magdalena.html')


def offers_en(request):
    return render(request, 'fantasia/en/offers/index.html')


def offers_en_choreo(request):
    return render(request, 'fantasia/en/offers/choreo.html')


def offers_en_fitfun(request):
    return render(request, 'fantasia/en/offers/fitfun.html')


def offers_en_workout(request):
    return render(request, 'fantasia/en/offers/workout.html')


def offers_en_contemp(request):
    return render(request, 'fantasia/en/offers/contemp.html')


def contact_en(request):
    return render(request, 'fantasia/en/contact.html')


def resize(pic):
    img = Image.open(pic)
    (w, h) = img.size
    if w > 500:
        h = int(h * 500. / w)
        w = 500
        image = img.resize((w, h), Image.ANTIALIAS)
        image.save(pic)
        print("resized image")


def resize_all():
    for filepath in pathlib.Path('media/gallery').glob('**/*'):
        resize(filepath)

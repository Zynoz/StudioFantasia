import pathlib

from PIL import Image
from django.shortcuts import render, redirect

from .models import Post, GalleryImage, Message


def index(request):
    message = Message.objects.last()

    if message is not None:
        msg = {
            'msg': message,
        }
        print(msg)
    else:
        msg = None
        print('No content')
    return render(request, 'fantasia/index.html', msg)


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
    return render(request, 'fantasia/pictures2.html', pics)


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
    message = Message.objects.last()

    if message is not None:
        msg = {
            'msg': message,
        }
        print(msg)
    else:
        msg = None
        print('No content')
    return render(request, 'fantasia/en/index.html', msg)


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
    news_list = Post.objects.order_by('-pub_date')
    context = {
        'posts': news_list,
    }
    return render(request, 'fantasia/en/news.html', context)


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


def view_404(request, exception=None):
    return redirect('/')


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

# def get_backup(request):
#     path = settings.MEDIA_ROOT
#     shutil.make_archive('/home/ubuntu/studio/images', 'zip', settings.MEDIA_ROOT)
#     z = zipfile.ZipFile('/home/ubuntu/studio/images.zip', 'a', zipfile.ZIP_DEFLATED)
#     z.write('/home/ubuntu/studio/db.sqlite3')
#     return None
#     manage.py dumpdata > export.json
# https://stackoverflow.com/questions/9680562/python-how-to-append-to-file-in-zip-archive
# https://coderwall.com/p/mvsoyg/django-dumpdata-and-loaddata
# https://docs.djangoproject.com/en/3.1/topics/http/file-uploads/
# https://docs.djangoproject.com/en/3.1/ref/forms/api/#binding-uploaded-files
#
#
# def handle_uploaded_file(f):
#     with open(os.path.join(settings.MEDIA_ROOT, 'backup.zip', 'wb+')) as dest:
#         for chunk in f.chunks():
#             dest.write(chunk)
#         manage.py loaddata export.json
#
#
# def load_backup(request):
#     if request.method == 'POST':
#         form = UploadBackupForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             return HttpResponseRedirect('/admin')
#     else:
#         form = UploadBackupForm()
#     return render(request, 'fantasia/upload.html', {'form': form})

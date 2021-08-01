from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views
#from ..studio import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about_de, name='about'),
    path('about_isabella', views.about_de_isabella, name='about/isabella'),
    path('about_julia', views.about_de_julia, name='about/julia'),
    path('about_magdalena', views.about_de_magdalena, name='about/magdalena'),
    path('classical', views.classical_de, name='classical'),
    path('creative', views.creative_de, name='creative'),
    path('press', views.press_de, name='press'),
    path('prices', views.prices_de, name='prices'),
    path('contatct', views.contact_de, name='contact'),
    path('pictures', views.pictures_de, name='pictures'),
    path('news', views.news_de, name='news'),
    path('offers', views.offers_de, name='offers'),
    path('offers_choreo', views.offers_de_choreo, name='offers/choreo'),
    path('offers_fitfun', views.offers_de_fitfun, name='offers/fitfun'),
    path('offers_workout', views.offers_de_workout, name='offers/workout'),
    path('offers_contemp', views.offers_de_contemp, name='offers/contemp'),
    path('en', views.index_en, name='en/index'),
    path('en/classical', views.classical_en, name='en/classical'),
    path('en/creative', views.creative_en, name='en/creative'),
    path('en/press', views.press_en, name='en/press'),
    path('en/prices', views.prices_en, name='en/prices'),
    path('en/pictures', views.pictures_en, name='en/pictures'),
    path('en/news', views.news_en, name='en/news'),
    path('en/about', views.about_en, name='en/about'),
    path('en/about/isabella', views.about_en_isabella, name='en/about/isabella'),
    path('en/about/julia', views.about_en_julia, name='en/about/julia'),
    path('en/about/magdalena', views.about_en_magdalena, name='en/about/magdalena'),
    path('en/offers', views.offers_en, name='en/offers'),
    path('en/offers/choreo', views.offers_en_choreo, name='en/offers/choreo'),
    path('en/offers/fitfun', views.offers_en_fitfun, name='en/offers/fitfun'),
    path('en/offers/workout', views.offers_en_workout, name='en/offers/workout'),
    path('en/offers/contemp', views.offers_en_contemp, name='en/offers/contemp'),
    path('en/contact', views.contact_en, name='en/contact'),
    # path('backup', views.backup, name='backup'),
]

# if settings.DEBUG:
# urlpatterns += static('/media/', document_root='/opt/app/studio/media/')
# else:
# urlpatterns += staticfiles_urlpatterns()

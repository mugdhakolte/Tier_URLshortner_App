import random
import string

from django.views import View
from django.shortcuts import render, redirect
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from urlshortner.models import *


class ShortURL(View):

    def get(self, request):
        return render(request, template_name='index.html')

    def post(self, request):
        request_url = request.POST.get('url')
        # base_url = 'tier.app'
        base_url = '127.0.0.1:8000'
        random_string = ''.join(random.choices(string.ascii_uppercase +
                                               string.digits + string.ascii_lowercase,
                                               k=10))
        short_url = "http://{}/{}/".format(base_url, random_string)
        validate = URLValidator()
        request.session['random_str'] = random_string
        try:
            validate(short_url)
        except ValidationError as e:
            print(e)

        try:
            obj = TierURL.objects.get(short_url=short_url)
        except TierURL.DoesNotExist:
            obj = TierURL(main_url=request_url, short_url=short_url)
            obj.save()
        context = {
            'new_url': obj.short_url,
            'main_url': request_url,
            'random_string': random_string
        }
        return render(request, 'index.html', context)


class VisitURL(View):
    def get(self, request, url):
        # request_url = 'http://tier.app/{}/'.format(url)
        request_url = 'http://127.0.0.1:8000/{}/'.format(url)

        try:
            obj = TierURL.objects.get(short_url=request_url)
            try:
                visit_obj = URLVisit.objects.get(tier_url=obj)
                visit_obj.visits += 1
                visit_obj.save()
                return redirect(visit_obj.tier_url.main_url)

            except URLVisit.DoesNotExist:
                visit_obj = URLVisit(tier_url=obj, visits=1)
                visit_obj.save()
                return redirect(visit_obj.tier_url.main_url)
        except TierURL.DoesNotExist:
            return redirect('shorten_url')


class VisitedURLCount(View):
    def get(self, request):
        random_string = request.session.get('random_str')
        # base_url = 'tier.app'
        base_url = '127.0.0.1:8000'
        short_url = "http://{}/{}/".format(base_url, random_string)
        try:
            obj = TierURL.objects.get(short_url=short_url)
            try:
                visit_obj = URLVisit.objects.get(tier_url=obj)
                context = {
                    'visits': visit_obj.visits,
                    'short_url': visit_obj.tier_url.short_url
                }
                return render(request, 'visits.html', context)

            except URLVisit.DoesNotExist:
                context = {
                    'short_url': obj.short_url,
                    'no_visits': True
                }
                return render(request, 'visits.html', context)
        except TierURL.DoesNotExist:
            pass
        context = {}
        return render(request, 'visits.html', context)



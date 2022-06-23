from django.shortcuts import render
from django.http import HttpResponse
import re

# from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "form.html")

def _transform_link(orig_link):
    orig_link = orig_link.split("/")
    result_link = []
    found_date_already = False
    for idx, tok in enumerate(orig_link):
        if re.search("^\d\d\d\d-\d\d-\d\d$", tok) != None:
            found_date_already = True
            result_link.append("tmr")
        if not found_date_already:              
            if idx <= 2:
                result_link.append(tok)
        else:
            if not tok.startswith("."):
                result_link.append(tok)
    result_link = ("/").join(result_link)
    return result_link

def transform(request):
    orig_link = request.GET.get('origlink')
    result_link = _transform_link(orig_link)

    return render(request, "result.html", {"result_link": result_link})


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})


if __name__ == "__main__":
    _transform_link('https://www.haaretz.co.il/gallery/trip/2022-06-01/ty-article-magazine/.premium/00000181-1d7e-db47-a5dd-9d7f4d9f0000')
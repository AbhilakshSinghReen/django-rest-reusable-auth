from django.shortcuts import render


# Serve single-page React app
def index(request):
    return render(request, "index.html")

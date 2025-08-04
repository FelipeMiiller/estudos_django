from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def products_view(request):
    html = """
    <html>
    <head>
    <title>Products</title>
    </head>
    <body>
    <h1>Products</h1>
    <p>Lista de produtos</p>
    </body>
    </html>
    """
    return HttpResponse(html)
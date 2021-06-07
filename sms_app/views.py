from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Stock, Tag
from .forms import StockFormView, StockUpdateForm, StockSearchForm
from django.shortcuts import get_object_or_404
import csv
import datetime
from django.db.models import Q, Sum
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile

# Create your views here.


def get_stock(request, id):
    try:
        stock = Stock.objects.get(id=id)
    except Stock.DoesNotExist:
        return render(request, 'sms_app/404.html')
    context = {'get_stock': stock}
    return render(request, 'sms_app/get_stock.html', context)


def dashboard(request):
    return render(request, 'sms_app/dashboard.html')


def all_stock(request):
    form = StockSearchForm(request.POST or None)
    stock = Stock.objects.all()
    title = 'Inventory'
    content = 'This page represent all products stocked in our inventory'
    context = {'all_stock': stock, 'title': title, 'content': content, 'form': form}
    if request.method == 'POST':
        stock = Stock.objects.filter(name__icontains=form['name'].value(),
                                     quantity__icontains=form['quantity'].value())
        context = {'all_stock': stock, 'title': title, 'content': content, 'form': form}
        if form['export_to_csv'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=list of stock' + str(datetime.datetime.now()) + '.csv'
            writer = csv.writer(response)
            writer.writerow(['NAME', 'QUANTITY', 'QUANTITY RECEIVED', 'QUANTITY ISSUE'])
            instance = stock
            for st in instance:
                writer.writerow([st.name, st.quantity, st.receive_quantity, st.issue_quantity])
            return response
    return render(request, 'sms_app/all_stock.html', context)


# def export_csv(request):
#     # stock = Stock.objects.all()
#     form = StockSearchForm(request.POST)
#     if request.method == 'POST':
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename=list of stock' + str(datetime.datetime.now()) + '.csv'
#         writer = csv.writer(response)
#         writer.writerow(['NAME', 'QUANTITY', 'QUANTITY RECEIVED', 'QUANTITY ISSUE'])
#         stock = Stock.objects.filter(name__icontains=form['name'].value())
#         instance = stock
#         for stock in instance:
#             writer.writerow([stock.name, stock.quantity, stock.receive_quantity, stock.issue_quantity])
#             return response
#
#     return render(request, 'sms_app/all_stock.html')


def export_pdf(request):
    stock = Stock.objects.all()
    sum = stock.count()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=stock pdf' + str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    html_string = render_to_string('sms_app/pdf-output.html', {'stock': stock, 'total': 0})
    html = HTML(string=html_string)
    result = html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response


def name_tag(request):
    tag = Tag.objects.all()
    return render(request, 'sms_app/all_stock.html', {'tags': tag})


def add_stock(request):
    form = StockFormView(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('/stocks')
    else:
        form = StockFormView(request.POST, request.FILES)
    title = 'Add Item'
    content = "Let's Add an item to your inventory"
    context = {'form': form, 'title': title, 'content': content}
    return render(request, 'sms_app/add_stock.html', context)


def update_stock(request, id):
    query = Stock.objects.get(id=id)
    form = StockUpdateForm(instance=query)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=query)
        if form.is_valid():
            form.save()
            return redirect('/stocks')

    context = {'form': form}
    return render(request, 'sms_app/add_stock.html', context)


def delete_stock(request, id):
    query = Stock.objects.get(id=id)
    if request.method == 'POST':
        query.delete()
        return redirect('/stocks')
    return render(request, 'sms_app/delete_stock.html')

# def error_404(request, exception):
#     print('no')
#     return render(request, 'sms_app/404.html')

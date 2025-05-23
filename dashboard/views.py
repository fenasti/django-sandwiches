from django.shortcuts import render
from .forms import SalesDataForm
from . import google_sheets
from django.contrib import messages

def home(request):
    result = None
    error = None
    headers = ["cheese ham", "tom moz", "chicken salad", "egg salad", "hummus veg", "ham egg"]

    if request.method == 'POST':
        form = SalesDataForm(request.POST)
        if form.is_valid():
            raw_data = form.cleaned_data['sales_data']
            data_list = raw_data.split(',')

            if google_sheets.validate_data(data_list):
                sales_data = [int(num) for num in data_list]
                google_sheets.update_worksheet(sales_data, "sales")

                surplus_data = google_sheets.calculate_surplus_data(sales_data)
                google_sheets.update_worksheet(surplus_data, "surplus")

                last_5_sales = google_sheets.get_last_5_entries_sales()
                stock_data = google_sheets.calculate_stock_data(last_5_sales)
                google_sheets.update_worksheet(stock_data, "stock")

                messages.success(request, "Data submitted successfully!")

                result = {
                    "sales_data": zip(headers, sales_data),
                    "surplus_data": zip(headers, surplus_data),
                    "stock_data": zip(headers, stock_data),
                }
            else:
                messages.error(request, "Invalid data. Please enter 6 comma-separated numbers.")
    else:
        form = SalesDataForm()

    return render(request, 'dashboard/dashboard.html', {
        'form': form,
        'result': result,
        'error': error
    })

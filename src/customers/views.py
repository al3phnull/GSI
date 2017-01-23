# -*- coding: utf-8 -*-
"""Views for the customers app."""
import os
import subprocess
from PIL import Image
from subprocess import check_call, Popen, PIPE
from osgeo import osr, gdal
# import Image, ImageDraw
# from osgeo import gdal
# import gdal

from django.shortcuts import render
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from customers.models import Category, ShelfData, DataSet, CustomerAccess
from customers.customers_forms import CategoryForm, ShelfDataForm, DataSetForm, CustomerAccessForm
from customers.customers_update_create import (category_update_create, shelf_data_update_create,
                                                data_set_update_create, customer_access_update_create)
from core.get_post import get_post
from core.paginations import paginations
from gsi.settings import (RESULTS_DIRECTORY, GOOGLE_MAP_ZOOM, POLYGONS_DIRECTORY,
                        DAFAULT_LAT, DAFAULT_LON, PNG_PATH, BASE_DIR, TIF_PATH)


# categorys list
@user_passes_test(lambda u: u.is_superuser)
@render_to('customers/categorys_list.html')
def categorys(request):
    """**View all categories for the Shelf Data.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
    """

    title = 'The categorys for the Shelf Data'
    url_name = 'categorys'
    but_name = 'info_panel'

    categorys = Category.objects.all()
    category_name = ''

    # Sorted by
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('name', ):
            categorys = categorys.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                categorys = categorys.reverse()

    # Ajax when deleting objects
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'run_id[]' in data_post:
            data = ''
            message = u'Are you sure you want to remove these objects:'
            run_id = data_post.getlist('run_id[]')

            for r in run_id:
                cur_run = get_object_or_404(Category, pk=int(r))
                data += '"' + cur_run.name + '", '

            data = data[:-2]
            data = '<b>' + data + '</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)

        if 'cur_run_id' in data_post:
            message = u'Are you sure you want to remove this objects:'
            run_id = data_post['cur_run_id']
            cur_run = get_object_or_404(Category, pk=int(run_id))
            data = '<b>"' + cur_run.name + '"</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        if request.POST.get('category_select'):
            for category_id in request.POST.getlist('category_select'):
                cur_category = get_object_or_404(Category, pk=category_id)
                category_name += '"' + cur_category.name + '", '
                cur_category.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('categorys_list'),
                (u'Categorys: {0} deleted.'.format(category_name))))
        elif request.POST.get('delete_button'):
            cur_category = get_object_or_404(Category, pk=request.POST.get('delete_button'))
            category_name += '"' + cur_category.name + '", '
            cur_category.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('categorys_list'), (u'Categorys: {0} deleted.'.format(category_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('categorys_list'), (u"To delete, select Category or more Categorys.")))

    # paginations
    model_name = paginations(request, categorys)

    data = {
        'title': title,
        'categorys': model_name,
        'model_name': model_name,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# category add
@login_required
@render_to('gsi/static_data_item_edit.html')
def category_add(request):
    """**View for the "Category Add" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Category Add'
    url_form = 'category_add'
    template_name = 'customers/_category_form.html'
    reverse_url = {
        'save_button': 'categorys',
        'save_and_another': 'category_add',
        'save_and_continue': 'category_edit',
        'cancel_button': 'categorys'
    }
    func = category_update_create
    form = None
    url_name = 'categorys'
    but_name = 'info_panel'

    # Handling POST request
    if request.method == "POST":
        response = get_post(request, CategoryForm, 'Category', reverse_url, func)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = CategoryForm()

    data = {
        'title': title,
        'url_form': url_form,
        'template_name': template_name,
        'form': form,
        'available_tiles': available_tiles,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# category edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def category_edit(request, category_id):
    """**View for the "Category "<name>" Edit" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
        * *category_id:* The Category object ID
    """

    category = get_object_or_404(Category, pk=category_id)
    title = 'Category Edit "%s"' % (category.name)
    url_form = 'category_edit'
    template_name = 'customers/_category_form.html'
    reverse_url = {
        'save_button': 'categorys',
        'save_and_another': 'category_add',
        'save_and_continue': 'category_edit',
        'cancel_button': 'categorys'
    }
    func = category_update_create
    form = None
    url_name = 'categorys'
    but_name = 'info_panel'

    # Handling POST request
    if request.method == "POST":
        response = get_post(
            request,
            CategoryForm,
            'Category',
            reverse_url,
            func,
            item_id=category_id)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = CategoryForm(instance=category)

    data = {
        'title': title,
        'url_form': url_form,
        'url_name': url_name,
        'but_name': but_name,
        'template_name': template_name,
        'form': form,
        'item_id': category_id,
    }

    return data


# shelf data list
@user_passes_test(lambda u: u.is_superuser)
@render_to('customers/shelf_data_list.html')
def shelf_data(request):
    """**View all Shelf Data.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
    """

    title = 'The Shelf Data'
    url_name = 'shelf_data'
    but_name = 'info_panel'

    shelf_data = ShelfData.objects.all()
    shelf_data_name = ''

    # Sorted
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('category', 'attribute_name', 'root_filename', 'units',):
            shelf_data = shelf_data.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                shelf_data = shelf_data.reverse()

    # Ajax when deleting objects
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'run_id[]' in data_post:
            data = ''
            message = u'Are you sure you want to remove these objects:'
            run_id = data_post.getlist('run_id[]')

            for r in run_id:
                cur_run = get_object_or_404(ShelfData, pk=int(r))
                data += '"' + str(cur_run) + '", '

            data = data[:-2]
            data = '<b>' + data + '</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)

        if 'cur_run_id' in data_post:
            message = u'Are you sure you want to remove this objects:'
            run_id = data_post['cur_run_id']
            cur_run = get_object_or_404(ShelfData, pk=int(run_id))
            data = '<b>"' + str(cur_run) + '"</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        if request.POST.get('shelf_data_select'):
            for shelf_data_id in request.POST.getlist('shelf_data_select'):
                cur_shelf_data = get_object_or_404(ShelfData, pk=shelf_data_id)
                shelf_data_name += '"' + cur_shelf_data.attribute_name + '", '
                cur_shelf_data.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('shelf_data_list'),
                (u'Shelf Data: {0} deleted.'.format(shelf_data_name))))
        elif request.POST.get('delete_button'):
            cur_shelf_data = get_object_or_404(ShelfData, pk=request.POST.get('delete_button'))
            shelf_data_name += '"' + cur_shelf_data.attribute_name + '", '
            cur_shelf_data.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('shelf_data_list'), (u'Shelf Data: {0} deleted.'.format(shelf_data_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('shelf_data_list'), (u"To delete, select Shelf Data or more Shelf Data.")))

    # paginations
    model_name = paginations(request, shelf_data)

    data = {
        'title': title,
        'shelf_data': model_name,
        'model_name': model_name,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# shelf data add
@login_required
@render_to('gsi/static_data_item_edit.html')
def shelf_data_add(request):
    """**View for the "ShelfData Add" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Shelf Data Add'
    url_form = 'shelf_data_add'
    template_name = 'customers/_shelf_data_form.html'
    reverse_url = {
        'save_button': 'shelf_data',
        'save_and_another': 'shelf_data_add',
        'save_and_continue': 'shelf_data_edit',
        'cancel_button': 'shelf_data'
    }
    func = shelf_data_update_create
    form = None
    url_name = 'shelf_data'
    but_name = 'info_panel'
    available_tiles = ShelfData.objects.all()

    # Handling POST request
    if request.method == "POST":
        response = get_post(request, ShelfDataForm, 'Shelf Data', reverse_url, func)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = ShelfDataForm()

    data = {
        'title': title,
        'url_form': url_form,
        'template_name': template_name,
        'form': form,
        'available_tiles': available_tiles,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# shelf data edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def shelf_data_edit(request, shelf_data_id):
    """**View for the "ShelfData "<attribute_name>" Edit" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
        * *shelf_data_id:* The ShelfData object ID
    """

    shelf_data = get_object_or_404(ShelfData, pk=shelf_data_id)
    title = 'Category Edit "%s"' % (shelf_data.attribute_name)
    url_form = 'shelf_data_edit'
    template_name = 'customers/_shelf_data_form.html'
    reverse_url = {
        'save_button': 'shelf_data',
        'save_and_another': 'shelf_data_add',
        'save_and_continue': 'shelf_data_edit',
        'cancel_button': 'shelf_data'
    }
    func = shelf_data_update_create
    form = None
    url_name = 'shelf_data'
    but_name = 'info_panel'

    # Handling POST request
    if request.method == "POST":
        response = get_post(
            request,
            ShelfDataForm,
            'Shelf Data',
            reverse_url,
            func,
            item_id=shelf_data_id)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = ShelfDataForm(instance=shelf_data)

    data = {
        'title': title,
        'url_form': url_form,
        'url_name': url_name,
        'but_name': but_name,
        'template_name': template_name,
        'form': form,
        'item_id': shelf_data_id,
    }

    return data


# data sets list
@user_passes_test(lambda u: u.is_superuser)
@render_to('customers/dataset_list.html')
def data_sets(request):
    """**View all the DataSets.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
    """

    title = 'DataSets Definition'
    url_name = 'data_sets'
    but_name = 'info_panel'

    data_sets = DataSet.objects.all()
    data_set_name = ''

    # Sorted by name
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('name', 'description', 'results_directory', 'shelf_data__attribute_name', 'shelf_data__root_filename'):
            data_sets = data_sets.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                data_sets = data_sets.reverse()

    # Ajax when deleting objects
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'run_id[]' in data_post:
            data = ''
            message = u'Are you sure you want to remove these objects:'
            run_id = data_post.getlist('run_id[]')

            for r in run_id:
                cur_run = get_object_or_404(DataSet, pk=int(r))
                data += '"' + cur_run.name + '", '

            data = data[:-2]
            data = '<b>' + data + '</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)

        if 'cur_run_id' in data_post:
            message = u'Are you sure you want to remove this objects:'
            run_id = data_post['cur_run_id']
            cur_run = get_object_or_404(DataSet, pk=int(run_id))
            data = '<b>"' + cur_run.name + '"</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        if request.POST.get('dataset_select'):
            for data_set_id in request.POST.getlist('dataset_select'):
                cur_data_set = get_object_or_404(DataSet, pk=data_set_id)
                data_set_name += '"' + cur_data_set.name + '", '
                cur_data_set.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('data_sets'),
                (u'DataSets: {0} deleted.'.format(data_set_name))))
        elif request.POST.get('delete_button'):
            cur_data_set = get_object_or_404(DataSet, pk=request.POST.get('delete_button'))
            data_set_name += '"' + cur_data_set.name + '", '
            cur_data_set.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('data_sets'), (u'DataSets: {0} deleted.'.format(data_set_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('data_sets'), (u"To delete, select DataSet or more DataSets.")))

    # paginations
    model_name = paginations(request, data_sets)

    data = {
        'title': title,
        'data_sets': model_name,
        'model_name': model_name,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# shelf data add
@login_required
@render_to('gsi/static_data_item_edit.html')
def data_set_add(request):
    """**View for the "DataSet Add" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'DataSet Add'
    url_form = 'data_set_add'
    template_name = 'customers/_data_set_form.html'
    reverse_url = {
        'save_button': 'data_sets',
        'save_and_another': 'data_set_add',
        'save_and_continue': 'data_set_edit',
        'cancel_button': 'data_sets'
    }
    func = data_set_update_create
    form = None
    shelf_data = ShelfData.objects.all()
    url_name = 'data_sets'
    but_name = 'info_panel'
    dirs_list = []

    # Ajax when insert the root_filename and the attribute_name
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'shelf_data_id' in data_post:
            shelf_data_id = data_post['shelf_data_id']
            shelf_data = get_object_or_404(ShelfData, pk=int(shelf_data_id))
            root_filename = shelf_data.root_filename
            attribute_name = shelf_data.attribute_name
            data = root_filename + '$$$' + attribute_name

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)


    # Handling POST request
    if request.method == "POST":
        if request.POST.get('update_button') is not None:
            form = DataSetForm(request.POST)

            if form.is_valid():
                if form.cleaned_data['results_directory']:
                    try:
                        results_directory = RESULTS_DIRECTORY + form.cleaned_data['results_directory']
                        root, dirs, files = os.walk(results_directory).next()

                        for sd in shelf_data:
                            if str(sd.root_filename) in dirs:
                                dirs_list.append(sd)
                    except StopIteration:
                        return HttpResponseRedirect(
                            u'%s?danger_message=%s' % (reverse('data_set_add'),
                            (u'The directory "{0}" does not exist!'.format(results_directory)))
                        )
        else:
            response = get_post(request, DataSetForm, 'DataSet', reverse_url, func)

            if isinstance(response, HttpResponseRedirect):
                return response
            else:
                form = response
    else:
        form = DataSetForm()

    data = {
        'title': title,
        'url_form': url_form,
        'template_name': template_name,
        'form': form,
        'url_name': url_name,
        'but_name': but_name,
        'dirs_list': dirs_list,
    }

    return data


# shelf data edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def data_set_edit(request, data_set_id):
    """**View for the "DataSets "<name>" Edit" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
        * *data_set_id:* The ShelfData object ID
    """

    data_set = get_object_or_404(DataSet, pk=data_set_id)
    title = 'DataSet Edit "%s"' % (data_set.name)
    url_form = 'data_set_edit'
    template_name = 'customers/_data_set_form.html'
    reverse_url = {
        'save_button': 'data_sets',
        'save_and_another': 'data_set_add',
        'save_and_continue': 'data_set_edit',
        'cancel_button': 'data_sets'
    }
    func = data_set_update_create
    form = None
    shelf_data = ShelfData.objects.all()
    url_name = 'data_sets'
    but_name = 'info_panel'
    dirs_list = []

    # Get the results_directorys list
    try:
        results_directory = RESULTS_DIRECTORY + data_set.results_directory
        root, dirs, files = os.walk(results_directory).next()

        for sd in shelf_data:
            if str(sd.root_filename) in dirs:
                dirs_list.append(sd)
    except Exception:
        pass

    # Ajax when insert the root_filename and the attribute_name
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'shelf_data_id' in data_post:
            shelf_data_id = data_post['shelf_data_id']
            shelf_data = get_object_or_404(ShelfData, pk=int(shelf_data_id))
            root_filename = shelf_data.root_filename
            attribute_name = shelf_data.attribute_name
            data = root_filename + '$$$' + attribute_name

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        # Update the results_directorys list
        if request.POST.get('update_button') is not None:
            form = DataSetForm(request.POST)
            dirs_list = []

            if form.is_valid():
                if form.cleaned_data['results_directory']:
                    results_directory = RESULTS_DIRECTORY + form.cleaned_data['results_directory']

                    try:
                        root, dirs, files = os.walk(results_directory).next()

                        for sd in shelf_data:
                            if str(sd.root_filename) in dirs:
                                dirs_list.append(sd)
                    except StopIteration:
                        return HttpResponseRedirect(
                            u'%s?danger_message=%s' % (reverse('data_set_edit', args=[data_set_id]),
                            (u'The directory "{0}" does not exist!'.format(results_directory)))
                        )
        else:
            response = get_post(request, DataSetForm, 'DataSet', reverse_url, func, item_id=data_set_id)

            if isinstance(response, HttpResponseRedirect):
                return response
            else:
                form = response
    else:
        form = DataSetForm(instance=data_set)

    data = {
        'title': title,
        'url_form': url_form,
        'url_name': url_name,
        'but_name': but_name,
        'template_name': template_name,
        'form': form,
        'item_id': data_set_id,
        'data_set': data_set,
        'dirs_list': dirs_list,
    }

    return data


# customers access list
@user_passes_test(lambda u: u.is_superuser)
@render_to('customers/customer_access_list.html')
def customer_access(request):
    """**View the Customer Access.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
    """

    title = 'Customer Access'
    url_name = 'customer_access'
    but_name = 'info_panel'

    customers_access = CustomerAccess.objects.all()
    customer_access_name = ''

    # Sorted by customer name
    if request.method == "GET":
        order_by = request.GET.get('order_by', '')

        if order_by in ('user', ):
            customers_access = customers_access.order_by(order_by)

            if request.GET.get('reverse', '') == '1':
                customers_access = customers_access.reverse()

    # Ajax when deleting objects
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        if 'run_id[]' in data_post:
            data = ''
            message = u'Are you sure you want to remove these objects:'
            run_id = data_post.getlist('run_id[]')

            for r in run_id:
                cur_run = get_object_or_404(CustomerAccess, pk=int(r))
                data += '"{0}", '.format(cur_run)

            data = data[:-2]
            data = '<b>' + data + '</b>'
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)

        if 'cur_run_id' in data_post:
            message = u'Are you sure you want to remove this objects:'
            run_id = data_post['cur_run_id']
            cur_run = get_object_or_404(CustomerAccess, pk=int(run_id))
            data = '<b>"{0}"</b>'.format(cur_run)
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)
        else:
            data = ''
            return HttpResponse(data)

    # Handling POST request
    if request.method == "POST":
        if request.POST.get('customer_access_select'):
            for customer_access_id in request.POST.getlist('customer_access_select'):
                cur_customer_access = get_object_or_404(CustomerAccess, pk=customer_access_id)
                customer_access_name += '"{0}", '.format(cur_customer_access)
                cur_customer_access.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('customer_access'),
                (u'Customers Access: {0} deleted.'.format(customer_access_name))))
        elif request.POST.get('delete_button'):
            cur_customer_access = get_object_or_404(CustomerAccess, pk=request.POST.get('delete_button'))
            customer_access_name += '"{0}", '.format(cur_customer_access)
            cur_customer_access.delete()

            return HttpResponseRedirect(u'%s?status_message=%s' % (
                reverse('customer_access'), (u'Customers Access: {0} deleted.'.format(customer_access_name))))
        else:
            return HttpResponseRedirect(u'%s?warning_message=%s' % (
                reverse('customer_access'), (u"To delete, select Customer Access or more Customers Access.")))

    # paginations
    model_name = paginations(request, customers_access)

    data = {
        'title': title,
        'customers_access': model_name,
        'model_name': model_name,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# customer access add
@login_required
@render_to('gsi/static_data_item_edit.html')
def customer_access_add(request):
    """**View for the "Customer Access Add" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page

    """

    title = 'Customer Access Add'
    url_form = 'customer_access_add'
    template_name = 'customers/_customer_access_form.html'
    reverse_url = {
        'save_button': 'customer_access',
        'save_and_another': 'customer_access_add',
        'save_and_continue': 'customer_access_edit',
        'cancel_button': 'customer_access'
    }
    func = customer_access_update_create
    form = None
    url_name = 'customer_access'
    but_name = 'info_panel'
    available_data_set = DataSet.objects.all()

    # Handling POST request
    if request.method == "POST":
        response = get_post(request, CustomerAccessForm, 'Customer Access', reverse_url, func)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = CustomerAccessForm()

    data = {
        'title': title,
        'url_form': url_form,
        'template_name': template_name,
        'form': form,
        'available_data_set': available_data_set,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


# customer access edit
@login_required
@render_to('gsi/static_data_item_edit.html')
def customer_access_edit(request, customer_access_id):
    """**View for the "Customer Access "<name>" Edit" page.**

    :Arguments:
        * *request:* The request is sent to the server when processing the page
        * *customer_access_id:* The CustomerAccess object ID
    """

    customer_access = get_object_or_404(CustomerAccess, pk=customer_access_id)
    title = 'Customer Access Edit "%s"' % (customer_access)
    url_form = 'customer_access_edit'
    template_name = 'customers/_customer_access_form.html'
    reverse_url = {
        'save_button': 'customer_access',
        'save_and_another': 'customer_access_add',
        'save_and_continue': 'customer_access_edit',
        'cancel_button': 'customer_access'
    }
    func = customer_access_update_create
    form = None
    url_name = 'customer_access'
    but_name = 'info_panel'
    chosen_data_set = customer_access.data_set.all()
    available_data_set = DataSet.objects.exclude(id__in=customer_access.data_set.values_list('id', flat=True))

    # Handling POST request
    if request.method == "POST":
        response = get_post(
            request, CustomerAccessForm, 'Customer Access', reverse_url, func, item_id=customer_access_id)

        if isinstance(response, HttpResponseRedirect):
            return response
        else:
            form = response
    else:
        form = CustomerAccessForm(instance=customer_access)

    data = {
        'title': title,
        'url_form': url_form,
        'template_name': template_name,
        'form': form,
        'item_id': customer_access_id,
        'available_data_set': available_data_set,
        'chosen_data_set': chosen_data_set,
        'url_name': url_name,
        'but_name': but_name,
    }

    return data


def get_file_filepath(f, ext, path):
    farea = '{0}.{1}'.format(f, ext)
    fpath = os.path.join(path, farea)

    return fpath


# view Customer Section
@login_required
@render_to('customers/customer_section.html')
def customer_section(request, user_id):
    """**View for the "Customer '<user>' section" page.**

    :Functions:
        When you load the page is loaded map with Google MAP. Initial coordinates: eLat = 0, eLng = 0.
        Zoom map is variable GOOGLE_MAP_ZOOM, whose value is in the project settings.
        Code view allows to change position when you enter values in the fields on the page "Enter Lat" and "Enter Log".

    :Arguments:
        * *request:* The request is sent to the server when processing the page
        * *user_id:* The User ID
    """

    scheme = '{0}://'.format(request.scheme)
    absolute_png_url = os.path.join(scheme, request.get_host(), PNG_PATH)
    absolute_path_png = os.path.join(BASE_DIR, PNG_PATH)
    absolute_tif_folder = os.path.join(BASE_DIR, TIF_PATH)

    select_area = ''

    absolute_url_png_file = ''
    absolute_path_tif_file = ''

    png_file = ''
    tif_file = ''

    customer = get_object_or_404(User, pk=user_id)
    customer_access = get_object_or_404(CustomerAccess, user=customer)
    shelf_data = ShelfData.objects.all()
    data_set = None
    statistics = None
    title = 'Customer {0} section'.format(customer)
    url_name = 'customer_section'
    data_set_id = 0
    data_sets = {}
    dirs_list = []
    polygons_list = []
    fpng_list = []
    data_sets_current = CustomerAccess.data_set.through.objects.filter(
        customeraccess_id=customer_access.id).order_by('dataset_id')

    # default GEOTIFF coordinates
    cLng = 0
    cLat = 0
    eLat_1 = 0
    eLng_1 = 0
    eLat_2 = 0
    eLng_2 = 0

    # delete the 'select_data_set' session
    # del request.session['select_data_set']

    # get the list files for the show on the custom section
    try:
        root, dirs, files = os.walk(absolute_path_png).next()

        for f in files:
            fpng_list.append(f.split('.png')[0])
    except Exception, e:
        return HttpResponseRedirect(
            u'%s?danger_message=%s' % (reverse('data_set_edit', args=[data_set_id]),
            (u'The directory "{0}" does not exist!'.format(absolute_path_png)))
        )


    # fpng = '{0}.png'.format(fpng_list[0])
    # ftif = '{0}.tif'.format(fpng_list[0])
    # absolute_uri_png_file = os.path.join(absolute_uri_png_folder, fpng)
    # absolute_uri_tif_file = os.path.join(absolute_uri_png_folder, ftif)


    # print 'absolute_url_png_file =========================== ', absolute_url_png_file
    # print '00 absolute_tif_folder =========================== ', absolute_tif_folder
    #
    # print '00-1 request.session[png] =========================== ', request.session.get('png', False)
    # print '00-2 request.session[png] =========================== ', request.session.get('png', True)

    # get the list polygons for the show on the custom section
    try:
        root, dirs, files = os.walk(POLYGONS_DIRECTORY).next()

        for f in files:
            polygons_list.append(f.split('.kml')[0])
    except Exception, e:
        return HttpResponseRedirect(
            u'%s?danger_message=%s' % (reverse('data_set_edit', args=[data_set_id]),
            (u'The directory "{0}" does not exist!'.format(POLYGONS_DIRECTORY)))
        )

    if request.session.get('select_data_set', False):
        data_set_id = request.session['select_data_set']
        data_set = get_object_or_404(DataSet, pk=data_set_id)
        data_set_id = int(data_set_id)

        # Get the results_directorys list
        try:
            results_directory = RESULTS_DIRECTORY + data_set.results_directory
            root, dirs, files = os.walk(results_directory).next()

            for sd in shelf_data:
                if str(sd.root_filename) in dirs:
                    dirs_list.append(sd)
        except Exception, e:
            return HttpResponseRedirect(
                u'%s?danger_message=%s' % (reverse('data_set_edit', args=[data_set_id]),
                (u'The directory "{0}" does not exist!'.format(results_directory)))
            )
    else:
        request.session['select_data_set'] = data_sets_current[0].dataset_id
        request.session.set_expiry(172800)

    if request.session.get('eLat', False):
        eLat = request.session['eLat']
    else:
        eLng = DAFAULT_LAT
        request.session.set_expiry(172800)

    if request.session.get('eLng', False):
        eLng = request.session['eLng']
    else:
        eLng = DAFAULT_LON
        request.session.set_expiry(172800)

    if request.session.get('png', False):
        absolute_url_png_file = get_file_filepath(request.session['png'], 'png', absolute_png_url)
        absolute_path_tif_file = get_file_filepath(request.session['png'], 'tif', absolute_tif_folder)
        select_area = request.session['png']
    else:
        if fpng_list[0]:
            # path to a GeoTIFF files
            absolute_url_png_file = get_file_filepath(fpng_list[0], 'png', absolute_png_url)
            absolute_path_tif_file = get_file_filepath(fpng_list[0], 'tif', absolute_tif_folder)
            request.session['png'] = fpng_list[0]
            select_area = fpng_list[0]
            request.session.set_expiry(172800)

    for n in data_sets_current:
        ds = get_object_or_404(DataSet, pk=n.dataset_id)
        data_sets[ds] = n.dataset_id

    # Ajax when deleting objects
    if request.method == "POST" and request.is_ajax():
        data_post = request.POST

        # print 'data_post ========================== ', data_post

        if 'datasets_id' in data_post:
            data_set_id = data_post.get('datasets_id', '')

            if data_set_id:
                request.session['select_data_set'] = data_set_id
            status = 'success'

            return HttpResponse(status)

        if 'multiple' in data_post:
            message = u'Are you sure you want to remove this objects:'
            run_id = data_post['cur_run_id']
            cur_run = get_object_or_404(CustomerAccess, pk=int(run_id))
            data = '<b>"{0}"</b>'.format(cur_run)
            data = '{0} {1}?'.format(message, data)

            return HttpResponse(data)

        if 'area_name' in data_post:
            area_name = data_post.get('area_name', '')
            request.session['png'] = area_name

            # print '3 request.session[png] =========================== ', request.session['png']

            # print 'area_name ========================= ', area_name
            # print 'request.session png ========================= ', request.session['png']
            #
            # # path to a GeoTIFF files
            # absolute_url_png_file = get_file_filepath(area_name, 'png', absolute_png_url)
            # absolute_path_tif_file = get_file_filepath(area_name, 'tif', absolute_tif_folder)

            status = 'success'


            # print 'absolute_url_png_file =========================== ', absolute_url_png_file
            # print 'absolute_path_tif_file =========================== ', absolute_path_tif_file

            return HttpResponse(status)

    # Handling POST request
    # if request.method == "POST":
    #     data_post = request.POST
    #
    #     data_set_id = data_post.get('datasets_id', '')
    #
    #     if data_post.get('eLat', ''):
    #         eLat = data_post.get('eLat', '')
    #
    #     if data_post.get('eLng', ''):
    #         eLng = data_post.get('eLng', '')


    # path to a GeoTIFF files
    # file_tif = '/home/greg/Elance_com/KeyUA/GSI/UI/images/BA_10_aws_v3.Site1.tif'
    # file_png = '/home/greg/Elance_com/KeyUA/GSI/UI/images/BA_10_aws_v3.Site1.png'

    # Convert tif to png
    # # **** 1
    # check_call(('cat {0} | convert - {1}').format(file_tif, file_png), shell=True)
    #
    # # ***** 2
    # proc = Popen(['cat', file_tif], stdout=PIPE)
    #
    # p2 = Popen(['convert', '-', file_png],stdin=proc.stdout)
    #
    # out,err = proc.communicate()

    # get the lat/lon values for a GeoTIFF files
    # ulx, uly is the upper left corner, lrx, lry is the lower right corner
    # src = gdal.Open(file_tif)
    # ulx, xres, xskew, uly, yskew, yres = src.GetGeoTransform()
    # lrx = ulx + (src.RasterXSize * xres)
    # lry = uly + (src.RasterYSize * yres)
    #
    # print 'lrx ======================== ', lrx
    # print 'lry ======================== ', lry

    # media/png/

    # print '!! absolute_path_tif_file  =========================== \n', absolute_path_tif_file

    # get the lat/lon values for a GeoTIFF files
    try:
        ds = gdal.Open(absolute_path_tif_file)
        width = ds.RasterXSize
        height = ds.RasterYSize
        gt = ds.GetGeoTransform()
        minx = gt[0]
        miny = gt[3] + width*gt[4] + height*gt[5]
        maxx = gt[0] + width*gt[1] + height*gt[2]
        maxy = gt[3]
        centery = (maxy + miny) / 2
        centerx = (maxx + minx) / 2

        cLng = centerx
        cLat = centery
        eLat_1 = miny
        eLng_1 = minx
        eLat_2 = maxy
        eLng_2 = maxx

        # print 'width ======================== ', width
        # print 'height ======================== ', height
        # print '--------------------------------------------------------------------'
        # print 'centerx ======================== ', centerx
        # print 'centery ======================== ', centery
        # print '--------------------------------------------------------------------'
        # print 'minx ======================== ', minx
        # print 'miny ======================== ', miny
        # print 'maxx ======================== ', maxx
        # print 'maxy ======================== ', maxy
    except AttributeError:
        pass





    # imagefile = file_tif
    # proc_res = subprocess.Popen(["gdalinfo", "%s"%imagefile], stdout=subprocess.PIPE)
    # out, err = proc_res.communicate()
    # ul = out[out.find("Upper Left")+14:out.find("Upper Left")+38]
    # lr = out[out.find("Lower Right")+14:out.find("Lower Right")+38]
    # center = out[out.find("Center")+14:out.find("Center")+38]
    #
    #
    # # eLng, eLat = center.split(', ')
    # center.replace(' ', '')
    # ul.replace(' ', '')
    # lr.replace(' ', '')
    #
    # print 'OUT 2 ============================================== ', out
    # print 'Center 2 ============================================== ', center
    # print 'ul ============================================== ', ul
    # print 'lr ============================================== ', lr
    #
    # cLng, cLat = center.split(',')
    # eLng_1, eLat_1 = ul.split(',')
    # eLng_2, eLat_2 = lr.split(',')
    #
    # print '--------------------------------------------------------------------'
    # print 'eLat_1 ============================================== ', eLat_1
    # print '--------------------------------------------------------------------'
    # print 'eLat_2 ============================================== ', eLat_2
    #
    # eLat_1_conv = float(eLat_1) + float(eLat_1) - float(eLat_2)
    # eLat_2_conv = float(eLat_2) + float(eLat_1) - float(eLat_2)
    #
    # print '--------------------------------------------------------------------'
    # print 'cLng ============================================== ', cLng
    # print 'cLat ============================================== ', cLat
    # print '--------------------------------------------------------------------'
    # print 'eLng_1 ============================================== ', eLng_1
    # print 'eLat_1 ============================================== ', eLat_1
    # print 'eLat_1_conv ============================================== ', eLat_1_conv
    # print '--------------------------------------------------------------------'
    # print 'eLng_2 ============================================== ', eLng_2
    # print 'eLat_2 ============================================== ', eLat_2
    # print 'eLat_2_conv ============================================== ', eLat_2_conv

    # print '!! absolute_url_png_file =========================== ', absolute_url_png_file
    # print '!! select_area ========================= ', select_area

    data = {
        'title': title,
        'user_id': user_id,
        'customer': customer,
        'data_sets': data_sets,
        'url_name': url_name,
        'data_set_id': data_set_id,
        'data_set': data_set,
        'dirs_list': dirs_list,
        'polygons_list': polygons_list,
        'fpng_list': fpng_list,
        'select_area': select_area,

        'absolute_url_png_file': absolute_url_png_file,

        'cLng': cLng,
        'cLat': cLat,
        'eLat_1': eLat_1,
        'eLng_1': eLng_1,
        'eLat_2': eLat_2,
        'eLng_2': eLng_2,
        'GOOGLE_MAP_ZOOM': GOOGLE_MAP_ZOOM,
    }

    return data
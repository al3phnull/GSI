# -*- coding: utf-8 -*-
"""Customers app urls.py"""

from django.conf.urls import include, url


urlpatterns = [
    # the url for the categorys list
	url(r'^category/show$', 'customers.views.categorys', name='categorys'),
	# the url for the category add
	url(r'^category/add$', 'customers.views.category_add', name='category_add'),
	# the url for the category edit
	url(r'^category/(?P<category_id>\d+)/edit$', 'customers.views.category_edit', name='category_edit'),

	# the url for the shelf_data list
	url(r'^shelf-data/show$', 'customers.views.shelf_data', name='shelf_data'),
	# the url for the shelf_data add
	url(r'^shelf-data/add$', 'customers.views.shelf_data_add', name='shelf_data_add'),
	# the url for the shelf_data edit
	url(r'^shelf-data/(?P<shelf_data_id>\d+)/edit$', 'customers.views.shelf_data_edit', name='shelf_data_edit'),

	# the url for the data_sets list
	url(r'^datasets/show$', 'customers.views.data_sets', name='data_sets'),
	# the url for the data_set add
	url(r'^dataset/add$', 'customers.views.data_set_add', name='data_set_add'),
	# the url for the data_set edit
	url(r'^dataset/(?P<data_set_id>\d+)/edit$', 'customers.views.data_set_edit', name='data_set_edit'),

	# the url for the customers_access list
	url(r'^access/show$', 'customers.views.customer_access', name='customer_access'),
	# the url for the customer_access add
	url(r'^access/add$', 'customers.views.customer_access_add', name='customer_access_add'),
	# the url for the customer_access edit
	url(r'^access/(?P<customer_access_id>\d+)/edit$', 'customers.views.customer_access_edit', name='customer_access_edit'),

	# the Customer Section
	url(r'^section/u/(?P<user_id>\d+)$', 'customers.views.customer_section', name='customer_section'),
]

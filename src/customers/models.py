# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categorys'

    def __unicode__(self):
        return u"{0}".format(self.name)


class ShelfData(models.Model):
    category = models.ForeignKey('Category')
    attribute_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Attribute Names')
    root_filename = models.CharField(max_length=100, blank=True, null=True, verbose_name='Root Filenames')
    units = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    show_totals = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Shelf Data'

    def __unicode__(self):
        return u"{0}".format(self.attribute_name)


class DataSet(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150, blank=True, null=True)
    results_directory = models.CharField(max_length=150, blank=True, null=True)
    shelf_data = models.ForeignKey('ShelfData', blank=True, null=True)

    def get_root_filename(self):
        if self.shelf_data:
            return self.shelf_data.root_filename
        return

    def get_attribute_name(self):
        if self.shelf_data:
            return self.shelf_data.attribute_name
        return

    class Meta:
        verbose_name_plural = 'DataSets'

    def __unicode__(self):
        return u"{0}".format(self.name)


class CustomerAccess(models.Model):
    user = models.ForeignKey(User, verbose_name='Customer Name')
    data_set = models.ManyToManyField(DataSet, related_name='customer_access', verbose_name='DataSets')

    def get_data_sets(self):
        return '; '.join([p.name for p in self.data_set.all()])

    class Meta:
        verbose_name_plural = 'Customer Access'

    def __unicode__(self):
        return u"{0}".format(self.user.username)


class CustomerInfoPanel(models.Model):
    user = models.ForeignKey(User, verbose_name='User', blank=True, null=True)
    data_set = models.ForeignKey('DataSet', blank=True, null=True)
    attribute_name = models.CharField(max_length=150, blank=True, null=True)
    statisctic = models.CharField(max_length=150, blank=True, null=True)
    # polygon = models.CharField(max_length=150, blank=True, null=True)

    file_area_name = models.CharField(max_length=150, blank=True, null=True)
    tif_path = models.CharField(max_length=150, blank=True, null=True)
    png_path = models.CharField(max_length=150, blank=True, null=True)
    url_png = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Customer Info Panel'

    def __unicode__(self):
        return u"{0}_{1}".format(self.user, self.data_set)
        
        
class CustomerPolygons(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='User', blank=True, null=True)
    kml_name = models.CharField(max_length=150, blank=True, null=True)
    kml_path = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Customer Polygons'

    def __unicode__(self):
        return u"{0}_{1}".format(self.user, self.name)
        
        
class DataTerraserver(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='User', blank=True, null=True)
    shapefile_link = models.CharField(max_length=250, blank=True, null=True)
    shapefile = models.CharField(max_length=250, blank=True, null=True)
    parameter = models.CharField(max_length=250, blank=True, null=True)
    transaction_id = models.CharField(max_length=250, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.name = str(self.user) + '_' + str(self.shapefile)
        super(DataTerraserver, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Data from Terraserver'

    def __unicode__(self):
        return u"{0}".format(self.name)
    

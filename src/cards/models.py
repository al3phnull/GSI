# -*- coding: utf-8 -*-
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import \
    ugettext_lazy as _  # Always aware of translations to other languages in the future -> wrap all texts into _()
from django.contrib.contenttypes.models import ContentType
from django.db import models

from core.utils import (UnicodeNameMixin, update_list_files)


class NamedModel(UnicodeNameMixin, models.Model):
    """**Abstract model**.

    Inherits the *"name"* field
    """
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True


class ParallelModel(models.Model):
    """**Abstract model.**

        Inherits the *"run_parallel"* field

    """

    run_parallel = models.BooleanField(default=False)

    class Meta:
        abstract = True


class QRF(NamedModel):
    """**Model for the cards QRF.**

    :Functions:
        The Quantile Random Forest (QRF) process analyses all of the decision trees generated by
        RFtrain, looking at the distributions of all Y-parameter values across all trees, to determine
        the confidence that can be placed on each predicted value; this information can be used
        subsequently in scoring, to provide a range of statiscs for each scored pixel, including:
        Median, lower quartile, upper quartile, min (eg <5%) quantile, max (eg >95%) quantile,
        standard error, standard deviation, variance, and per-pixel quantile value.

    :Fields:

        **interval**: Confidence interval (overrides $QRF_INTERVAL)

        **number_of_trees**: Number of trees to use for QRF (overrides actual number of trees created)

        **number_of_threads**: Number of parallel threads to use for QRF

        **directory**: Identifies parent directory for trees, if not in default location (under $RF_DIR)

    """

    interval = models.CharField(max_length=200, blank=True)
    number_of_trees = models.IntegerField(default=0, blank=True)
    number_of_threads = models.IntegerField(default=1, blank=True)
    directory = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = _('QRF cards')


class RFScore(NamedModel, ParallelModel):
    """**Model for the cards RFScore.**

    :Functions:
        RFscore uses the Random Forest decision trees generated by RFtrain to predict the Y-
        parameter value for each combination of X-parameter values in the specified input files.
        The range of possible output files depends on whether QRF has been run, or not. If QRF has
        been run for the selected training set, then a number of statistical measures can be output,
        (based on the setting of the <QRFopts> command line argument). If QRF has not been run,
        then the only output will be the Conditional Mean of the predicted Y-parameters values.


    :Fields:

        **area**: Relation with the Area model from the applications GSI

        **year_group**: Relation with the YearGroup model from the applications GSI

        **bias_corrn**:Nnumber of parallel threads to use for QRF

        **number_of_threads**: Number of parallel threads used for QRF, if enabled ($QRF_INTERVAL>0)

        **QRFopts**: Controls outputs: 0=None, 1=Mean, 2=Median, 4=Min, 8=Max, 16=LowerQ, 32=UpperQ, 64=QRFstats (set OR of values), 128=Std Error, 256=Std Dev, 512=Variance (sigma sq), 1024=nVar, 2048=per pixel Quantile

        **ref_target**: Datatype used for training (eg 'Biomass'), which triggers generation of new target <90th quantile

        **clean_name**: Text to uniquely identify filename for new cleaned target (<RefTarget>_<CleanName>)

    """

    area = models.ForeignKey('gsi.Area')
    year_group = models.ForeignKey('gsi.YearGroup')
    bias_corrn = models.CharField(max_length=200, blank=True)
    number_of_threads = models.IntegerField(default=1, blank=True)
    QRFopts = models.CharField(max_length=200, blank=True)
    ref_target = models.CharField(max_length=200, blank=True)
    clean_name = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = _('RFScore cards')


class Remap(NamedModel, ParallelModel):
    """**Model for the cards Remap.**

    :Functions:
        Extracts/mosaics and remaps the specified input image(s) to the specified output min/max
        lat/long limits. If a shape file is specified, then the polygons within the shape file are used to
        identify which portions of the output will have remapped pixel values (all regions outside the
        polygons will be set to NO_DATA (=-9999)).
        This utility can be used for remapping files stored within the MODIS tiles directory structure
        (for a specified parameter name), with output as WGS84 image. It can also be used for
        extracting a subset of an existing WGS84 image and rescaling to the same size, with the same
        spatial resolution as other extracted images. The latter functionality can alternatively be
        achieved using the GDAL utility – gdalwarp.
        Remap also provides the option to output images as .png format files, using a user-specified
        colour look-up table (LUT). The lut may be in any of three formats: ".lut" as used by the
        OpenSource ImageJ program, .pal format, which are simple ASCII text files, with 2 header
        lines, then each of 256 lines containing "R G B" values, or .txt files which allow for
        specifying the LUT in terms of breakpoints, where each line contain 4 values ("breakpoint R
        G B"), and the software interpolates between each breakpoint to give the final 256 colour
        range.

    :Fields:

        **year_group**: Relation with the YearGroup model from the applications GSI

        **file_spec**: <subdir>/<fileroot> below $RF_DIR/Tiles/hxxvyy

        **roi**: <filename> With single line comprising: MinLat MinLon MaxLat MaxLon

        **model_name**: The name of the model

        **output_root**: Pathname and root for filename of all outputs generated (<OutRoot>_<ParamName>.tif)

        **output_suffix**: Suffix for output filenames, eg <OutRoout>/<ParamName>_<OutSuffix>.tif

        **scale**: Spatial resolution of required output (1000=1km, 250=250m etc)

        **output**: 1 for .tif, 2 for .png, 4 for .csv (OR value for multiple outputs)

        **color_table**: Full pathname for required colour LUT for .png

        **refstats_file**: Geotiff <filename>.tif

        **refstats_scale**: Scale factor for RefStatsFile pixel values

        **conditional_mean**: Boolean field

        **conditional_min**: Boolean field

        **conditional_median**: Boolean field

        **conditional_max**: Boolean field

        **lower_quartile**: Boolean field

        **upper_quartile**: Boolean field

    """

    year_group = models.ForeignKey('gsi.YearGroup', blank=True, null=True)
    file_spec = models.CharField(max_length=200)
    roi = models.CharField(max_length=200)
    model_name = models.CharField(max_length=200, blank=True, null=True)
    output_root = models.CharField(max_length=200)
    output_suffix = models.CharField(max_length=200, blank=True)
    scale = models.CharField(max_length=200, blank=True)
    output = models.CharField(max_length=200, blank=True)
    color_table = models.CharField(max_length=200, blank=True)
    refstats_file = models.CharField(max_length=200, blank=True)
    refstats_scale = models.PositiveIntegerField(blank=True, null=True)

    conditional_mean = models.BooleanField(default=False)
    conditional_min = models.BooleanField(default=False)
    conditional_median = models.BooleanField(default=False)
    conditional_max = models.BooleanField(default=False)
    lower_quartile = models.BooleanField(default=False)
    upper_quartile = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = _('Remap cards')


class YearFilter(NamedModel, ParallelModel):
    """**Model for the cards YearFilter.**

    :Functions:
        Applies filtering across multiple years (either Fourier filter of specified order, or Kalman
        filter with specified gain scale factor) to all geotiff input images for the specified time period,
        covering (per-year) output from Calcstats or output from RFscore.


    :Fields:

        **area**: Relation with the Area model from the applications GSI

        **filetype**: Values to determine which files to output

        **filter**: Smoothing filter method

        **filter_output**: Selection of output images

        **extend_start**: Number of years to extend the start backwards to attempt better early fit (default=0)

        **input_fourier**: Value for NDVI files, maximum Fourier order used in CalcStats

        **output_directory**: Specific output directory

        **input_directory**: Specific input directory

    """

    area = models.ForeignKey('gsi.Area')
    filetype = models.CharField(max_length=50)
    filter = models.CharField(max_length=200, blank=True)
    filter_output = models.CharField(max_length=200, blank=True)
    extend_start = models.CharField(max_length=200, blank=True)
    input_fourier = models.CharField(max_length=200, blank=True)
    output_directory = models.CharField(max_length=200, blank=True)
    output_directory = models.CharField(max_length=200, blank=True)
    input_directory = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = _('YearFilter cards')


class Collate(NamedModel, ParallelModel):
    """**Model for the cards Collate.**

    :Functions:
        Processing GeoTIFF files to specify the tiles.


    :Fields:

        **area**: Relation with the Area model from the applications GSI

        **mode**: Data are MODIS, DEM and soil

        **output_tile_subdir**: Output tile subdirectory/filename root

        **input_scale_factor**: Input scale factor

        **input_data_directory**: Relation with the InputDataDirectory model from the applications GSI

        **input_files**: Input ad-hoc geotiff filename, assumed to be in $RF_AUXDATA_DIR directory.
        Relation with the InputDataDirectory model from the applications GSI

    """

    def __init__(self, *args, **kwargs):
        super(Collate, self).__init__(*args, **kwargs)

        if self.input_data_directory is not None:
            update_list_files(self.input_data_directory)

    area = models.ForeignKey('gsi.Area')
    mode = models.CharField(max_length=200, blank=True)
    output_tile_subdir = models.CharField(max_length=200, blank=True)
    input_scale_factor = models.CharField(max_length=200, blank=True)
    input_data_directory = models.ForeignKey('gsi.InputDataDirectory', blank=True, null=True)
    input_files = models.ManyToManyField('gsi.ListTestFiles', blank=True, related_name='input_files')

    class Meta:
        verbose_name_plural = _('Collate cards')


class PreProc(NamedModel, ParallelModel):
    """**Model for the cards PreProc.**

    :Functions:
        The normal use for PreProc is to extract selected bands from MODIS hdf files (in the per-tile
        directory structure under $MODIS_DIR), saving the extracted images as GeoTiffs in the
        appropriate per-tile location in the directory structure under $SAT_TIF_DIR.


    :Fields:

        **area**: Relation with the Area model from the applications GSI

        **mode**: Extracts GeoTiffs from hdf and performs stats for selected year(s)

        **year_group**: Relation with the YearGroup model from the applications GSI

        **path_spec_location**: The full path to a specific hdf file

    """

    area = models.ForeignKey('gsi.Area', null=True, blank=True)
    mode = models.CharField(max_length=50, blank=True)
    year_group = models.ForeignKey('gsi.YearGroup', null=True, blank=True)
    path_spec_location = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = _('PreProc cards')


class MergeCSV(NamedModel, models.Model):
    """**Model for the cards MergeCSV.**

    :Functions:
        Data on csv files.


    :Fields:

        **csv1**: Filename

        **csv2**: Filename

    """

    csv1 = models.CharField(max_length=200, blank=True)
    csv2 = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = _('MergeCSV cards')


class RFTrain(NamedModel, ParallelModel):
    """**Model for the cards RFTrain.**

    :Functions:
        Core Random Forest processing, which uses the specified “target” (Y-parameter) imagery as
        the basis for training using all the specified input “X-parameter” images as the basis. (this
        will enable subsequent scoring using other images (different times/locations) for X-
        parameters to derive the target Y-parameter values for those times and locations.

        The main output from RFtrain are a set of decision trees, which define how any combination
        of input X-parameters can be used to predict a corresponding output Y-parameter.


    :Fields:

        **tile_type**: Relation with the TileType model from the applications GSI

        **number_of_trees**: The number of trees to use in randomForest (default = 50)

        **value**: Value

        **config_file**: The configuration file

        **output_tile_subdir**: The output tile subdirectory

        **input_scale_factor**: The input scale factor

        **training**: Integer field

        **number_of_variable**: Number of iterations used for tree node (or automatically calculated if not defined)

        **number_of_thread**: Number of parallel threads used for tree generation (default is one, if not defined)

    """

    tile_type = models.ForeignKey('gsi.TileType')
    number_of_trees = models.IntegerField(default=50, blank=True)
    value = models.CharField(max_length=200)
    config_file = models.CharField(max_length=200, blank=True)
    output_tile_subdir = models.CharField(max_length=200, blank=True)
    input_scale_factor = models.CharField(max_length=200, blank=True)
    training = models.PositiveIntegerField(blank=True, null=True)
    number_of_variable = models.PositiveIntegerField(blank=True, null=True)
    number_of_thread = models.PositiveIntegerField(default=1, blank=True, null=True)

    class Meta:
        verbose_name_plural = _('RFTRain cards')


class RandomForest(NamedModel):
    """**Model for the cards RandomForest.**

    :Functions:
        Random Forest processing.


    :Fields:

        **aoi_name**: Character field

        **satellite**: Relation with the Satellite model from the applications GSI

        **param_set**: Text field

        **run_set**: Character field

        **model**: Character field

        **mvrf**: Character field

    """

    aoi_name = models.CharField(max_length=200)
    satellite = models.ForeignKey('gsi.Satellite')
    param_set = models.TextField()
    run_set = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    mvrf = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = _('Random Forest cards')

    def __unicode__(self):
        return u"{0}".format(self.name)


PERIOD = (
    ('year', 'Year'),
    ('quarter', 'Quarter'),
    ('month', 'Month'),
    ('doy', 'Input a variable'),
)

FILTER_OUT = (
    ('select', 'Select'),
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
)


class CalcStats(NamedModel, ParallelModel):
    """**Model for the cards CalcStats.**

    :Functions:
        Applies filtering (either Fourier filter of specified order, or Kalman filter with specified gain
        scale factor) to all geotiff input images for the specified time period. Also performs statistics
        on the resulting imagery, giving mean, min, max, median values per pixel.


    :Fields:

        **output_tile_subdir**: Output directory

        **year_group**: Relation with the YearGroup model from the applications GSI

        **area**: Relation with the Area model from the applications GSI

        **period**: Time period over which statistics are calculated

        **doy_variable**: Character field

        **filter**: Order of Fourier series to fit to time-series (default=0)

        **filter_out**: Filtered outputs

        **input_fourier**: Character field

        **out_dir**: Output directory (if non-MODIS tile specified as first argument)

        **path_spec_location**: The path to the location of a special file

    """

    output_tile_subdir = models.CharField(max_length=200)
    year_group = models.ForeignKey('gsi.YearGroup', null=True, blank=True)
    area = models.ForeignKey('gsi.Area', null=True, blank=True)
    period = models.CharField(max_length=100, choices=PERIOD, default='year', null=True, blank=True)
    doy_variable = models.CharField(max_length=200, null=True, blank=True)
    filter = models.PositiveIntegerField(default=0, blank=True, null=True)
    filter_out = models.CharField(max_length=100, choices=FILTER_OUT, null=True, blank=True)
    input_fourier = models.CharField(max_length=200, null=True, blank=True)
    out_dir = models.CharField(max_length=200, null=True, blank=True)
    path_spec_location = models.CharField(max_length=200, null=True, blank=True)


class CardItem(models.Model):
    """**Model for the cards CardItem.**

    :Functions:
        It writes to the database all models Cards application.

    :CONTENT_LIMIT:
        The list of the all models Cards application.


    :Fields:

        **name**: Model name

        **content_type**: Relation with the ContentType model

        **object_id**: ID of the element from the model

        **content_object**: Associates model element and its ID

        **order**: The order of an element

    """

    CONTENT_LIMIT = (
        models.Q(app_label='cards', model='rftrain') |
        models.Q(app_label='cards', model='mergecsv') |
        models.Q(app_label='cards', model='preproc') |
        models.Q(app_label='cards', model='collate') |
        models.Q(app_label='cards', model='yearfilter') |
        models.Q(app_label='cards', model='remap') |
        models.Q(app_label='cards', model='rfscore') |
        models.Q(app_label='cards', model='qrf') |
        models.Q(app_label='cards', model='randomforest') |
        models.Q(app_label='cards', model='calcstats')
    )

    name = models.CharField(max_length=200, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, limit_choices_to=CONTENT_LIMIT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('content_type', 'object_id')

    def get_name(self):
        return u"{0}".format(self.content_object)

    def save(self, *args, **kwargs):
        self.name = u"{0}".format(self.content_object)
        return super(CardItem, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"{0}".format(self.content_object)


class OrderedCardItem(models.Model):
    """**Model for the cards OrderedCardItem.**

    :Functions:
        It writes to the database all models Cards application.

    :CONTENT_LIMIT:
        The list of the all models Cards application.


    :Fields:

        **name**: Model name

        **content_type**: Relation with the ContentType model

        **object_id**: ID of the element from the model

        **content_object**: Associates model element and its ID

        **order**: The order of an element the CardItem model

    """

    card_item = models.ForeignKey(CardItem)
    order = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return u"{0}".format(self.card_item)


def get_card_item(self):
    """Get an element the CardItem model or create a new."""

    card_item, created = CardItem.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(self.__class__),
            object_id=self.pk,
    )
    return card_item


def __unicode__(self):
    return self.name


ContentType.__unicode__ = __unicode__


@receiver(post_save)
def auto_add_card_item(sender, instance=None, created=False, **kwargs):
    """To write a new element models of the Cards applications in the CardItem model."""

    list_of_models = (
        RFScore, RFTrain, QRF, YearFilter, MergeCSV,
        Collate, PreProc, Remap, RandomForest, CalcStats
    )
    if sender in list_of_models:
        if created:
            get_card_item(instance)

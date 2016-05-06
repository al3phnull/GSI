# -*- coding: utf-8 -*-import os, stat# import subprocessfrom subprocess import callfrom subprocess import Popen, PIPEfrom datetime import datetimefrom django.conf import settingsfrom django.utils.translation import ugettext_lazy as _from gsi.settings import (EXECUTE_FE_COMMAND,                          STATIC_ROOT, STATIC_DIR)class UnicodeNameMixin(object):    def __unicode__(self):        return _(u"%s") % self.namedef validate_status(status):    from gsi.models import STATES    states = [st[0] for st in STATES]    if not status or status not in states:        return {            'status': False,            'message': 'Invalid or missing "status" GET parameter.'        }    return {'status': status}def slash_remove_from_path(path):    result = path    if '//' in path:        result = path.replace('//', '/')    elif '///' in path:        result = path.replace('///', '/')    return resultdef create_symlink(src, dest, path):    if not os.path.exists(path):        symlink = call("ln -s {0} {1}".format(dest, src), shell=True)    else:        passdef get_dir_root_static_path():    from gsi.models import HomeVariables    home_var = HomeVariables.objects.all()    user_dir_root = home_var[0].USER_DATA_DIR_ROOT    static_dir_root = user_dir_root.split('/')[-1]    if not static_dir_root:        static_dir_root = user_dir_root.split('/')[-2:-1]    static_dir_root_path = STATIC_DIR + '/' + static_dir_root[0]    static_dir_root_path = slash_remove_from_path(static_dir_root_path)    return {        'static_dir_root': static_dir_root[0],        'static_dir_root_path': static_dir_root_path,    }def make_run(run_base, user):    from gsi.models import Run, Log, RunStep, OrderedCardItem    from gsi.models import HomeVariables as Home    now = datetime.now()    # status = True    step = RunStep.objects.none()    scripts = []    first_script = {}    path_test_data = ''    run = Run.objects.create(run_base=run_base, user=user)    home_var = Home.objects.all()    resolution = run.run_base.resolution    directory_path = run.run_base.directory_path    # first_card = OrderedCardItem.objects.filter(sequence__runbase=run_base).order_by('order').first()    all_card = OrderedCardItem.objects.filter(sequence__runbase=run.run_base).order_by('order')    try:        # <USER_DATA_DIR_ROOT>/<resolution>        path_test_data = home_var[0].USER_DATA_DIR_ROOT + '/' + str(resolution) + '/' + str(directory_path) + '/'        path_test_data = path_test_data.replace('//', '/')        try:            os.makedirs(path_test_data)            # write log file            # path_file = '/home/gsi/logs/0_make_dirs.log'            # now = datetime.now()            # log_file = open(path_file, 'a')            # log_file.writelines('{0}\n'.format(now))            # log_file.writelines('PATH TESTS: {0}\n\n\n'.format(path_test_data))            # log_file.close()        except OSError, e:            print '*** FOLDER EXIST ***'            # write log file            # path_file = '/home/gsi/logs/1_make_dirs.log'            # now = datetime.now()            # log_file = open(path_file, 'a')            # log_file.writelines('{0}\n'.format(now))            # log_file.writelines('PATH TESTS: {0}\n'.format(path_test_data))            # log_file.writelines('ERROR: {0}\n\n\n'.format(e))            # log_file.close()    except Exception, e:        # write log file        path_file = '/home/gsi/logs/2_make_dirs.err'        now = datetime.now()        log_file = open(path_file, 'a')        log_file.writelines('{0}\n'.format(now))        log_file.writelines('PATH TESTS: {0}\n'.format(path_test_data))        log_file.writelines('ERROR: {0}\n\n\n'.format(e))        log_file.close()    for card in all_card:        step = RunStep.objects.create(parent_run=run, card_item=card)        #TODO: make scripts for each step        sequence = step.parent_run.run_base.card_sequence        script = create_scripts(run, sequence, card, step)        script['step'] = step        scripts.append(script)    # if all_card is not None:    #     first_step = all_card.first()	#    #     #TODO: make script for first step    #     sequence = first_step.parent_run.run_base.card_sequence    #     script = create_scripts(run, sequence, first_step, first_step)    #     script['step'] = first_step    #     first_script.append(script)    if scripts:        first_script = scripts[0]        # write log file        path_file = '/home/gsi/logs/make_run.log'        now = datetime.now()        log_file = open(path_file, 'a')        log_file.writelines('{0}\n'.format(now))        log_file.writelines('SCRIPTS: \n')        log_file.writelines('name ==> {0}\n'.format(first_script['script_name']))        log_file.writelines('run ==> {0}\n'.format(first_script['run'].id))        log_file.writelines('card ==> {0}\n\n\n'.format(first_script['card'].id))        log_file.close()        ex_fe_com = Popen(            'nohup {0} {1} {2} &'.format(                EXECUTE_FE_COMMAND,                first_script['run'].id,                first_script['card'].id            ),            shell=True,        )        log_name = '{0}_{1}.log'.format(run.id, first_script['card'].id)        path_log = first_script['path_runs_logs']        write_log(log_name, run, path_log)        # log_file = open(path_log_file, 'a')        # log_file.writelines('LOG {0}_{1}:\n'.format(run.id, first_script['card'].id))        # log_file.writelines('LOG:' + '\n')        # ex_fe_com.wait()    # дождаться выполнения        # res_execute = ex_fe_com.communicate()  # получить tuple('stdout', 'stderr')        # if ex_fe_com.returncode:        #     print 'ERRROR ================= ', res_execute[1]        #     path_file = '/home/gsi/logs/runcards_{0}.error'.format(data['card'].id)        #     log_file = open(path_file, 'a')        #     log_file.writelines('Fail' + '\n')        #     log_file.writelines(str(now) + '\n')        #     log_file.writelines('ERROR: ' + res_execute[1] + '\n')		#        #     log_name_error = '{0}_{1}.error'.format(run.id, data['card'].id)        #     path_log_error = data['path_runs_logs']        #     name_path_log = path_log + '/' + log_name        #     write_log(log_name_error, run, path_log_error)        #     file_err = open(name_path_log, 'w+')        #     file_err.writelines('ERROR' + '\n')        #     file_err.writelines('Status succes: ' + str(res_execute[0]) + '\n')        #     file_err.writelines('Status error: ' + str(res_execute[1]) + '\n\n\n')        #     file_err.close()		#        #     script['step'].state = 'fail'        #     script['run'].state = 'fail'        #     status = False        #     script['step'].save()        #     script['run'].save()        #     break        # else:        #     print 'SUC ================= ', res_execute[0]        #     path_file = '/home/gsi/logs/runcards_{0}.log'.format(data['card'].id)        #     log_file = open(path_file, 'a')        #     log_file.writelines('Sucess' + '\n')        #     log_file.writelines(str(now) + '\n')        #     log_file.writelines('Status succes: ' + res_execute[0] + '\n')        #     log_file.writelines('Status error: ' + res_execute[1] + '\n\n\n')		#        #     log_name = '{0}_{1}.log'.format(run.id, data['card'].id)        #     path_log = script['path_runs_logs']        #     name_path_log = path_log + '/' + log_name        #     write_log(log_name, run, path_log)        #     file_log = open(name_path_log, 'w+')        #     file_log.writelines('Sucess' + '\n')        #     file_log.writelines('Status succes: ' + str(res_execute[0]) + '\n')        #     file_log.writelines('Status error: ' + str(res_execute[1]) + '\n\n\n')        #     file_log.close()		#        #     # script['step'].state = 'success'        #     # script['step'].save()        # log_file.close()    return {'run': run, 'step': step}def create_scripts(run, sequence, card, step):    """ Create a script at startup run_base """    from gsi.models import HomeVariables as Home    # logs for api    # run, sequence, card, card_item    path_file = '/home/gsi/LOGS/create_scripts.log'    now = datetime.now()    log_file = open(path_file, 'a')    log_file.writelines('\n\n\nCREATE SCRIPT ==================\n')    log_file.writelines(str(now) + '\n')    log_file.writelines('RUN ==> {0}; ID ==> {1}\n'.format(run, run.id))    log_file.writelines('RUN BASE ==> {0}; ID ==> {1}\n'.format(run.run_base, run.run_base.id))    log_file.writelines('SEQUENCE ==> {0}; ID ==> {1}\n'.format(sequence, sequence.id))    log_file.writelines('CARD ==> {0}; ID ==> {1}\n'.format(card, card.id))    log_file.writelines('CARD ITEM ==> {0}; ID ==> {1}\n'.format(step.card_item.card_item, step.card_item.card_item.id))    # log_file.close()    home_var = Home.objects.all()    export_home_var = ''    # path_test_data = ''    LOCAL_VAR_GROUPS = ''    # directory_path = run.run_base.directory_path    # home dir scripts    GSI_HOME = settings.SCRIPTS_HOME    # <RESOLUTION_ENV_SCRIPT>    resolution = run.run_base.resolution    RESOLUTION_ENV_SCRIPT = GSI_HOME + 'bin/' + str(resolution) + '_config'    # <HOME_ENV_OVERRIDES>    for hv in home_var:        export_home_var += 'export SAT_TIF_DIR=' + hv.SAT_DIF_DIR_ROOT + '\n'        export_home_var += 'export RF_DIR=' + hv.RF_DIR_ROOT + '\n'        export_home_var += 'export USER_DATA_DIR=' + hv.USER_DATA_DIR_ROOT + '\n'        export_home_var += 'export MODIS_DIR=' + hv.MODIS_DIR_ROOT + '\n'        export_home_var += 'export RF_AUXDATA_DIR=' + hv.RF_AUXDATA_DIR + '\n'        export_home_var += 'export SAT_DIF_DIR=' + hv.SAT_DIF_DIR_ROOT    # <LOCAL_ENV_OVERRIDES>    log_file.writelines('LOCAL VAR GROUP ==================\n')    try:        local_var_groups = (run.run_base.card_sequence.environment_base.environment_variables).replace('\r\n', '\n')        local_var_groups = local_var_groups.splitlines()        LOCAL_VAR_GROUPS = ''        for line in local_var_groups:            if line != '':                ln = line.replace('export ', '')                LOCAL_VAR_GROUPS += u'export {0}\n'.format(ln)        log_file.writelines('LOCAL_VAR_GROUPS succes ==> {0}\n'.format(LOCAL_VAR_GROUPS))    except Exception, e:        # LOCAL_VAR_GROUPS = 'LOCAL_VAR_GROUPS: Error:: {0}'.format(e)        LOCAL_VAR_GROUPS = ''        log_file.writelines('LOCAL_VAR_GROUPS error ==> {0}\n'.format(e))    # <ENVIROMENT OVERRIDE>    log_file.writelines('ENVIROMENT OVERRIDE ==================\n')    try:        env_override = (run.run_base.card_sequence.environment_override).replace('\r\n', '\n')        env_override = env_override.splitlines()        ENVIROMENT_OVERRIDE = ''        for line in env_override:            log_file.writelines('ENVIROMENT_OVERRIDE LINE ==> {0}\n'.format(line))            if line != '':                ln = line.replace('export ', '')                ENVIROMENT_OVERRIDE += u'export {0}\n'.format(ln)        log_file.writelines('ENVIROMENT_OVERRIDE succes ==> {0}\n'.format(ENVIROMENT_OVERRIDE))    except Exception, e:        # ENVIROMENT_OVERRIDE = 'ENVIROMENT_OVERRIDE: Error:: {0}'.format(e)        ENVIROMENT_OVERRIDE = ''        log_file.writelines('ENVIROMENT_OVERRIDE error ==> {0}\n'.format(e))    # <EXECUTABLE>    log_file.writelines('EXECUTABLE ==================\n')    try:        card_item = step.card_item.card_item        EXECUTABLE = get_executable(run, sequence, card, card_item)        log_file.writelines('EXECUTABLE succes ==> {0}\n'.format(EXECUTABLE))    except Exception, e:        # EXECUTABLE = 'EXECUTABLE: Error:: {0}'.format(e)        EXECUTABLE = ''        log_file.writelines('EXECUTABLE error ==> {0}\n'.format(e))    # path to scripts for runs and steps    path_runs = GSI_HOME + 'scripts/runs/R_{0}/'.format(run.id)    path_runs_logs = GSI_HOME + 'scripts/runs/R_{0}/LOGS'.format(run.id)    # <USER_DATA_DIR_ROOT>/<resolution>    # write log file    # path_file = '/home/gsi/logs/2_make_dirs.log'    # now = datetime.now()    # log_file = open(path_file, 'a')    # log_file.writelines('{0}\n'.format(now))    # log_file.writelines('PATH RUNS {0}\n'.format(path_runs))    # log_file.writelines('PATH LOGS {0}\n'.format(path_runs_logs))    # log_file.writelines('PATH TESTS {0}\n'.format(path_test_data))    # log_file.close()    try:        os.makedirs(path_runs)        os.makedirs(path_runs_logs)        # os.makedirs(path_test_data)    except OSError:        print '*** FOLDER EXIST ***'    finally:        script_name = 'card_{0}.sh'.format(step.card_item.id)        script_path = path_runs + script_name        fd = open(script_path, 'w+')        fd.write('# Sequence: {0}, card: {1} - Generated {2} \n\n'.\                 format(sequence.name, card.card_item, step.start_date))        fd.writelines('. ' + RESOLUTION_ENV_SCRIPT + '\n\n')        fd.writelines(export_home_var + '\n\n')        fd.writelines(LOCAL_VAR_GROUPS + '\n\n')        fd.writelines(ENVIROMENT_OVERRIDE + '\n\n')        fd.writelines(EXECUTABLE)        os.chmod(script_path, 0777)        os.chmod(path_runs_logs, 0777)        fd.close()    log_file.close()    return {        'script_path': script_path,        'path_runs_logs': path_runs_logs,        'script_name': script_name,        'card': card_item.id,        'run': run,        'card': card    }def write_log(log_name, run, path_log):    from gsi.models import Log    log = Log.objects.create(name=log_name)    log.log_file_path = path_log    log.log_file = log_name    log.save()    run.log = log    run.save()def get_years(name):    from gsi.models import YearGroup    year_group = YearGroup.objects.get(name=name)    return year_group.years.through.objects.filter(yeargroup=year_group)def get_area_tiles(name):    from gsi.models import Area    card_area = Area.objects.get(name=name)    return card_area.tiles.through.objects.filter(area=card_area)def get_executable(run, sequence, card, card_item):    """ get the <EXECUTABLE> to script """    from cards.models import (RFScore, RFTrain, QRF,                              Remap, YearFilter, PreProc,                              Collate, MergeCSV, RandomForest)    from gsi.models import Year, Tile    # CARD_MODEL = (    #     'qrf',        +    #     'rfscore',    +    #     'remap',      +    #     'yearfilter', +    #     'preproc',    +    #     'collate',    +    #     'rftrain',    ?    #     'mergecsv',   -    #     'randomforest'    # )    card_model = card_item.content_type.model    # name_card = step.card_item.card_item.content_object    EXECUTABLE = ''    pid = 1    # write log file    # path_file = '/home/gsi/LOGS/card_create_script.log'    # now = datetime.now()    # log_file = open(path_file, 'a')    # log_file.writelines('{0}\n'.format(now))    # log_file.writelines('CARD MODEL: {0}\n'.format(card_model))    # log_file.writelines('CARD MODEL: {0}\n\n\n'.format(card.card_item.content_object))    # log_file.close()    if card_model == 'rfscore':        #  u'RFscore <Tile> [[MyDir]] [<BiasCorrn>] [<QRFopts>] [<RefTarget>] [<CleanName>]'        data_card = RFScore.objects.get(name=card.card_item.content_object)        years = get_years(data_card.year_group.name)        area_tiles = get_area_tiles(data_card.area)        for year in years:            year_card = Year.objects.get(id=year.year_id)            for tile in area_tiles:                tile_card = Tile.objects.get(id=tile.tile_id)                EXECUTABLE += '$RF_EXEC_DIR/RFscore {0} {1} {2} {3} {4} {5} -s {6}.{7}.{8}.{9}\n'.format(                        tile_card,                        # data_card.name,                        run.run_base.directory_path,                        data_card.bias_corrn,                        year_card,                        data_card.number_of_threads,                        data_card.QRFopts,                        run.id,                        sequence.id,                        card.id,                        pid,                )                pid += 1    if card_model == 'rftrain':        # u'RFtrain <Tile> [<Ntrees>] [<training>] [<Nvar>] [<Nthread>]'        data_card = RFTrain.objects.get(name=card.card_item.content_object)        # write log file        path_file = '/home/gsi/LOGS/rftrain_script.log'        now = datetime.now()        log_file = open(path_file, 'a')        log_file.writelines('{0}\n'.format(now))        log_file.writelines('CARD RFTrain: {0}\n'.format(card_model))        log_file.writelines('NAME RFTrain: {0}\n\n\n'.format(card.card_item.content_object))        log_file.writelines('VALUE: {0}\n'.format(data_card.value))        log_file.writelines('TREES: {0}\n'.format(data_card.number_of_trees))        log_file.writelines('VARIABLE: {0}\n'.format(data_card.number_of_variable))        log_file.writelines('TREAD: {0}\n'.format(data_card.number_of_thread))        log_file.close()        EXECUTABLE += '$RF_EXEC_DIR/RFtrain {0} {1} {2} {3} {4} -s {5}.{6}.{7}.{8}\n'.format(            data_card.value,            data_card.number_of_trees,            data_card.training,            data_card.number_of_variable,            data_card.number_of_thread,            run.id,            sequence.id,            card.id,            pid,        )        pid += 1    if card_model == 'qrf':        # u'QRF [<QRFinterval>] [<ntrees>] [<nthreads>] [<MyDir>]'        data_card = QRF.objects.get(name=card.card_item.content_object)        EXECUTABLE += '$RF_EXEC_DIR/QRF {0} {1} {2} {3} -s {4}.{5}.{6}.{7}\n'.format(            data_card.interval,            data_card.number_of_trees,            data_card.number_of_threads,            data_card.directory,            run.id,            sequence.id,            card.id,            pid,        )        pid += 1    if card_model == 'remap':        # u'Remap <FileSpec> <RoI> <OutRoot>[,<OutSuffix>] [<ColourTable>] [<RefStatsFile>] [<RefStatsScale>]'        data_card = Remap.objects.get(name=card.card_item.content_object)        EXECUTABLE += '$RF_EXEC_DIR/Remap {0} {1} {2} {3} {4} {5} {6} -s {7}.{8}.{9}.{10}\n'.format(            data_card.file_spec,            data_card.roi,            data_card.output_root,            data_card.output_suffix,            data_card.color_table,            data_card.refstats_file,            data_card.refstats_scale,            run.id,            sequence.id,            card.id,            pid,        )        pid += 1    if card_model == 'yearfilter':        # u'YearFilter <Tile> <FileType> [<Filter>] [<FiltOut>] [<ExtendStart>] [<InpFourier>] [<OutDir>] [<InpDir>]'        data_card = YearFilter.objects.get(name=card.card_item.content_object)        area_tiles = get_area_tiles(data_card.area)        for tile in area_tiles:            tile_card = Tile.objects.get(id=tile.tile_id)            EXECUTABLE += '$RF_EXEC_DIR/YearFilter {0} {1} {2} {3} {4} {5} {6} {7} -s {8}.{9}.{10}.{11}\n'.format(                tile_card,                data_card.filetype,                data_card.filter,                data_card.filter_output,                data_card.extend_start,                data_card.input_fourier,                data_card.output_directory,                data_card.input_directory,                run.id,                sequence.id,                card.id,                pid,            )            pid += 1    if card_model == 'preproc':        # u'PreProc [<Tile>|<file.hdf>] [<Year>] [<Mode>]'        data_card = PreProc.objects.get(name=card.card_item.content_object)        years = get_years(data_card.year_group.name)        area_tiles = get_area_tiles(data_card.area)        for year in years:            year_card = Year.objects.get(id=year.year_id)            for tile in area_tiles:                tile_card = Tile.objects.get(id=tile.tile_id)                EXECUTABLE += '$RF_EXEC_DIR/PreProc {0} {1} {2} -s {3}.{4}.{5}.{6}\n'.format(                    tile_card,                    year_card,                    data_card.mode,                    run.id,                    sequence.id,                    card.id,                    pid,                )                pid += 1    if card_model == 'collate':        # u'Collate <Tile> [<Mode>] [<InpFile>] [<OutDirFile>] [<InpScale>]'        data_card = Collate.objects.get(name=card.card_item.content_object)        area_tiles = get_area_tiles(data_card.area)        for tile in area_tiles:            tile_card = Tile.objects.get(id=tile.tile_id)            EXECUTABLE += '$RF_EXEC_DIR/Collate {0} {1} {2} {3} {4} -s {5}.{6}.{7}.{8}\n'.format(                tile_card,                data_card.mode,                data_card.input_file,                data_card.output_tile_subdir,                data_card.input_scale_factor,                run.id,                sequence.id,                card.id,                pid,            )            pid += 1    if card_model == 'randomforest':        # RunRandomForestModels.sh <AoI_Name> <Satellite> <ParamSet> <RunSet>        data_card = RandomForest.objects.get(name=card.card_item.content_object)        EXECUTABLE += 'export MODELDIR=/lustre/w23/mattgsi/satdata/RF/Projects/Models'        EXECUTABLE += 'export CSVFILE=/lustre/w23/mattgsi/satdata/RF/Projects/Lane/Data/ref/Model${0}.csv >> $MODELDIR/ParamSet_CSVbands.sh'.format(data_card.model)        EXECUTABLE += 'export MVRF_TOTAL={0} >> $MODELDIR/ParamSet_CSV"$XSET".sh'.format(data_card.mvrf)        EXECUTABLE += 'RunRandomForestModels.sh {0} {1} {2} {3} -s {4}.{5}.{6}.{7}\n'.format(            data_card.aoi_name,            data_card.satellite,            data_card.param_set,            data_card.run_set,            run.id,            sequence.id,            card.id,            pid,        )        pid += 1    # if card_model == 'mergecsv':    #     # MergeCSV <PathSpec>/<FileSpec> [<OutFile>] [<Scale>]    #     data_card = MergeCSV.objects.get(name=card)    #     EXECUTABLE += '$RF_EXEC_DIR/MergeCSV {0} {1} {2} -s {3}.{4}.{5}\n'.format(    #         run.id,    #         card_item.id,    #         pid,    #     )    return EXECUTABLE
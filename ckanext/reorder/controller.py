
import sys
import os
from operator import itemgetter

import pylons
import ckan

import ckan.lib.helpers as h
import ckan.plugins as plugins
from ckan.lib.base import BaseController
from ckan.lib.helpers import dataset_link, dataset_display_name
from ckan.lib.helpers import flash_error, flash_success, flash_notice
from ckan.logic.validators import package_name_exists
from ckan.logic.converters import convert_package_name_or_id_to_id as convert_to_id


def package_info(dsname, context):
    """ if package exists, returns dictionary containing:
    'view': True or False (can the user view the package)
    'edit': True or False (can the user edit the package)
    'package' the contents of the package

    Returns None if package doesn't exist
    """
    l = {'view': False, 'edit': False}

    #check package exists
    try:
        package_name_exists(dsname, context)
        print 'package_info: package_exists'
        package_id = convert_to_id(dsname, context)
    except Exception:
        #package doesn't exist
        l = None
        print 'package_info: package doesn\'t exist'

    #check user can view/edit
    if l:
        #view
        try:
            l['package'] = plugins.toolkit.get_action('package_show')(context, {'id': package_id})
            l['view'] = True
            print 'package_info: user can view'

            #edit
            try:
                l['edit'] = plugins.toolkit.check_access('package_update', context, data_dict={'id': package_id})
                print 'package_info: user can edit'
            except plugins.toolkit.NotAuthorized:
                print 'package_infop: not authorised to edit'

        except Exception:
            #print 'package_info: user can\'t view'
            pass

    return l


class ReorderController(BaseController):
    """
    ckanext-reorder controller
    """

    def bad_url(self):
        flash_notice('please form URL in this format: http://<your_website>/reorder/<dataset_name>')
        #return plugins.toolkit.render('bad_url.html')
        return plugins.toolkit.render('index.html')

    def result(self):

        context = {'model': ckan.model,
                   'session': ckan.model.Session,
                   'user': pylons.c.user or pylons.c.author}

        #check for POST data
        if ckan.plugins.toolkit.request.method == 'POST':
            data = ckan.plugins.toolkit.request.POST
            dataset = data['dataset']
            resources = data['resources'].split(';')

            try:
                package = plugins.toolkit.get_action('package_show')(context, {'id': dataset})
            except Exception:
                flash_error('error: update unsuccessful')

            #list of resources
            target_resources = package['resources']

            reorder_list = []

            for res in resources:
                index = map(itemgetter('name'), target_resources).index(res)
                reorder_list.append(target_resources[index])

            package['resources'] = reorder_list

            try:
                package = plugins.toolkit.get_action('package_update')(context, package)
                flash_success('resources in ' + dataset_display_name(package) + ' have been updated')
            except:
                #something went wrong with the update
                flash_error('error: update unsuccessful')
            plugins.toolkit.c.resources = [item['name'] for item in package['resources']]
            plugins.toolkit.c.name = package['name']
            plugins.toolkit.c.link = dataset_link(package)
        #no POST data - redirect to home page
        else:
            ckan.plugins.toolkit.redirect_to(controller="home", action="index")

        return plugins.toolkit.render('result.html')


    def index(self, dsname):

        context = {'model': ckan.model,
                   'session': ckan.model.Session,
                   'user': pylons.c.user or pylons.c.author}

        pk_info = package_info(dsname, context)

        #flash messages
        no_view_msg = dsname + ', might not exist or you might not have permission to view or edit this dataset'
        no_edit_msg = 'you do not have permission or need to be logged-in to reorder this dataset'

        #if package doesn't exist
        if not pk_info:
            flash_error(no_view_msg)

        #package exists
        else:
            if not pk_info['edit']:
                flash_notice(no_edit_msg)

            if pk_info['view']:
                    plugins.toolkit.c.name = dsname
                    plugins.toolkit.c.view = pk_info['view']
                    plugins.toolkit.c.edit = pk_info['edit']
                    plugins.toolkit.c.resources = [item['name'] for item in pk_info['package']['resources']]

        return plugins.toolkit.render('index.html')

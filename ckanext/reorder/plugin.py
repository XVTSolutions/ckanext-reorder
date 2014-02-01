import ckan.plugins as plugins


class ReorderPlugin(plugins.SingletonPlugin):
    """
    Setup plugin
    """
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IConfigurer, inherit=True)

    def before_map(self, map):

        map.connect('reorder', '/reorder',
            controller='ckanext.reorder.controller:ReorderController',
            action='bad_url')

        map.connect('reorder', '/reorder/result',
            controller='ckanext.reorder.controller:ReorderController',
            action='result')

        map.connect('reorder', '/reorder/{dsname}',
            controller='ckanext.reorder.controller:ReorderController',
            action='index')

        return map


    def update_config(self, config):
        plugins.toolkit.add_template_directory(config, 'templates')
        plugins.toolkit.add_public_directory(config, 'public')
        plugins.toolkit.add_resource('fanstatic', 'ckanext-reorder')
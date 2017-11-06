# coding=utf-8
from routes.mapper import SubMapper


class GobArRouter:

    def __init__(self, route_map):
        self.route_map = route_map

        self.home_controller = 'ckanext.gobar_theme.controller:GobArHomeController'
        self.home_routes = SubMapper(self.route_map, controller=self.home_controller)
        self.api_controller = 'ckanext.gobar_theme.controller:GobArApiController'
        self.package_controller = 'ckanext.gobar_theme.package_controller:GobArPackageController'
        self.config_controller = 'ckanext.gobar_theme.config_controller:GobArConfigController'
        self.user_controller = 'ckanext.gobar_theme.user_controller:GobArUserController'
        self.google_analytics_controller = 'ckanext.gobar_theme.google_analytics_controller:GobArGAController'

    def redirect(self, *routes):
        for url_from, url_to in routes:
            self.route_map.redirect(url_from, url_to)

    def set_routes(self):
        self.connect_home()
        self.connect_static()
        self.connect_datasets()
        self.connect_organizations()
        self.connect_groups()
        self.connect_users()
        self.remove_dashboard()
        self.remove_tags()
        self.remove_revision()
        # self.remove_admin()
        self.connect_api()
        self.connect_template_config()
        self.connect_google_analytics()

    def connect_home(self):
        self.home_routes.connect('/', action='index')

    # def connect_static(self):
    #     self.home_routes.connect('gobar_about', '/acerca', action='about')
    #     self.redirect(
    #         ('/about', '/acerca')
    #     )
    def connect_static(self):
        self.home_routes.connect('gobar_about', '/about', action='about')
        self.home_routes.connect('gobar_our_site', '/about/about-portal', action='about_our_site')
        self.home_routes.connect('gobar_legal', '/about/legal', action='about_legal')
        self.home_routes.connect('gobar_devs', '/about/developers', action='about_developers')
        self.home_routes.connect('gobar_glossary', '/about/glossary', action='about_glossary')
        self.redirect(
            ('/about', '/about')
        )
    def connect_google_analytics(self):
        with SubMapper(self.route_map, controller=self.google_analytics_controller) as m:
            m.connect('resource view embed', '/dataset/resource_view_embed/{resource_id}', action='resource_view_embed')

    def connect_datasets(self):
        with SubMapper(self.route_map, controller=self.package_controller) as m:
            m.connect('search', '/dataset', action='search', highlight_actions='index search')
            m.connect('add dataset', '/dataset/new', action='new')
            m.connect('edit dataset', '/dataset/edit/{id}', action='edit')
            m.connect('new resource', '/dataset/new_resource/{id}', action='new_resource')
        self.route_map.connect('/dataset/{id}/archive/{resource_id}', action='resource_read', controller='package')
        self.redirect(
            ('/dataset/history/{id:.*?}', '/dataset/{id}'),
            ('/dataset/activity/{id:.*?}', '/dataset/{id}'),
            ('/dataset/groups/{id:.*?}', '/dataset/{id}'),
            ('/dataset/followers/{id:.*?}', '/dataset/{id}'),
            ('/dataset/{id}/resource/{resource_id}', '/dataset/{id}/archive/{resource_id}')
        )

    def remove_dashboard(self):
        self.redirect(
            ('/dashboard', '/'),
            ('/dashboard/datasets', '/'),
            ('/dashboard/groups', '/'),
            ('/dashboard/organizations', '/'),
            ('/dashboard/{url:.*?}', '/dashboard')
        )

    def connect_organizations(self):
        self.route_map.connect('/organization', action='index', controller='organization')
        self.route_map.connect('/organization/new', action='new', controller='organization')
        self.redirect(
            ('/organization', '/organization'),
            ('/organization/list', '/organization'),
            ('/organization/{id}', '/organization/list'),
            ('/organization/activity/{id}/{offset}', '/organization/list'),
            ('/organization/about/{id}', '/organization/list'),
            ('/organization/admins/{id}', '/organization/list'),
            ('/organization/members/{id}', '/organization/list'),
            ('/organization/member_new/{id}', '/organization/list'),
            ('/organization/member_delete/{id}', '/organization/list'),
            ('/organization/history/{id}', '/organization/list'),
            ('/organization/bulk_process/{id}', '/organization/list')
        )

    def connect_groups(self):
        self.route_map.connect('group_new', '/group/new', action='new', controller='group')
        self.redirect(
            ('/group', '/'),
            ('/group/list', '/'),
            ('/group/{id}', '/group/list'),
            ('/group/about/{id}', '/group/list'),
            ('/group/members/{id}', '/group/list'),
            ('/group/member_new/{id}', '/group/list'),
            ('/group/member_delete/{id}', '/group/list'),
            ('/group/history/{id}', '/group/list'),
            ('/group/followers/{id}', '/group/list'),
            ('/group/follow/{id}', '/group/list'),
            ('/group/unfollow/{id}', '/group/list'),
            ('/group/admins/{id}', '/group/list'),
            ('/group/activity/{id}/{offset}', '/group/list')
        )

    def connect_users(self):
        self.route_map.connect('login', '/login', action='login', controller='user')
        self.route_map.connect('/logout', action='logout', controller='user')
        with SubMapper(self.route_map, controller=self.user_controller) as m:
            m.connect('/drafts', action="drafts")
            m.connect('/user/reset/{user_id}', action="password_reset")
            m.connect('user_datasets', '/user/{id:.*}', action='read')
            m.connect('/login', '/login', action='login')
            m.connect('/change_password', action="password_forgot")
            m.connect('/config/my_account', action="my_account")
            m.connect('/config/my_account/change_email', action="my_account_edit_email")
            m.connect('/config/my_account/change_password', action="my_account_edit_password")
            m.connect('/config/create_users', action="create_users")
            m.connect('/config/edit_user', action="edit_user")
            m.connect('/config/delete_user', action="delete_user")
            m.connect('/config/historical', action="user_history")
            m.connect('/config/historial.json', action="user_history_json")

        self.redirect(
            ('/user/login', '/'),
            ('/user/generate_key/{id}', '/'),
            ('/user/activity/{id}/{offset}', '/'),
            ('/user/activity/{id}', '/'),
            ('/user/follow/{id}', '/'),
            ('/user/unfollow/{id}', '/'),
            ('/user/followers/{id:.*}', '/'),
            ('/user/delete/{id}', '/'),
            ('/user/register', '/'),
            ('/user/reset', '/'),
            ('/user/set_lang/{lang}', '/'),
            ('/user', '/'),
            ('/user/_logout', '/logout'),
            ('/user/logged_out_redirect', '/'),
            ('/logout', '/logout')
        )

    def remove_tags(self):
        self.redirect(
            ('/tag', '/'),
            ('/tag/{url}', '/')
        )

    def remove_revision(self):
        self.redirect(
            ('/revision', '/'),
            ('/revision/list', '/'),
            ('/revision/edit/{id}', '/revision'),
            ('/revision/diff/{id}', '/revision'),
            ('/revision/{id}', '/revision')
        )

    def remove_admin(self):
        self.redirect(
            ('/ckan-admin', '/'),
            ('/ckan-admin/config', '/'),
            ('/ckan-admin/trash', '/'),
            ('/ckan-admin/{action}', '/')
        )

    def connect_api(self):
        with SubMapper(self.route_map, controller=self.api_controller, path_prefix='/api{ver:/3|}', ver='/3') as m:
            m.connect('/action/{logic_function}', action='action', conditions=dict(method=['GET', 'POST']))
            m.connect('/util/status', action='status')

    def connect_template_config(self):
        with SubMapper(self.route_map, controller=self.config_controller) as m:
            m.connect('/config/title', action='edit_title')
            m.connect('/config/portal', action='edit_home')
            m.connect('/config/header', action='edit_header')
            m.connect('/config/topics', action='edit_groups')
            m.connect('/config/social', action='edit_social')
            m.connect('/config/footer', action='edit_footer')
            m.connect('/config/datasets', action='edit_datasets')
            m.connect('/config/organization', action='edit_organizations')
            m.connect('/config/about', action='edit_about')
            m.connect('/config/metadata/google_fb', action='edit_metadata_google_fb')
            m.connect('/config/metadata/tw', action='edit_metadata_tw')
            m.connect('/config/welcome', action='edit_greetings')

        self.redirect(
            ('/config', '/config/title'),
            ('/config', '/config/metadata')
        )

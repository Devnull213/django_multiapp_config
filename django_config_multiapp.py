#!/usr/bin/env python3
import subprocess
import os

def first_config(project, apps, database):

    subprocess.run(['django-admin', 'startproject', project])
    os.chdir(project)
    subprocess.run(['mkdir', 'templates'])
    subprocess.run(['mkdir', 'static'])
    subprocess.run(['mkdir', 'apps'])

    for app in apps:
        os.chdir('apps')
        subprocess.run(['django-admin', 'startapp', app])
        os.chdir(app)
        subprocess.run(['touch', 'urls.py'])

        to_new_urls = 'from django.urls import path\nfrom . import views\n\nurlpatterns = [\n\tpath(\'\',  views.index),\n]'
        to_views = 'from django.shortcuts import render, redirect, HttpResponse\n\ndef index(request):\n\treturn HttpResponse(\'Creado en un abrir y cerrar de ojos\')'

        with open ('./urls.py', 'w') as url:
            url.write(to_new_urls)

        with open ('./views.py', 'w') as view:
            view.write(to_views)

        setting_apps = '\'django.contrib.staticfiles\','
        setting_apps_modified = f'\'django.contrib.staticfiles\',\n    \'apps.{app}\','
        url_settings_one= 'from django.urls import path'
        url_settings_two= 'path(\'admin/\', admin.site.urls)'

        os.chdir('../..')
        os.chdir(project)
        with open ('./settings.py', 'r') as settings:
            to_modify = settings.read()

        to_modify = to_modify.replace(setting_apps, setting_apps_modified)

        with open ('./settings.py', 'w') as settings:
            settings.write(to_modify)

        with open ('./urls.py', 'r') as urls:
            to_modify_urls = urls.read()

        to_modify_urls = to_modify_urls.replace(url_settings_one, url_settings_one+ ', include')
        to_modify_urls = to_modify_urls.replace(url_settings_two, url_settings_two+ f',\n    path(\'\', include(\'apps.{app}.urls\'))')

        with open ('./urls.py', 'w') as urls:
            urls.write(to_modify_urls)

        os.chdir('..')

#TODO: Separar todo lo que es de la app master en  una nueva funcion

    os.chdir('apps')
    subprocess.run(['django-admin', 'startapp', 'master'])
    os.chdir('master')
    subprocess.run(['touch', 'urls.py'])

    to_new_urls = 'from django.urls import path\nfrom . import views\n\nurlpatterns = [\n\tpath(\'\',  views.index),\n]'
    to_views = 'from django.shortcuts import render, redirect, HttpResponse\n\ndef index(request):\n\treturn HttpResponse(\'Creado en un abrir y cerrar de ojos\')'

    with open ('./urls.py', 'w') as url:
        url.write(to_new_urls)

    with open ('./views.py', 'w') as view:
        view.write(to_views)

    subprocess.run(['mkdir', 'static'])
    os.chdir('static')
    subprocess.run(['mkdir', 'master'])
    os.chdir('master')
    subprocess.run(['mkdir', 'js', 'css', 'img'])
    os.chdir('css')
    subprocess.run(['touch', 'style.css'])
    os.chdir('..')
    os.chdir('js')
    subprocess.run(['touch', 'app.js'])
    os.chdir('../../../../..')

#TODO: refactorizar todo esto, por el momento se queda así por apuro

    masterapp = 'master'
    setting_apps = '\'django.contrib.staticfiles\','
    setting_apps_modified = f'\'django.contrib.staticfiles\',\n    \'apps.{masterapp}\','
    url_settings_one= 'from django.urls import path'
    url_settings_two= 'path(\'admin/\', admin.site.urls)'

    os.chdir(project)
    with open ('./settings.py', 'r') as settings:
        to_modify = settings.read()

    to_modify = to_modify.replace(setting_apps, setting_apps_modified)

    with open ('./settings.py', 'w') as settings:
        settings.write(to_modify)

    with open ('./urls.py', 'r') as urls:
        to_modify_urls = urls.read()

    to_modify_urls = to_modify_urls.replace(url_settings_one, url_settings_one+ ', include')
    to_modify_urls = to_modify_urls.replace(url_settings_two, url_settings_two+ f',\n    path(\'\', include(\'apps.{masterapp}.urls\'))')

    with open ('./urls.py', 'w') as urls:
        urls.write(to_modify_urls)

    os.chdir('..')


    db_settings = 'DATABASES = {\n    \'default\': {\n        \'ENGINE\': \'django.db.backends.sqlite3\',\n        \'NAME\': os.path.join(BASE_DIR, \'db.sqlite3\'),\n    }\n}'
    db_settings_modified = 'DATABASES = {\n    \'default\': {\n\t\'ENGINE\': \'django.db.backends.postgresql\',\n\t\'NAME\': \'' + database + '\',\n\t\'USER\': \'postgres\',\n\t\'PASSWORD\': \'root\',\n\t\'HOST\': \'127.0.0.1\',\n\t\'PORT\': \'5432\',\n    }\n}'

    template_settings = '\'DIRS\': [],'
    template_settings_modified = '\'DIRS\': [os.path.join(BASE_DIR, \'templates\'),],'

    static_settings = 'STATICFILES_DIRS = [\n    os.path.join(BASE_DIR, \'static\')\n]'

    os.chdir(project)
    with open ('./settings.py', 'r') as settings:
        to_modify = settings.read()

    to_modify = to_modify.replace(db_settings, db_settings_modified)
    to_modify = to_modify.replace(template_settings, template_settings_modified)

    with open ('./settings.py', 'w') as settings:
        settings.write(to_modify)

    with open ('./settings.py', 'a') as settings:
        settings.write(static_settings)

if __name__ == "__main__":

    project = input('Enter project name: ')
    apps = input('Enter app\'s name separated by coma: ')
    database = input('Enter database\'s name: ')
    apps = apps.split(', ')
    first_config(project, apps, database)


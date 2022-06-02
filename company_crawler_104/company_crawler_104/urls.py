from django.conf.urls import include, url
from django.contrib import admin
from crawler_core import views as core_view

urlpatterns = [
    url(r'^$', core_view.home_page, name ='home_page'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', core_view.main_crawler, name ='search'),
    url(r'^csv_insert/', core_view.csv_to_db, name ='csv_insert'),
    # url(r'^selected/', core_view.select_to_excel, name ='selected'),
    url(r'^save/', core_view.save, name ='save'),
    url(r'^mapping/', core_view.mapping, name ='mapping'),
    url(r'^end_page/', core_view.mapping, name ='mapping'),
    url(r'^update_mapping/', core_view.update_mapping, name ='update_mapping'),

]

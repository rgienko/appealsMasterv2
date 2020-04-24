"""appealsMasterv2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app import views
from .views import parent_update_view

urlpatterns = [
    path(r'', views.home, name='home'),
    path('signin', views.sign_in, name='signin'),
    path('signout', views.sign_out, name='signout'),
    path('callback', views.callback, name='callback'),
    path(r'newAppeal/', views.new_appeal, name='new_appeal_master' ),
    path(r'charge-master/', views.charge_master_view, name='charge_master_url'),
    path(r'issue-master/', views.issue_master_view, name='issue_master_url'),
    path(r'issue-master/new/', views.new_issue_master, name='new_issue_master_url'),
    path(r'issue-master/detail/<pk>/', views.issue_detail_view, name='issue_detail_url'),
    path(r'issue-master/detail/<issue_id>/edit/', views.update_issue_view.as_view(), name='update_issue_url'),
    path(r'parent-master/', views.parent_master_view, name='parent_master_url'),
    path(r'parent-master/new/', views.new_parent_view, name='new_parent_url'),
    path(r'parent-master/edit/<parent_id>/', views.parent_update_view.as_view(), name='edit_parent_url'),
    path(r'prov-name-master/', views.provider_name_master_view, name='provider_name_master_url'),
    path(r'details/<pk>/', views.appeal_details, name='appeal_detail_url'),
    path(r'details/<pk>/', views.delete_issue, name='delete_issue'),
    path(r'transfer/<pk>/', views.transfer_issue_view, name='transfer_issue_url'),
    path(r'details/<pk>/critical_due/', views.add_critical_due_dates, name='add_critical_due_dates_url'),
    path(r'calendar/', views.calendar, name='calendar'),
]

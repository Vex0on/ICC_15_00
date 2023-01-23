from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('registration/', views.registration, name='registration'),
    path('remind_password/', views.remind_password, name='remind_password'),
    path('manager_panel/', views.manager_panel, name='manager_panel'),
    path('manager_panel/plan/', views.manager_plan, name='manager_plan'),
    path('manager_panel/plan/list/', views.manager_plan_list, name='manager_plan_list'),
    path('manager_panel/employees/', views.manager_employees, name='manager_employees'),
    path('manager_panel/employees/add/', views.manager_employees_add, name='manager_employees_add'),
    path('manager_panel/employees/add/workerAddress', views.manager_employees_add_worker_address, name='manager_employees_add_worker_address'),
    path('manager_panel/employees/show/<int:worker_id>/', views.manager_employees_show, name='manager_employees_show'),
    path('manager_panel/employees/delete/<int:worker_id>', views.manager_employees_delete, name='manager_employees_delete'),
    path('manager_panel/employees/edit/<int:worker_id>', views.manager_employees_edit, name='manager_employees_edit'),
    path('manager_panel/employees/edit/workerAddress/<int:worker_id>', views.manager_employees_edit_worker_address, name='manager_employees_edit_worker_address'),
    path('receptionist_panel/', views.receptionist_panel, name='receptionist_panel'),
    path('receptionist_panel/tickets/', views.receptionist_tickets, name='receptionist_tickets'),
    path('receptionist_panel/tickets_add/', views.receptionist_tickets_add, name='receptionist_tickets_add'),
    path('accountant_panel/', views.accountant_panel, name='accountant_panel'),
    path('accountant_accountancy/', views.accountant_accountancy, name='accountant_accountancy'),
    path('accountant_result/', views.accountant_result, name='accountant_result'),
    path('ticket_buy/swimming_pool/', views.ticket_buy_swimming_pool, name='ticket_buy_swimming_pool'),
    path('ticket_buy/gym/', views.ticket_buy_gym, name='ticket_buy_gym'),
    path('ticket_buy/spa/', views.ticket_buy_spa, name='ticket_buy_spa'),
]

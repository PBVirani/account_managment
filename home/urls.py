from django.contrib import admin
from django.urls import path 
from django.contrib.auth.decorators import login_required
from . import views
from home.views import Renderhomepage , addproductpage , viewproductpage, editproductdetails , addcustomerpage , viewcustomerpage, editcustomerdetails , vieworderpage , editorderdetails , addorderpage , addexpensepage , editexpensedetails , viewexpensepage , profiledetails , login , vieworderdetails , editproduct , editorder , editexpense ,editcustomer , viewrebates

urlpatterns = [
    path('', Renderhomepage.as_view(), name="Renderhomepage"),

    path('addproduct', addproductpage.as_view(), name="addproduct"),
    path('viewproduct', viewproductpage.as_view(), name="viewproduct"),
    path('editproductdetails/<id>', editproductdetails.as_view(), name="editproductdetails"),
    path('editproduct', editproduct.as_view(), name="editproduct"),

    path('addcustomer', addcustomerpage.as_view(), name="addcustomer"),
    path('viewcustomer', viewcustomerpage.as_view(), name="viewcustomer"),
    path('viewrebates/<id>', viewrebates.as_view(), name="viewrebates"),
    path('editcustomerdetails/<id>', editcustomerdetails.as_view(), name="editcustomerdetails"),
    path('editcustomer', editcustomer.as_view(), name="editcustomer"),

    path('addorder', addorderpage.as_view(), name="addorder"),
    path('vieworder', vieworderpage.as_view(), name="vieworder"),
    path('editorderdetails/<id>', editorderdetails.as_view(), name="editorderdetails"),
    path('vieworderdetails/<customer>/<id>', vieworderdetails.as_view(), name="vieworderdetails"),
    path('editorder', editorder.as_view(), name="editorder"),


    path('addexpense', addexpensepage.as_view(), name="addexpense"),
    path('viewexpense', viewexpensepage.as_view(), name="viewexpense"),
    path('editexpensedetails/<id>', editexpensedetails.as_view(), name="editexpensedetails"),
    path('editexpense', editexpense.as_view(), name="editexpense"),

    path('profile', profiledetails.as_view(), name="profile"),
    path('login', login.as_view(), name="login"),
    path('logout/', views.logout, name="Log Out"),
]
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse 
import pymongo
import random
from datetime import datetime
from django.utils import timezone
import json
from django.http import JsonResponse

connect_string = 'mongodb+srv://bvmengineeringcollege75:363mn35EliREfqgj@cluster0.jtuxc2q.mongodb.net/?retryWrites=true&w=majority' 
from django.conf import settings
my_client = pymongo.MongoClient(connect_string)
dbname = my_client['vasu']


# Dashboard view.
class Renderhomepage(View):
    template_name = 'HtmlContent/index.html'
    
    def get(self,request):
        if 'name' in request.session:
            parent_company = request.session['company']
            expense = dbname["expense"]
            rebate = dbname["rebate"]
            order = dbname["orders"]

            data = list(expense.find({'parent':parent_company}))
            data1 = list(rebate.find({'parent':parent_company}))
            data2 = list(order.find({'parent':parent_company}))
            
            sales_count = len(data2)

            total_expense = sum(int(item['amount']) for item in data)
            total_rebate = sum(int(item['rebate']) for item in data1)
            total_sales = sum(int(item['Total']) for item in data2)

            context ={
                    'expense':data,
                    'rebate':data1,
                    'total_expense':total_expense,
                    'total_rebate':total_rebate,
                    'total_sales':total_sales,
                    'sales':sales_count
                    }
            return render(request, self.template_name,context)  
        else:
            return HttpResponseRedirect('/logout')
# Product view.
class addproductpage(View):
    template_name = 'HtmlContent/addproduct.html'

    def get(self,request):
        if 'name' in request.session:
            return render(request, self.template_name) 
        else:
            return HttpResponseRedirect('/logout')
    
    def post(self,request):
        parent_company = request.session['company']
        prodcut = request.POST.get('product')
        productnumber = request.POST.get('productnumber')
        price = request.POST.get('price')

        collection_name = dbname["product"]
        productdetails = {
            "product": prodcut,
            "productnumber" : productnumber,
            "price" : price,
            "id":str(random.randint(10000, 99999)),
            "company":parent_company
        }
        collection_name.insert_one(productdetails)
        return HttpResponseRedirect("/viewproduct")
    
class viewproductpage(View):
    template_name = 'HtmlContent/viewproduct.html'

    def get(self,request):
        parent_company = request.session['company']
        if 'name' in request.session:
            collection_name = dbname["product"]
            data = list(collection_name.find({'company':parent_company}))
            return render(request, self.template_name,{"data":data}) 
        else:
            return HttpResponseRedirect('/logout')

class editproductdetails(View):
    template_name = 'HtmlContent/editproductdetails.html'

    def get(self,request,id):
        if 'name' in request.session:
            collection_name = dbname["product"]
            data = list(collection_name.find({'id':id}))
            return render(request, self.template_name,{'data':data}) 
        else:
            return HttpResponseRedirect('/logout')
    
class editproduct(View):
    def post(self,request):
        parent_company = request.session['company']
        id = request.POST.get('id')
        prodcut = request.POST.get('product')
        productnumber = request.POST.get('productnumber')
        price = request.POST.get('price')

        collection_name = dbname["product"]
        
        productdetails = {
            "product": prodcut,
            "productnumber" : productnumber,
            "price" : price,
            "company":parent_company
        }
        update_query = {"$set": productdetails}
        filter_query = {"id": id,"company":parent_company}  # Specify the filter criteria for the documents to update
    
        collection_name.update_one(filter_query,update_query)
        return HttpResponseRedirect("/viewproduct")


# Customer view.
class addcustomerpage(View):
    template_name = 'HtmlContent/addcustomer.html'

    def get(self,request):
        if 'name' in request.session:
            return render(request, self.template_name) 
        else:
            return HttpResponseRedirect('/logout')
    
    def post(self,request):
        collection_name = dbname["customer"]
        
        customer = request.POST.get('customer')
        company = request.POST.get('company')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        parent_company = request.session['company']
        customerdetails = {
            "id":str(random.randint(10000, 99999)),
            "customer":customer,
            "company":company,
            "contact":contact,
            "address":address,
            "pincode":pincode,
            "parent":parent_company
        }
        collection_name.insert_one(customerdetails)
        return HttpResponseRedirect("/viewcustomer")
    
class viewcustomerpage(View):
    template_name = 'HtmlContent/viewcustomer.html'

    def get(self,request):
        if 'name' in request.session:
            collection_name = dbname["customer"]
            rebate = dbname["rebate"]
            parent_company = request.session['company']

            data = list(collection_name.find({'parent':parent_company}))
            rebate = list(rebate.find({'parent':parent_company}))
            return render(request, self.template_name,{"data":data,"rebate":rebate,"total":0}) 
        else:
            return HttpResponseRedirect('/logout')
    
    def post(self,request):
        collection_name = dbname["rebate"]
        
        customer = request.POST.get('customer')
        rebate = request.POST.get('rebate')
        rebatedate = request.POST.get('rebatedate')
        parent_company = request.session['company']
        rebatedetails = {
            "id":str(random.randint(10000, 99999)),
            "customer":customer,
            "rebate":rebate,
            "rebatedate":rebatedate,
            "parent":parent_company
        }
        collection_name.insert_one(rebatedetails)
        return HttpResponseRedirect("/viewcustomer")

class editcustomerdetails(View):
    template_name = 'HtmlContent/editcustomerdetails.html'

    def get(self,request,id):
        parent_company = request.session['company']
        if 'name' in request.session:
            collection_name = dbname["customer"]
            data = list(collection_name.find({"id":id,"parent":parent_company}))
            return render(request, self.template_name,{"data":data}) 
        else:
            return HttpResponseRedirect('/logout')

class editcustomer(View):
    def post(self,request):

        id = request.POST.get('id')
        customer = request.POST.get('customer')
        company = request.POST.get('company')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        contact = request.POST.get('contact')
        parent_company = request.session['company']
        collection_name = dbname["customer"]
        
        customerdetails = {
            "customer":customer,
            "company":company,
            "contact":contact,
            "address":address,
            "pincode":pincode,
            "parent":parent_company
        }
        update_query = {"$set": customerdetails}
        filter_query = {"id": id}  # Specify the filter criteria for the documents to update
    
        collection_name.update_one(filter_query,update_query)
        return HttpResponseRedirect("/viewcustomer")
    
class viewrebates(View):
    template_name = 'HtmlContent/viewrebates.html'
    
    def get(self,request,id):
        collection_name = dbname["rebate"]
        data = list(collection_name.find({"customer":id}))
        total = 0
        for d in data:
            total += int(d['rebate'])
        return render(request,self.template_name,{'data':data,'total':total})

# Order view.
class addorderpage(View):
    template_name = 'HtmlContent/addorder.html'

    def get(self,request):
        parent_company = request.session['company']
        if 'name' in request.session:
            collection_name = dbname["customer"]
            data = list(collection_name.find({"parent":parent_company}))

            collection_name1 = dbname["product"]
            product = list(collection_name1.find({"company":parent_company}))
            return render(request, self.template_name,{"data":data,"product":product}) 
        else:
            return HttpResponseRedirect('/logout')
    
    def post(self,request):
        collection_name = dbname["orders"]
        parent_company = request.session['company']
        customer = request.POST.get('customer')
        order = request.POST.get('order')
        date = request.POST.get('orderdate')

        product = request.POST.get('jsondata')
        valid_json_string = product.replace("'", "\"")
        json_data = json.loads(valid_json_string)
        
        productlist = []
        total = 0
        for i in json_data:
                temp = {}
                temp['Product'] = i[0]
                temp['Quantity'] = i[1]
                temp['Price'] = i[2]
                temp['Total'] = i[3]
                total += int(i[3])
                productlist.append(temp)

        orderdetails = {
            "orderid":str(random.randint(00000, 99999)),
            "customer":customer,
            "order":order,
            "date":date,
            "product":productlist,
            "Total":total,
            "parent":parent_company
        }
        collection_name.insert_one(orderdetails)
        return HttpResponseRedirect("/vieworder")
    
class vieworderpage(View):
    template_name = 'HtmlContent/vieworder.html'

    def get(self,request):
        if 'name' in request.session:
            collection_name = dbname["orders"]
            parent_company = request.session['company']
            data = list(collection_name.find({"parent":parent_company}))
            return render(request, self.template_name,{'order': data}) 
        else:
            return HttpResponseRedirect('/logout')

class editorderdetails(View):
    template_name = 'HtmlContent/editorderdetails.html'

    def get(self,request,id):
        if 'name' in request.session:
            collection_name = dbname["orders"]
            parent_company = request.session['company']
            customer = dbname["customer"]
            customerdata = list(customer.find({"parent":parent_company}))

            product = dbname["product"]
            productdata = list(product.find({"company":parent_company}))

            data = list(collection_name.find({"orderid":id}))
            return render(request, self.template_name,{"data":data,"customer":customerdata,"product":productdata}) 
        else:
            return HttpResponseRedirect('/logout')

class editorder(View):
    template_name = 'HtmlContent/editorderdetails.html'

    def post(self,request):
        collection_name = dbname["orders"]
        parent_company = request.session['company']
        customer = request.POST.get('customer')
        order = request.POST.get('order')
        date = request.POST.get('orderdate')
        orderid = request.POST.get('orderid')

        product = request.POST.get('jsondata')

        if product:
            valid_json_string = product.replace("'", "\"")
            json_data = json.loads(valid_json_string)
            
            productlist = []
            total = 0
            for i in json_data:
                    temp = {}
                    temp['Product'] = i[0].strip()
                    temp['Quantity'] = i[1].strip()
                    temp['Price'] = i[2].strip()
                    temp['Total'] = i[3].strip()
                    total += int(i[3])
                    productlist.append(temp)

            orderdetails = {
                "customer":customer,
                "order":order,
                "date":date,
                "product":productlist,
                "Total":total
            }            
        else:
            orderdetails = {
                "customer":customer,
                "order":order,
                "date":date,
                "demo":product
            }
            

        update_query = {"$set": orderdetails}
        filter_query = {"orderid": orderid}  # Specify the filter criteria for the documents to update
    
        collection_name.update_one(filter_query,update_query)
        return HttpResponseRedirect("/vieworder")

class vieworderdetails(View):
    template_name = 'HtmlContent/vieworderdetails.html'

    def get(self,request,customer,id):
        parent_company = request.session['company']
        if 'name' in request.session:
            collection_name = dbname["orders"]
            data = list(collection_name.find({"orderid":str(id),"parent":parent_company}))

            customer1 = dbname["customer"]
            customerdata = list(customer1.find({"company":str(customer)}))

            company = dbname["company"]
            companydata = list(company.find({"company":parent_company}))

            return render(request, self.template_name,{"order":data,"customer":customerdata,"company":companydata}) 
        else:
            return HttpResponseRedirect('/logout')
        
# Expense view.
class addexpensepage(View):
    template_name = 'HtmlContent/addexpense.html'

    def get(self,request):
        if 'name' in request.session:
            return render(request, self.template_name) 
        else:
            return HttpResponseRedirect('/logout')
    
    def post(self,request):

        employee = request.POST.get('employee')
        expense = request.POST.get('expense')
        amount = request.POST.get('amount')
        expensedate = request.POST.get('expensedate')
        money = request.POST.get('money')
        parent_company = request.session['company']
        expensedetails = {
                "id":str(random.randint(00000, 99999)),
                "parent":parent_company,
                "employee":employee,
                "date":expensedate,
                "detail":expense,
                "amount":amount,
                "status":money
            }  
        collection_name = dbname["expense"]       
        collection_name.insert_one(expensedetails)
        return HttpResponseRedirect("/viewexpense")
    
class viewexpensepage(View):
    template_name = 'HtmlContent/viewexpense.html'

    def get(self,request):
        if 'name' in request.session:
            collection_name = dbname["expense"]
            parent_company = request.session['company']
            data = list(collection_name.find({"parent":parent_company}))
            return render(request, self.template_name,{"data":data}) 
        else:
            return HttpResponseRedirect('/logout')

class editexpensedetails(View):
    template_name = 'HtmlContent/editexpense.html'

    def get(self,request,id):
        if 'name' in request.session:
            collection_name = dbname["expense"]

            data = list(collection_name.find({"id":id }))
            return render(request, self.template_name,{"data":data}) 
        else:
            return HttpResponseRedirect('/logout')

class editexpense(View): 
    def post(self,request):
        collection_name = dbname["expense"]

        id = request.POST.get('id')
        employee = request.POST.get('employee')
        expense = request.POST.get('expense')
        amount = request.POST.get('amount')
        expensedate = request.POST.get('expensedate')
        money = request.POST.get('money')

        expensedetails = {
                "employee":employee,
                "date":expensedate,
                "detail":expense,
                "amount":amount,
                "status":money
            }  
        update_query = {"$set": expensedetails}
        filter_query = {"id": id}  # Specify the filter criteria for the documents to update
    
        collection_name.update_one(filter_query,update_query)
        return HttpResponseRedirect("/viewexpense")

# Profile Details    
class profiledetails(View):
    template_name = 'HtmlContent/profile.html'

    def get(self,request):
        if 'name' in request.session:
            collection_name = dbname["user"]
            data = list(collection_name.find({"id": str(52274) }))

            return render(request, self.template_name,{'data':data}) 
        else:
            return HttpResponseRedirect('/logout')
    def post(self,request):
        collection_name = dbname["user"]

        id = request.POST.get('id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        request.session['name'] = name
        details = {
                "name":name,
                "email":email,
                "contact":contact,
                "password":password
            }  
        update_query = {"$set": details}
        filter_query = {"id": id}  # Specify the filter criteria for the documents to update
    
        collection_name.update_one(filter_query,update_query)
        return HttpResponseRedirect('/') 


class login(View):
    template_name = 'HtmlContent/login.html'
    def get(self,request):
        return render(request, self.template_name) 
    
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        collection_name = dbname["user"]

        data =list(collection_name.find({"email": username,"password":password }))
        try:
            request.session['name'] = str(data[0]['name'])
            request.session['id'] = str(data[0]['id'])
            request.session['company'] = "Ajanta"
            return HttpResponseRedirect('/')
        except:
            message="Invalid Credentials!!  Please ChecK your Data"
            return render(request, self.template_name,{'message':message}) 

class changecompany(View):
    template_name = 'HtmlContent/index.html'
    def get(self,request):
        return render(request, self.template_name) 
    
    def post(self,request):
        try:
            request.session['company'] =  request.POST.get('company')
            return HttpResponseRedirect('/')
        except:
            message="Invalid Credentials!!  Please ChecK your Data"
            return render(request, self.template_name,{'message':message}) 
        
def logout(request):
    try:
        request.session.flush()
    except:
        pass
    return HttpResponseRedirect('/login') 
# # from django.shortcuts import render
#
# # Create your views here.
# from django.shortcuts import render
# from django.http import HttpResponse
# import requests
# # Create your views here.
# def users(request):
#     #pull data from third party rest api
#     response = requests.get('https://jsonplaceholder.typicode.com/users')
#     #convert reponse data into json
#     users = response.json()
#     # print(users)
#     # return HttpResponse("Users")
#     return render(request, "users.html")
#     pass

from django.shortcuts import render
from django.http import HttpResponse
import requests
# Create your views here.
def users(request):
    #pull data from third party rest api
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    #convert reponse data into json
    users = response.json()
    #print(users)
    return render(request, "users.html", {'users': users})
    pass
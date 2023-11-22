# todo_list/todo_app/views.py
from django.urls import reverse, reverse_lazy
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import ToDoItem, ToDoList



def SignupPage(request):
    if request.method== 'POST':
        uname=request.POST.get('username') 
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2') 

        if pass1 != pass2:
            return HttpResponse("Enter same passwords")
        else:
            my_user = User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')

    return render(request,'todo_app/signup.html')

def LoginPage(request):
    if request.method== 'POST':
        username=request.POST.get('username') 
        pass1=request.POST.get('pass')
        user= authenticate(request,username = username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return HttpResponse ('ENter correct credentials')   
    return render (request, 'todo_app/login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

class ListListView(LoginRequiredMixin, ListView):
    model = ToDoList
    template_name = "todo_app/index.html"

    def get_queryset(self):
        return ToDoList.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ItemListView(LoginRequiredMixin, ListView):
    model = ToDoItem
    template_name = "todo_app/todo_list.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(
            user=self.request.user,
            todo_list_id=self.kwargs["list_id"]
        )

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = ToDoList.objects.get(
            user=self.request.user,
            id=self.kwargs["list_id"]
        )
        return context

class ListCreate(LoginRequiredMixin, CreateView):
    model = ToDoList
    fields = ["title"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self):
        context = super().get_context_data()
        context["title"] = "Add a new list"
        return context

class ItemCreate(LoginRequiredMixin, CreateView):
    model = ToDoItem
    fields = ["todo_list", "title", "description", "due_date"]

    def get_initial(self):
        initial_data = super().get_initial()
        todo_list = ToDoList.objects.get(
            user=self.request.user,
            id=self.kwargs["list_id"]
        )
        initial_data["todo_list"] = todo_list
        return initial_data

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self):
        context = super().get_context_data()
        todo_list = ToDoList.objects.get(
            user=self.request.user,
            id=self.kwargs["list_id"]
        )
        context["todo_list"] = todo_list
        context["title"] = "Create a new item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])

class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = ToDoItem
    fields = ["todo_list", "title", "description", "due_date", "completed"]

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])

class ListDelete(LoginRequiredMixin, DeleteView):
    model = ToDoList
    success_url = reverse_lazy("index")

    def get_queryset(self):
        return ToDoList.objects.filter(user=self.request.user)

class ItemDelete(LoginRequiredMixin, DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context

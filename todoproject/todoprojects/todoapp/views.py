from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy

from .models import Task

from .forms import Taskform
from django.views.generic import ListView, DetailView, UpdateView, DeleteView


class Taskview(ListView):
    model=Task
    template_name = 'home.html'
    context_object_name = 'result'
class Taskdetailview(DetailView):
    model=Task
    template_name = 'detail.html'
    context_object_name = 'result'

class Taskupdateview(UpdateView):
        model = Task
        template_name = 'update.html'
        context_object_name = 'result'
        fields = ('name','priority','date')
        def get_success_url(self):
            return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})
class Taskdeleteview(DeleteView):
    model=Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')

def home(request):
   task1 = Task.objects.all()
   if request.method=='POST':
      name=request.POST.get('task')
      priority = request.POST.get('priority')
      date=request.POST.get('date')
      task=Task(name=name,priority=priority,date=date)
      task.save()
   return render(request,'home.html',{'result':task1})
def delete(request,taskid):
    task=Task.objects.get(id=taskid)
    if request.method=='POST':
        task.delete()
        return redirect('/')
    return render(request,'delete.html')
def update(request,id):
     task=Task.objects.get(id=id)

     form = Taskform(request.POST or None, request.FILES, instance=task)
     if form.is_valid():
         form.save()
         return redirect('/')
     return render(request, 'edit.html',{'f':form,'task':task})
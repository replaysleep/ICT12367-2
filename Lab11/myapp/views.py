from django.shortcuts import render,redirect
from django.http import HttpResponse
from myapp.models import Person

# Create your views here.
def index(request):
    all_person = Person.objects.all()
    return render(request, 'index.html', {"all_person": all_person})

def about(request):
    return render(request, 'about.html')

def form(request):
    if request.method == "POST":
        # รับค่าจากฟอร์ม
        name = request.POST.get("name")
        age = request.POST.get("age")

        # บันทึกข้อมูลลงฐานข้อมูล
        person = Person(
            name=name,
            age=age
        )
        person.save()
        
        # เปลี่ยนเส้นทางไปหน้าแรก
        return redirect("/")
    else:

        # แสดงฟอร์ม
        return render(request, "form.html")
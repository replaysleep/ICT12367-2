from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from myapp.models import Person
from django.db.models import Q

# Create your views here.
def index(request):
    # ดึงข้อมูลประชากรทั้งหมดมาก่อน
    all_person = Person.objects.all()
    
    # รับค่าคำค้นหาจากช่องค้นหา (name="q")
    query = request.GET.get('q')
    
    # ตรวจสอบว่ามีค่าค้นหาถูกพิมพ์ส่งมาหรือไม่
    if query:
        # ถ้ามีคำค้นหา ให้กรองข้อมูลเฉพาะคนที่ชื่อหรืออายุตรงกับคำค้นหา
        all_person = all_person.filter(Q(name__icontains=query) | Q(age__icontains=query))
    
    # ส่งข้อมูลไปแสดงผลที่หน้า index.html
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
    
def edit(request, person_id):
    # ดึงข้อมูลจาก ID ที่ส่งมา ถ้าไม่เจอจะแสดงหน้า 404
    person = get_object_or_404(Person, pk=person_id)
    
    if request.method == "POST":
        # รับค่าใหม่จากฟอร์มบันทึกลงตัวแปร
        person.name = request.POST.get("name")
        person.age = request.POST.get("age")
        person.save() # บันทึกการเปลี่ยนแปลง
        return redirect("/") # แก้ไขเสร็จแล้วกลับไปหน้าแรก
    else:
        # ถ้าไม่ใช่ POST ให้ส่งข้อมูล person ไปแสดงที่หน้า edit.html
        return render(request, "edit.html", {"person": person})

def delete(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    person.delete() # คำสั่งลบข้อมูล
    return redirect("/") # ลบเสร็จกลับไปหน้าแรก
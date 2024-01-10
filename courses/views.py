from django.shortcuts import render, redirect
from .models import Customer, CustomerItem, Subject, Course, Class, Newsletter, Cancel
from . import forms
from django.http import HttpResponse
from .forms import UserForm, FormCustomer, FormNewsletter, FormCancel
from django_elearning.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import datetime
# Create your views here.

courses = Course.objects.all()
search_str = ''

def index(request):
    subjects = Subject.objects.all()
    courses = Course.objects.all()
    classes = Class.objects.all()
    total_course = len(courses)
    top_5_course = Course.objects.all().order_by('-created')[:5]
    latest_class = Class.objects.all().order_by('-schedule')[:1]
    form_newsletter = FormNewsletter()
    username = request.session.get('username', 0)

    context = {
        'subjects': subjects, 'courses': courses, 'classes': classes, 
        'total_course': total_course, 'top_5_course': top_5_course,
        'latest_class': latest_class, 'form_newsletter': form_newsletter, 'username': username,
    }
    return render(request, 'courses/index.html', context=context)

def chi_tiet_khoa_hoc(request, slug):
    subjects = Subject.objects.all()
    courses = Course.objects.all()
    classes = Class.objects.all()
    total_course = len(courses)
    top_5_course = Course.objects.all().order_by('-created')[:5]
    course_select = Course.objects.get(slug=slug)
    form_newsletter = FormNewsletter()
    username = request.session.get('username', 0)

    context = {
        'subjects': subjects, 'courses': courses, 'classes': classes, 
        'total_course': total_course, 'top_5_course': top_5_course, 'course_select': course_select,
        'form_newsletter': form_newsletter, 'username': username,
    }
    return render(request, 'courses/chi-tiet-khoa-hoc.html', context=context)

def lich_khai_giang(request):
    subjects = Subject.objects.all()
    courses = Course.objects.all()
    classes = Class.objects.all()
    total_course = len(courses)
    top_5_course = Course.objects.all().order_by('-created')[:5]
    form_newsletter = FormNewsletter()
    username = request.session.get('username', 0)
    now = datetime.date.today()

    context = {
        'subjects': subjects, 'courses': courses, 'classes': classes, 
        'total_course': total_course, 'top_5_course': top_5_course,
        'form_newsletter': form_newsletter, 'username': username, 'now': now,
    }
    return render(request, 'courses/lich-khai-giang.html', context=context)

def lich_khai_giang_lop(request, slug=None):
    subjects = Subject.objects.all()
    courses = Course.objects.all()
    if slug:
        course_select = Course.objects.get(slug=slug)
        classes = Class.objects.filter(course=course_select)
    total_course = len(courses)
    top_5_course = Course.objects.all().order_by('-created')[:5]
    form_newsletter = FormNewsletter()
    username = request.session.get('username', 0)
    now = datetime.date.today()
    context = {
        'subjects': subjects, 'courses': courses, 'classes': classes, 'course_select': course_select, 
        'total_course': total_course, 'top_5_course': top_5_course,'form_newsletter': form_newsletter,
        'username': username, 'now': now,
    }
    return render(request, 'courses/lich-khai-giang.html', context=context)

def dang_ky(request, slug):
    subjects = Subject.objects.all()
    courses = Course.objects.all()
    class_select = Class.objects.get(slug=slug)
    total_course = len(courses)
    top_5_course = Course.objects.all().order_by('-created')[:5]
    form_newsletter = FormNewsletter()
    students = len(CustomerItem.objects.filter(reg_class=class_select))
    username = request.session.get('username', 0)
    if username:
        reg_class_qs = CustomerItem.objects.filter(reg_class=class_select)
        if reg_class_qs.exists():
            result = '<h5 style="color:blue"><center>BẠN ĐÃ ĐĂNG KÝ KHOÁ HỌC NÀY RỒI</center></h5>'
        else:
            cus = Customer.objects.get(username=username)
            CustomerItem.objects.create(customer=cus, reg_class=class_select)

            #Gửi Email
            recepient = str(cus.email)
            result = 'Chúng tôi đã nhận thông tin đăng ký khoá học của bạn và sẽ liên hệ xác nhận trong thời gian sớm nhất. Cảm ơn bạn'
            html_content = '<h3 style="color:blue">Kính chào, <i>'+ cus.fullname +'</i></h3>'\
                        + '<h3>Chào mừng bạn đã đăng ký khoá học thành công tại <strong>Trung tâm nhật ngữ ABC</strong> website.</h3>' \
                        + '<h3>Lớp học đã đăng ký: ' + class_select.title + '</h3>' \
                        + '<h4 style="color:red">' + result + '</h4>'
        
            msg = EmailMultiAlternatives('Đăng ký thành công !', result, EMAIL_HOST_USER, [recepient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        context = {
            'subjects': subjects, 'courses': courses, 'class_select': class_select, 'students': students,
            'total_course': total_course, 'top_5_course': top_5_course, 'result': result,
            'form_newsletter': form_newsletter, 'username': username,
        }
        return render(request, 'courses/register.html', context=context)
    if request.method == 'POST':
        form_customer = FormCustomer(request.POST or None)
        if (form_customer.is_valid() and form_customer.cleaned_data['password'] == form_customer.cleaned_data['confirm']):
            fcustomer = form_customer.save(commit=False)
            fcustomer.username = form_customer.cleaned_data['username']
            fcustomer.password = form_customer.cleaned_data['password']
            fcustomer.confirm = form_customer.cleaned_data['confirm']
            fcustomer.email = form_customer.cleaned_data['email']
            fcustomer.fullname = form_customer.cleaned_data['fullname']
            fcustomer.phone = form_customer.cleaned_data['phone']
            fcustomer.address = form_customer.cleaned_data['address']
            fcustomer.save()
            CustomerItem.objects.create(customer=fcustomer, reg_class=class_select)
            # Gửi Email
            recepient = str(fcustomer.email)
            result = 'Chúng tôi đã nhận thông tin đăng ký khoá học của bạn và sẽ liên hệ xác nhận trong thời gian sớm nhất. Cảm ơn bạn'
            html_content = '<h3 style="color:blue">Kính chào, <i>'+ fcustomer.fullname +'</i></h3>'\
                        + '<h3>Chào mừng bạn đã đăng ký khoá học thành công tại <strong>Trung tâm nhật ngữ ABC</strong> website.</h3>' \
                        + '<h3>Lớp học đã đăng ký: ' + class_select.title + '</h3>' \
                        + '<h4 style="color:red">' + result + '</h4>'
        
            msg = EmailMultiAlternatives('Đăng ký thành công !', result, EMAIL_HOST_USER, [recepient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            context = {
                'subjects': subjects, 'courses': courses, 'class_select': class_select, 
                'students': students, 'total_course': total_course,  'top_5_course': top_5_course,
                'result': result, 'form_newsletter': form_newsletter, 'username': username,
            }
            return render(request, 'courses/register.html', context=context)
        if form_customer.cleaned_data['password'] != form_customer.cleaned_data['confirm']:
            form_customer.add_error('confirm', 'Mật khẩu và Xác nhận lại mật khẩu không giống nhau!')
            print(form_customer.errors)
    else:
        form_customer = FormCustomer()
        context = {
                    'subjects': subjects, 'courses': courses, 'class_select': class_select, 'students': students,
                    'total_course': total_course, 'top_5_course': top_5_course,'form_customer': form_customer,
                    'form_newsletter': form_newsletter,'username': username,
                }
        return render(request, 'courses/register.html', context=context)

def dang_nhap(request):
    subjects = Subject.objects.all()
    courses = Course.objects.all()
    classes = Class.objects.all()
    total_course = len(courses)
    top_5_course = Course.objects.all().order_by('-created')[:5]

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = Customer.objects.filter(username=username, password=password)
        if user:
            result = "Xin chào quý khách " + username
            request.session['username'] = username
            username = request.session.get('username', 0)
            return redirect('/tai-khoan/thong-tin-ca-nhan')
        else:
            print("You can't login.")
            print("Username: {} and password: {}".format(username, password))
            login_result = "Username hoặc password không chính xác!"
            context = {
                'subjects': subjects, 'courses': courses, 'classes': classes, 
                'total_course': total_course, 'top_5_course': top_5_course, 'login_result': login_result,
            }
            return render(request, "courses/login.html", context=context)
    context = {
        'subjects': subjects, 'courses': courses, 'classes': classes, 
        'total_course': total_course, 'top_5_course': top_5_course,
    }
    return render(request, 'courses/login.html', context=context)

def tai_khoan(request):
    subjects = Subject.objects.all()
    courses = Course.objects.all()
    classes = Class.objects.all()
    total_course = len(courses)
    top_5_course = Course.objects.all().order_by('-created')[:5]

    username = request.session.get('username', 0)
    customer_qs = Customer.objects.get(username=username)

    context = {
        'subjects': subjects, 'courses': courses, 'classes': classes, 
        'total_course': total_course, 'top_5_course': top_5_course,
        'username': username, 'customer_qs': customer_qs,
    }
    return render(request, 'courses/tai-khoan.html', context=context)

def lop_hoc_cua_toi(request):
    subjects = Subject.objects.all()
    courses = Course.objects.all()
    classes = Class.objects.all()
    total_course = len(courses)
    top_5_course = Course.objects.all().order_by('-created')[:5]

    username = request.session.get('username', 0)
    customer_qs = Customer.objects.get(username=username)
    customer_item = CustomerItem.objects.filter(customer=customer_qs)
    cancel_qs = None
    qs = Cancel.objects.filter(customer=customer_qs)
    if qs.exists():
        cancel_qs = Cancel.objects.filter(customer=customer_qs)
    deadline = datetime.date.today() + datetime.timedelta(7)
    now = datetime.date.today()

    context = {
        'subjects': subjects, 'courses': courses, 'classes': classes, 
        'total_course': total_course, 'top_5_course': top_5_course,
        'username': username,
        'deadline': deadline, 'now': now,
        'customer_qs': customer_qs, 'customer_item': customer_item, 'cancel_qs': cancel_qs,
    }
    return render(request, 'courses/lop-hoc-cua-toi.html', context=context)

def huy_dang_ky(request, slug):
    subjects = Subject.objects.all()
    courses = Course.objects.all()
    classes = Class.objects.all()
    total_course = len(courses)
    top_5_course = Course.objects.all().order_by('-created')[:5]
    class_select = Class.objects.get(slug=slug)
    username = request.session.get('username', 0)
    customer_qs = Customer.objects.get(username=username)
    result = ''
    if request.method == 'POST':
        form_cancel = FormCancel(request.POST or None)
        if form_cancel.is_valid():
            cancel = form_cancel.save(commit=False)
            cancel.customer = customer_qs
            cancel.reg_class = class_select
            cancel.reason = form_cancel.cleaned_data['reason']
            cancel.save()
            result = 'Bạn đã đăng ký huỷ khoá học! Trung tâm sẽ liên hệ xác nhận với bạn trong thời gian sớm nhất. Xin cám ơn!'
            html_content = '<h3 style="color:blue">Kính chào, <i>'+ customer_qs.fullname +'</i></h3>'\
                            + '<h3>Chào mừng bạn đến với website <strong>Trung tâm nhật ngữ ABC</strong>.</h3>' \
                            + '<h3>Lớp học đã huỷ đăng ký: ' + class_select.title + '</h3>' \
                            + '<h4 style="color:red">' + result + '</h4>'
            
            msg = EmailMultiAlternatives('Đăng ký huỷ lớp học! | Trung tâm ngoại ngữ ABC', result, EMAIL_HOST_USER, [customer_qs.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            context = {
                'subjects': subjects, 'courses': courses, 'classes': classes, 
                'total_course': total_course, 'top_5_course': top_5_course, 'class_select': class_select,
                'username': username, 'result': result,
                'form_cancel' : form_cancel, 'customer_qs': customer_qs, 
            }
            return render(request, 'courses/huy-dang-ky.html', context=context)
    else: 
        form_cancel = FormCancel()
        context = {
            'subjects': subjects, 'courses': courses, 'classes': classes, 
            'total_course': total_course, 'top_5_course': top_5_course, 'class_select': class_select,
            'username': username, 'form_cancel' : form_cancel, 'customer_qs': customer_qs, 
        }
        return render(request, 'courses/huy-dang-ky.html', context=context)

@login_required
def dang_xuat(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    logout = "Quý khách đã logout. Quý khách có thể login trở lại"
    return render(request, "courses/login.html", {'logout': logout})
    # logout(request)
    # result = "Quý khách đã logout. Quý khách có thể login trở lại"
    # # return render(request, "courses/index.html", {'logout_result': result})
    # return redirect('/')

def chu_de(request, slug):
    subjects = Subject.objects.all()
    subject_select = Subject.objects.filter(slug=slug)
    courses = Course.objects.all()
    classes = Class.objects.all()
    total_course = len(courses)
    top_5_course = Course.objects.all().order_by('-created')[:5]
    form_newsletter = FormNewsletter()
    username = request.session.get('username', 0)

    context = {
        'subjects': subjects, 'subject_select': subject_select, 'courses': courses, 'classes': classes, 
        'total_course': total_course, 'top_5_course': top_5_course,
        'form_newsletter': form_newsletter, 'username': username,
    }
    return render(request, 'courses/chu-de.html', context=context)

def khoa_hoc(request):
    subjects = Subject.objects.all()
    courses = Course.objects.all()
    classes = Class.objects.all()
    total_course = len(courses)
    top_5_course = Course.objects.all().order_by('-created')[:5]
    form_newsletter = FormNewsletter()
    username = request.session.get('username', 0)

    context = {
        'subjects': subjects, 'courses': courses, 'classes': classes, 
        'total_course': total_course, 'top_5_course': top_5_course,
        'form_newsletter': form_newsletter, 'username': username,
    }
    return render(request, 'courses/khoa-hoc.html', context=context)

def search_form(request):
    username = request.session.get('username', 0)

    subjects = Subject.objects.all()
    courses = Course.objects.all()
    classes = Class.objects.all()
    total_course = len(courses)
    top_5_course = Course.objects.all().order_by('-created')[:5]
    global search_str
    if request.method == 'GET':
        form = forms.FormSearch(request.GET, Course)

        if form.is_valid():
            search_str = form.cleaned_data['title']
            courses = Course.objects.filter(title__icontains=search_str)
            if courses:
                return render(request, "courses/khoa-hoc.html",
                        { 'subjects': subjects, 'courses': courses, 'classes': classes, 
                            'total_course': total_course, 'top_5_course': top_5_course,
                            'search_str': search_str, 'username': username,
                        })
            else:
                search_str2 = search_str.replace(" ","-")
                courses = Course.objects.filter(slug__icontains=search_str2)
                return render(request, "courses/khoa-hoc.html",
                    { 'subjects': subjects, 'courses': courses, 'classes': classes, 
                        'total_course': total_course, 'top_5_course': top_5_course,
                        'search_str': search_str, 'username': username,
                    })

        return render(request, "courses/khoa-hoc.html",
                    { 'subjects': subjects, 'courses': courses, 'classes': classes, 
                        'total_course': total_course, 'top_5_course': top_5_course,
                        'search_str': search_str, 'username': username,
                    })

def dang_ky_tin_moi(request):
    username = request.session.get('username', 0)

    subjects = Subject.objects.all()
    courses = Course.objects.all()
    classes = Class.objects.all()
    total_course = len(courses)
    top_5_course = Course.objects.all().order_by('-created')[:5]
    result_news = ''
    print(result_news)
    if request.method == 'POST':
        form_newsletter = FormNewsletter(request.POST or None)
        if form_newsletter.is_valid():
            fnewsletter = form_newsletter.save(commit=False)
            email = form_newsletter.cleaned_data['email']
            email_qs = Newsletter.objects.filter(email=email)
            if email_qs.exists():
                result_news = '<h5 style="color:blue">Email này đã đăng ký rồi.</h5>'
            else:
                fnewsletter.save()
                #Gửi Email
                result_news = '<h5 style="color:blue">Bạn đã đăng ký tin mới thành công. Chúc bạn một ngày tốt lành. Xin cám ơn</h5>'
                recepient = str(email)
                msg = EmailMultiAlternatives('Đăng ký tin mới thành công !', result_news, EMAIL_HOST_USER, [recepient])
                msg.attach_alternative(result_news, "text/html")
                msg.send()
            context = {
                'subjects': subjects, 'courses': courses, 'classes': classes, 
                'total_course': total_course, 'top_5_course': top_5_course,
                'result_news': result_news,'form_newsletter': form_newsletter,
                'username': username,
            }
            return render(request, 'courses/index.html', context=context)
    else:
        form_newsletter = FormNewsletter()
    
        context = {
                'subjects': subjects, 'courses': courses, 'classes': classes, 
                'total_course': total_course, 'top_5_course': top_5_course,
                'result_news': result_news, 'form_newsletter': form_newsletter,
                'username': username,
            }
        return render(request, 'courses/index.html', context=context)

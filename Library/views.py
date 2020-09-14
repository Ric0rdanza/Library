from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators import csrf
from database.models import Reader, Book, Borrow, Order, Comment, Wishlist, ViewBorrowlistWithStatus, ViewOrderlistWithStatus, ViewWishlistWithStock
from math import ceil
import datetime
import pytz

def index(request):
    context = {}
    status = request.session.get('is_login')
    if not status:
        context["status"] = None
    else:
        context["status"] = status
    return render(request, 'index.html', context)

def login_page(request):
    context = {}
    status = request.session.get('is_login')
    if not status:
        return render(request, 'login.html', context)
    else:
        return HttpResponse("<script>alert('您已登录');window.location.href='/index';</script>")

def login(request):
    status = request.session.get('is_login')
    if not status and request.POST:
        username = request.POST['username']
        password = request.POST['password']
        readerobject = Reader.objects.filter(username = username).first()
        if password == readerobject.password:
            request.session['is_login'] = True
            request.session['username'] = username
            return HttpResponse("<script>alert('已登录'); window.location.href='/index';</script>")
        else:
            return HttpResponse("<script>alert('密码错误请重试'); window.location.href='/login';</script>")
    else:
        HttpResponse("<script>alert('请求错误'); window.location.href='/login';</script>")

def register_page(request):
    context = {}
    status = request.session.get('is_login')
    if not status:
        return render(request, 'register.html', context)
    else:
        return HttpResponse("<script>alert('您已登录');window.location.href='/index';</script>")

def register(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        nickname = request.POST['nickname']
        address = request.POST['address']
        contact = request.POST['tel']
        reader = Reader(username = username, password = password, nickname = nickname, address = address, contact = contact, is_manager = False)
        reader.save()
        return HttpResponse("<script>alert('创建账户成功'); window.location.href='/login';</script>")
    else:
        return HttpResponse("<script>alert('请求错误'); window.location.href='/register';</script>")

def logout(request):
    status = request.session.get('is_login')
    if not status:
        return HttpResponse("<script>alert('请求错误'); window.location.href='/index';</script>")
    else:
        request.session.flush()
        return HttpResponse("<script>alert('已退出账号'); window.location.href='/index';</script>")

def detail(request, serial):
    context = {}
    status = request.session.get('is_login')
    if not status:
        context['status'] = None
    else:
        context['status'] = status
    book_object = Book.objects.filter(serial = serial).first()
    context['book'] = book_object
    return render(request, 'detail.html', context)

def myaccount(request, username):
    context = {}
    status = request.session.get('is_login')
    if not status:
        return HttpResponse("<script>alert('请先登录');window.location.href='/login';</script>")
    #ACCESS
    context['status'] = status
    reader_object = Reader.objects.filter(username = request.session['username']).first()
    context['account'] = reader_object
    #Search username
    return render(request, 'myaccount.html', context)

def modify_account(request):
    if not request.POST:
        return HttpResponse("<script>alert('请求错误'); window.location.href='/account';</script>")
    if not request.session.get('is_login'):
        return HttpResponse("<script>alert('请先登录');window.location.href='/login';</script>")
    username = request.session['username']
    nickname = request.POST['nickname']
    address = request.POST['address']
    contact = request.POST['tel']
    Reader.objects.filter(username = username).update(nickname = nickname, address = address, contact = contact)
    return HttpResponse("<script>alert('修改完成');window.location.href='/myaccount';</script>")

def changepassword(request):
    status = request.session.get('is_login')
    if not status:
        return HttpResponse("<script>alert('请先登录');window.location.href='/login';</script>")
    context = {}
    context['status'] = status
    return render(request, "newpassword.html", context)

def new_password(request):
    if not request.session.get('is_login'):
        return HttpResponse("<script>alert('请先登录');window.location.href='/login';</script>")
    old = request.POST['oldpassword']
    reader_object = Reader.objects.filter(username = request.session['username'])
    if reader_object.first().password == old:
        new = request.POST['newpassword']
        reader_object.update(password = new)
        return HttpResponse("<script>alert('修改完成');window.location.href='/myaccount';</script>")
    else:
        return HttpResponse("<script>alert('密码错误');window.location.href='/changepassword';</script>")


def searchbook(request, page):
    context = {}
    status = request.session.get('is_login')
    context['status'] = status
    if request.POST.get('keyword') and request.POST["keyword"] != '':
        keyword = request.POST.get('keyword')
        booklist = Book.objects.filter(bookname__icontains=keyword).values_list('serial', 'bookname', 'author', 'publisher')
    else:
        booklist = Book.objects.all().values_list('serial', 'bookname', 'author', 'publisher')
    totalpage = ceil(len(booklist) / 12)
    if not page:
        page = 1
        context['page'] = '1'
    elif int(page) < 1:
        return redirect('/search/1')
    elif int(page) > totalpage:
        return redirect('/search/' + str(totalpage))
    else:
        context['page'] = page
    context['booklist'] = booklist[(int(page) - 1) * 12: (int(page) - 1) * 12 + 12]
    context['totalpage'] = totalpage
    context['prevpage'] = int(page) - 1
    context['nextpage'] = int(page) + 1
    return render(request, 'search.html', context)

def addwishlist(request, serial):
    status = request.session.get('is_login')
    if not status:
        return HttpResponse("<script>alert('请先登录');window.location.href='/login';</script>")
    reader_object = Reader.objects.filter(username = request.session['username']).first()
    book_object = Book.objects.filter(serial = serial).first()
    wish_exist = Wishlist.objects.filter(readerid = reader_object).filter(bookid = book_object).exists()
    if wish_exist:
        return HttpResponse("<script>alert('该书已在愿望单中'); window.location.href='" + request.META['HTTP_REFERER'] + "';</script>")
    else:
        wishlist_object = Wishlist(readerid=reader_object, bookid=book_object, date=datetime.datetime.now(tz = pytz.timezone('UTC')))
        wishlist_object.save()
        return redirect(request.META['HTTP_REFERER'])

def viewwishlist(request):
    context = {}
    status = request.session.get('is_login')
    if not status:
        return HttpResponse("<script>alert('请先登录');window.location.href='/login';</script>")
    context['status'] = status
    wishlist_object = ViewWishlistWithStock.objects.filter(username = request.session['username']).all()
    if not wishlist_object:
        context['empty'] = True
    else:
        context['wishlist'] = wishlist_object
    return render(request, 'booklist.html', context)

def removewishlist(request, serial):
    status = request.session.get('is_login')
    if not status:
        return HttpResponse("<script>alert('请先登录');window.location.href='/login';</script>")
    reader_object = Reader.objects.filter(username = request.session['username']).first()
    book_object = Book.objects.filter(serial = serial).first()
    Wishlist.objects.filter(readerid = reader_object).filter(bookid = book_object).first().delete()
    return redirect("/wishlist/")

def vieworderlist(request):
    context = {}
    status = request.session.get('is_login')
    if not status:
        return HttpResponse("<script>alert('请先登录');window.location.href='/login';</script>")
    context['status'] = status
    orderlist_object = ViewOrderlistWithStatus.objects.filter(username = request.session['username']).first()
    if not orderlist_object == 0:
        context['empty'] = True
    else:
        context['orderlist'] = orderlist_object
    return render(request, 'orderlist.html', context)

def addorderlist(request, serial):
    status = request.session.get('is_login')
    if not status:
        return HttpResponse("<script>alert('请先登录');window.location.href='/login';</script>")
    reader_object = Reader.objects.filter(username = request.session['username']).first()
    book_object = Book.objects.filter(serial = serial).first()
    order_exist = Order.objects.filter(readerid = reader_object).filter(bookid = book_object).exists()
    if order_exist:
        return HttpResponse("<script>alert('已经预约该书'); window.location.href='" + request.META['HTTP_REFERER'] + "';</script>")
    else:
        orderlist_object = Order(readerid = reader_object, bookid = book_object, status = 0, date = datetime.datetime.now(tz = pytz.timezone('UTC')))
        orderlist_object.save()
        return HttpResponse("<script>alert('预约成功'); window.location.href='" + request.META['HTTP_REFERER'] + "';</script>")

def removeorderlist(request, serial):
    status = request.session.get('is_login')
    if not status:
        return HttpResponse("<script>alert('请先登录');window.location.href='/login';</script>")
    reader_object = Reader.objects.filter(username = request.session['username']).first()
    book_object = Book.objects.filter(serial = serial).first()
    Order.objects.filter(readerid = reader_object).filter(bookid = book_object).delete()
    return redirect('/orderlist/')

def viewborrowlist(request):
    context = {}
    status = request.session.get('is_login')
    if not status:
        return HttpResponse("<script>alert('请先登录');window.location.href='/login';</script>")
    context['status'] = status
    borrowlist_object = ViewBorrowlistWithStatus.objects.filter(username = request.session['username']).filter(status__lte = 1).all().order_by('date')
    if len(borrowlist_object) == 0:
        context['empty'] = True
    else:
        context['borrowlist'] = borrowlist_object
    return render(request, 'borrowlist.html', context)

def addborrowlist(request, serial):
    status = request.session.get('is_login')
    if not status:
        return HttpResponse("<script>alert('请先登录');window.location.href='/login';</script>")
    reader_object = Reader.objects.filter(username = request.session['username']).first()
    book_object = Book.objects.filter(serial = serial).first()
    borrow_exist = Borrow.objects.filter(readerid = reader_object).filter(bookid = book_object).exists()
    if borrow_exist:
        return HttpResponse("<script>alert('已经借过该书'); window.location.href='" + request.META['HTTP_REFERER'] + "';</script>")
    elif book_object.stock == 0:
        return HttpResponse("<script>alert('该书没有库存，请预约'); window.location.href='" + request.META['HTTP_REFERER'] + "';</script>")
    else:
        borrowlist_object = Borrow(readerid = reader_object, bookid = book_object, status = 0, date = datetime.datetime.now(tz = pytz.timezone('UTC')))
        borrowlist_object.save()
        Book.objects.filter(serial = serial).update(stock = book_object.stock - 1)
        return HttpResponse("<script>alert('借阅成功'); window.location.href='" + request.META['HTTP_REFERER'] + "';</script>")

def borrowrecord(request):
    context = {}
    status = request.session.get('is_login')
    if not status:
        return HttpResponse("<script>alert('请先登录');window.location.href='/login';</script>")
    context['status'] = status
    borrow_record = ViewBorrowlistWithStatus.objects.filter(username = request.session['username']).all().order_by('date')
    if not borrow_record:
        context['empty'] = True
    else:
        context['record'] = borrow_record
    return render(request, 'allrecord.html', context)
    
def readerreturn(request, serial):
    status = request.session.get('is_login')
    if not status:
        return HttpResponse("<script>alert('请先登录');window.location.href='/login';</script>")
    reader_object = Reader.objects.filter(username = request.session['username']).first()
    book_object = Book.objects.filter(serial = serial).first()
    borrow_record = Borrow.objects.filter(readerid = reader_object.id).filter(bookid = book_object.id)
    if borrow_record.first().status == 0:
        borrow_record.update(status = borrow_record.first().status + 1)
    else:
        return HttpResponse(("<script>alert('请求错误'); window.location.href='" + request.META['HTTP_REFERER'] + "';</script>"))
    return HttpResponse(("<script>alert('已提交'); window.location.href='" + request.META['HTTP_REFERER'] + "';</script>"))

def manager_newbook(request):
    context = {}
    return render(request, 'managernewbook.html', context)

def newbook_action(request):
    if request.POST:
        serial = request.POST['serial']
        name = request.POST['name']
        author = request.POST['author']
        publisher = request.POST['publisher']
        quantity = request.POST['quantity']
        description = request.POST['description']
        NBook = Book(serial = serial, bookname = name, author = author, publisher = publisher, stock = quantity, description = description)
        NBook.save()
        return HttpResponse("<script>alert('添加成功'); window.location.href='/newbook';</script>")
    else:
        return HttpResponse("<script>alert('请求错误'); window.location.href='/newbook';</script>")

def manager_check(request):
    context = {}
    pending_check = ViewBorrowlistWithStatus.objects.filter(status = 1).all()
    if not pending_check:
        context['empty'] = True
    else:
        context['checklist'] = pending_check
    return render(request, 'managereturn.html', context)

def check_action(request, serial, username):
    reader_object = Reader.objects.filter(username = username).first()
    book_object = Book.objects.filter(serial = serial).first()
    borrow_record = Borrow.objects.filter(readerid = reader_object.id).filter(bookid = book_object.id)
    if borrow_record.first().status == 1:
        borrow_record.update(status = borrow_record.first().status + 1)
        book_object.stock += 1
        book_object.save()
    else:
        return HttpResponse(("<script>alert('请求错误'); window.location.href='" + request.META['HTTP_REFERER'] + "';</script>"))
    return HttpResponse(("<script>alert('确认成功'); window.location.href='" + request.META['HTTP_REFERER'] + "';</script>"))
from django.db import models

# Create your models here.
class Reader(models.Model):
    objects = models.Manager()
    username = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    nickname = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    is_manager = models.BooleanField()
    wishlist = models.ManyToManyField(to='Book', through='Wishlist', through_fields=('readerid', 'bookid'), related_name='wishlist_reader')
    comment = models.ManyToManyField(to='Book', through='Comment', through_fields=('readerid', 'bookid'), related_name='comment_reader')
    order = models.ManyToManyField(to='Book', through='Order', through_fields=('readerid', 'bookid'), related_name='order_reader')
    borrow = models.ManyToManyField(to='Book', through='Borrow', through_fields=('readerid', 'bookid'), related_name='borrow_reader')

class Book(models.Model):
    objects = models.Manager()
    serial = models.CharField(max_length=128, unique=True)
    bookname = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    publisher = models.CharField(max_length=30)
    stock = models.IntegerField()
    description = models.TextField(max_length=200)
    wishlist = models.ManyToManyField(to='Reader', through='Wishlist', through_fields=('bookid', 'readerid'), related_name= 'wishilist_book')
    comment = models.ManyToManyField(to='Reader', through='Comment', through_fields=('bookid', 'readerid'), related_name='comment_book')
    order = models.ManyToManyField(to='Reader', through='Order', through_fields=('bookid', 'readerid'), related_name='order_book')
    borrow = models.ManyToManyField(to='Reader', through='Borrow', through_fields=('bookid', 'readerid'), related_name='borrow_book')

class Comment(models.Model):
    readerid = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='reader_comment')
    bookid = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_comment')
    comment = models.TextField(max_length=400)

class Order(models.Model):
    objects = models.Manager()
    readerid = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='reader_order')
    bookid = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_order')
    status = models.IntegerField()
    date = models.DateTimeField()

class Borrow(models.Model):
    objects = models.Manager()
    readerid = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='reader_borrow')
    bookid = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_borrow')
    status = models.IntegerField()
    date = models.DateTimeField()

class Wishlist(models.Model):
    objects = models.Manager()
    readerid = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name='reader_wishlist')
    bookid = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_wishlist')
    date = models.DateTimeField()

class ViewWishlistWithStock(models.Model):
    objects = models.Manager()
    serial = models.CharField(max_length=128)
    username = models.CharField(max_length = 254)
    bookname = models.CharField(max_length = 30)
    author = models.CharField(max_length = 30)
    publisher = models.CharField(max_length = 30)
    stock = models.IntegerField()
    date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'view_wishlist_with_stock'
    

class ViewOrderlistWithStatus(models.Model):
    objects = models.Manager()
    username = models.CharField(max_length = 254)
    bookname = models.CharField(max_length = 30)
    author = models.CharField(max_length = 30)
    publisher = models.CharField(max_length = 30)
    status = models.IntegerField()
    date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = "view_orderlist_with_status"

class ViewBorrowlistWithStatus(models.Model):
    objects = models.Manager()
    serial = models.CharField(max_length=128)
    username = models.CharField(max_length = 254)
    bookname = models.CharField(max_length = 30)
    author = models.CharField(max_length = 30)
    publisher = models.CharField(max_length = 30)
    status = models.IntegerField()
    date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = "view_borrowlist_with_status"
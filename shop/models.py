from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=250, verbose_name='Имя категории')
    description = models.TextField(max_length=2048, verbose_name='Описание', null=True)
    label = models.CharField(max_length=255, verbose_name='Примечание')
    image = models.ImageField(verbose_name='Изображение', null=True)
    featured = models.BooleanField(default=False, verbose_name='Показывать на главной странице')
    slug = models.SlugField(unique=True, verbose_name='Путь')

    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(max_length=2048, verbose_name='Описание', null=True)
    image = models.ImageField(verbose_name='Изображение', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена', null=True)
    old_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Старая цена', null=True)
    rating = models.PositiveIntegerField(default=0, verbose_name='Рейтинг')
    sale = models.BooleanField(default=False, verbose_name='Распродажа')
    featured = models.BooleanField(default=False, verbose_name='Показывать на главной странице')
    slug = models.SlugField(unique=True, verbose_name='Путь')
    #TODO: other props

    def __str__(self):
        return self.name + ' [' + self.slug + ']'


class Order(models.Model):

    session_key = models.CharField(max_length=32, verbose_name='Сессия')
    customer_name = models.CharField(max_length=128, verbose_name='Имя покупателя', null=True)
    customer_address = models.CharField(max_length=256, verbose_name='Адрес покупателя', null=True)
    customer_phone = models.CharField(max_length=16, verbose_name='Телефон покупателя', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена', null=True)
    finalized = models.BooleanField(default=False, verbose_name='Заказ завершён')
    date = models.DateTimeField(auto_now_add=False, null=True)
    content = models.TextField(max_length=4096, verbose_name='Состав заказа', null=True)

    def __str__(self):
        return 'Незавершённый заказ [' + self.session_key + ']' if self.finalized == False else self.customer_name + ' - ' + str(self.price) + ' - ' + self.date.strftime('%Y-%m-%d %H:%M')


class OrderProduct(models.Model):

    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена на момент покупки', null=True)

    def __str__(self):
        return "Продукт: {} (для заказа)".format(self.product.name if self.product != None else '[Удалённый продукт]')
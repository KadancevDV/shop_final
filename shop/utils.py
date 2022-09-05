from django.db.models import Sum
from .models import Category, Order, OrderProduct


class Utils():

    def getBaseContect(request):

        if request.session.session_key == None:
            request.session.set_test_cookie()

        cart = Order.objects.filter(session_key=request.session.session_key, finalized=False).first()
        qty = OrderProduct.objects.filter(order=cart).aggregate(Sum('qty'))['qty__sum']
        
        return {
            'categories': Category.objects.filter(),
            'cart_qty': qty if qty != None and qty > 0 else ''
        }
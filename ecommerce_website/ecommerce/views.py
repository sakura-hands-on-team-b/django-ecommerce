import datetime
from django.shortcuts import redirect, render, get_list_or_404, render_to_response
from ecommerce.models import *
from pprint import pprint

# Create your views here.

def index(request):
    """
    商品一覧画面(/ec/list/)が呼び出された際に呼び出されるビューです。
    商品情報を返します。
    """

    products = get_list_or_404(Product)

    #   セッションにカートの情報を格納するListを定義します。
    if not request.session.has_key('cart'):
        request.session['cart'] = list()
    cart = request.session['cart'];

    # 購入点数を再設定
    request.session['num'] = len(cart)
    response = render(request, 'product_list.html', {'products': products})

    return response

def cart_add(request, product_id):
    """
    カートに任意の商品を追加する場合に呼び出されるビューです。
    カート(セッション)に任意の商品の商品IDを追加します。
    """

    quantity = 0
    quantity = request.GET["quantity"]
    #   カート(セッション)に商品を追加します。
    if not request.session.has_key('cart'):
        request.session['cart'] = list()
    cart = request.session['cart']
    cart_set = {'product_id': product_id,'quantity': quantity}
    cart.append(cart_set)
    request.session['cart'] = cart

    products = get_list_or_404(Product)

    response = redirect('/ec/list/', {'products': products})

    return response

def cart_delete(request, product_id):
    """
    カートに入っている任意の商品を削除する場合に呼び出されるビューです。
    カート(セッション)から任意の商品の商品IDを削除します。
    """

    #   カート(セッション)から指定された商品を削除します。
    if not request.session.has_key('cart'):
        request.session['cart'] = list()
    cart = request.session['cart']
    #   同じ商品が複数listに入っていた場合に、指定されてIDのオブジェクトをすべて削除する
    cart = [item for item in cart if item is not str(product_id)]
    request.session['cart'] = cart

    products = get_list_or_404(Product)

    response = redirect('/ec/list/', {'products': products})

    return response


def cart_reset(request):
    """
    カートを空にするがクリックされた場合に実行されるビューです。
    カートの中身(セッション)を空にします。
    """

    #   カート(セッション)からすべての商品を削除します。
    if not request.session.has_key('cart'):
        request.session['cart'] = list()
    del request.session['cart']
    del request.session['num']
    products = get_list_or_404(Product)

    response = redirect('/ec/list/', {'products': products})

    return response

def cart_list(request):
    """
    カートの中身を表示するページが表示される場合に実行されるビューです。
    カートに入っている商品情報を返します。
    """

    #   カート(セッション)内にある商品IDを取得します。
    if not request.session.has_key('cart'):
        request.session['cart'] = list()
    cart = request.session['cart']

    #   カートに入っている商品の情報を取得します
    # products = Product.objects.filter(id__in=cart)
    products = list()
    total = 0
    if len(cart) > 0:
        for index in cart:
            product = Product.objects.get(id=index['product_id'])
            subtotal = int(product.price)*int(index['quantity'])
            total += subtotal
            cart_set = {'product_id': index['product_id'],'quantity': index['quantity'],'id': product.id,'name': product.name, 'price': product.price,'subtotal': subtotal }
            products.append(cart_set)

    # 金額合計
    return render(request, 'cart_list.html', {'products': products,'total': total})

def order(request):
    """
    注文画面が表示される場合に実行されるビューです。
    カートに入っている商品情報と決済方法と注文画面を返します。
    """

    #   カート(セッション)内にある商品IDを取得します。
    if not request.session.has_key('cart'):
        request.session['cart'] = list()
    cart = request.session['cart']
    products = list()
    total = 0
    if len(cart) > 0:
        for index in cart:
            product = Product.objects.get(id=index['product_id'])
            subtotal = int(product.price)*int(index['quantity'])
            print(subtotal)
            total += subtotal
            cart_set = {'product_id': index['product_id'],
                        'quantity': index['quantity'],
                        'id': product.id,'name': product.name,
                        'price': product.price,'subtotal': subtotal }
            products.append(cart_set)

    #   カートに入っている商品の情報を取得します
    # products = Product.objects.filter(id__in=cart)

    #   決済方法を取得します。
    payments = get_list_or_404(Payment)

    return render(request, 'order.html', {'products': products, 'payments': payments,'total': total})

def order_execute(request):
    """
    注文画面からPOSTされた際に実行されるビューです。
    お客様情報を保存し注文された商品情報を保存します。
    """

    #   送信されたお客様情報を保存します。
    customer = Customer(first_name=request.POST['first_name'],
                        last_name=request.POST['last_name'],
                        postal_code=request.POST['postal_code'],
                        prefecture=request.POST['prefecture'],
                        city=request.POST['city'],
                        street1=request.POST['street1'],
                        street2 =request.POST['street2'],
                        tel=request.POST['tel'],
                        email=request.POST['email'])
    customer.save()

    #   Paymentオブジェクトを取得します。
    payment = Payment.objects.get(id=int(request.POST['payment']))

    #   注文情報を保存します。
    order = Order(customer=customer, payment=payment)
    order.save()
    request.session['order_id'] = order.id;
    #   カート(セッション)内にある商品IDを取得します。
    if not request.session.has_key('cart'):
        request.session['cart'] = list()
    cart = request.session['cart']
    products = {}
    if len(cart) > 0:
        for index in cart:
            # カートの中で重複はまとめる
            product = Product.objects.get(id=index['product_id'])
            subtotal = int(product.price)*int(index['quantity'])
            print(subtotal)
            if len(products) > 0:
                # pprint(products)
                # if products.has_key('product_id_' + index['product_id']):
                target = 'product_id_' + index['product_id']
                if target in products:
                    # pair = products[target]
                    # count = pair['count']
                    # price = pair['price']
                    products[target]['count'] = int(products[target]['count']) + int(index['quantity'])
                    products[target]['price'] = int(products[target]['price']) + int(subtotal)
                else:
                    products[target] = {'count':0,'price': 0}
                    products[target]['count'] = index['quantity']
                    products[target]['price'] = subtotal
                    products[target]['product_id'] = index['product_id']
            else:
                products['product_id_' + index['product_id']] = {'count':0,'price': 0}
                products['product_id_' + index['product_id']]['count'] = index['quantity']
                products['product_id_' + index['product_id']]['price'] = subtotal
                products['product_id_' + index['product_id']]['product_id'] = index['product_id']

    pprint(products)
    #   カートに入っている商品の情報を取得します
    # products = Product.objects.filter(id__in=cart)

    for key,product in products.items():
        # order_product = Order_Product(order=order, product=product, count=1, price=product.price)
        # p = Product.objects.get(id=product['product_id'])
        p = Product.objects.get(id=product['product_id'])
        order_product = Order_Product(order=order, product=p, count=product['count'], price=product['price'])
        order_product.save()

    #   注文完了画面にリダイレクトします。
    return redirect('/ec/order_complete/')

def order_complete(request):
    """
    注文完了時に実行されるビューです。
    注文完了画面を返します。
    """

    response = render_to_response('order_complete.html',{'order_id':request.session['order_id']})

    #   カートの中身を削除します
    if request.session.has_key('cart'):
        del request.session['cart']
    if request.session.has_key('order_id'):
        del request.session['order_id']
    return response

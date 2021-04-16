from django.shortcuts import render
from django.http import HttpResponse
from users.models import Driver, PointHist
from users.models import Sponsor, DriverOrder
from users.models import GenericAdmin
from users.models import GenericUser
from users.models import Application
from users.models import Sponsorship
from users.models import Product
from django.shortcuts import redirect
from django.contrib.auth.models import User
import requests
from html import unescape
import time


# from portal.models import UserLogin

def driverGet(user):
    gUser = GenericUser.objects.get(username=user.username)
    if (gUser.type == 'Driver'):
        return Driver.objects.get(username=user.username)
    elif (gUser.type == 'Sponsor'):
        return Driver.objects.get(username=Sponsor.objects.get(username=user.username).driver_vicarious)


# send user to homepage
def home(request):
    user = request.user
    gUser = GenericUser.objects.get(username=user.username)
    userType = gUser.type
    if userType == 'Driver':
        response = redirect('driver-home')
    elif userType == 'Sponsor':
        response = redirect('sponsor-home')
    elif userType == 'Admin':
        response = redirect('admin-home')
    else:
        response = redirect('logout')
    # # log login attempt
    # login_attempt = UserLogin(
    # 	username = user.username,
    # 	date= "Today",
    # 	success = "true"
    # )
    # login_attempt.save()
    return response


# return render(request, 'portal/home.html')

def portal_home(request):
    return render(request, 'portal/home.html')


def register(request):
    return render(request, 'portal/register.html')


def driver_home(request):
    # send driver info to page
    user = request.user
    gUser = GenericUser.objects.get(username=user.username)
    userType = gUser.type
    if userType == 'Sponsor':
        print('Driver name is: \''+Sponsor.objects.get(username=user.username).driver_vicarious+'\'')
    if userType == 'Sponsor' and not Driver.objects.filter(username=Sponsor.objects.get(username=user.username).driver_vicarious).exists():
        return redirect('select-driver')
    driver = driverGet(user)
    # send point history to page
    try:
        if userType == 'Sponsor':
            point_hist = PointHist.objects.filter(username=driver.username,sponsor_company=Sponsor.objects.get(username=user.username).sponsor_company)
        else:
            point_hist = PointHist.objects.filter(username=driver.username)
    except PointHist.DoesNotExist:
        point_hist = None
    # send application data to page
    try:
        if userType == 'Sponsor':
            applications = Application.objects.filter(driver=driver.username,sponsor_company=Sponsor.objects.get(username=user.username).sponsor_company)
        else:
            applications = Application.objects.filter(driver=driver.username)
    except Application.DoesNotExist:
        applications = None
    # get sponsors and point totals
    try:
        if userType == 'Sponsor':
            sponsor_list = Sponsorship.objects.filter(driver=driver.username,sponsor_company=Sponsor.objects.get(username=user.username).sponsor_company)
        else:
            sponsor_list = Sponsorship.objects.filter(driver=driver.username)
    except Sponsorship.DoesNotExist:
        sponsor_list = None
    data = {
        'points': driver.points,
        'point_hist': point_hist,
        'first_name': driver.first_name,
        'last_name': driver.last_name,
        'phone_num': driver.phone_num,
        'address': driver.address,
        'profile_photo': driver.profile_photo.url,
        'applications': applications,
        'sponsor': driver.sponsor,
        'sponsor_list': sponsor_list,
        'realDriver': (userType == 'Driver'),

    }

    return render(request, 'portal/driver_home.html', data)


def sponsor_home(request):
    # Assign the sponsor user data to the user var
    user = request.user
    # Get the sponsor username
    sponsor = Sponsor.objects.get(username=user.username)
    sponsor_company = Sponsor.objects.get(username=request.user.username).sponsor_company
    try:
        my_drivers = Sponsorship.objects.filter(sponsor_company=sponsor_company)
    except Driver.DoesNotExist:
        my_drivers = None
    # get applications
    try:
        applications = Application.objects.filter(sponsor_company=sponsor_company)
    except Application.DoesNotExist:
        applications = None

    data = {
        'first_name': sponsor.first_name,
        'last_name': sponsor.last_name,
        'phone_num': sponsor.phone_num,
        'address': sponsor.address,
        'email': sponsor.email,
        # Get rid of this variable, later.
        'sponsor_company': sponsor.sponsor_company,
        # This will access all of the drivers assigned to the sponsors.
        'my_drivers': my_drivers,
        'applications': applications
    }
    return render(request, 'portal/sponsor_home.html', data)


def admin_home(request):
    return render(request, 'admin/')


def catalog_sponsor(request):
    # Assign the sponsor user data to the user var
    user = request.user
    # Get the sponsor username
    user = request.user
    gUser = GenericUser.objects.get(username=user.username)
    userType = gUser.type
    if userType == 'Sponsor':
        sponsor = Sponsor.objects.get(username=user.username)
        prodID = ''
        prodID = request.POST.get('product-chosen')
        if prodID != '' and prodID != None:
            print('Product ID received!')
            if Product.objects.filter(sponsor_company=sponsor.sponsor_company, idNum=prodID).exists():
                newProduct = Product.objects.filter(sponsor_company=sponsor.sponsor_company, idNum=prodID).delete()
        listed_products = Product.objects.filter(sponsor_company=sponsor.sponsor_company)
        parse1 = []
        tally = 0
        for item in listed_products:
            parse1.append(requests.get(
                'https://openapi.etsy.com/v2/listings/' + str(item.idNum) + '?api_key=pmewf48x56vb387qgsprzzry').json()[
                              'results'][0])
            tally += 1
            if tally > 8:
                time.sleep(1)
                tally = 0
        tally = 0
        parse3 = parse1
        tags = "tags: "
        for x in parse3:
            x['title'] = unescape(x['title'])
            x['description'] = unescape(x['description'])
            x['image'] = requests.get('https://openapi.etsy.com/v2/listings/' + str(
                x['listing_id']) + '/images?api_key=pmewf48x56vb387qgsprzzry').json()['results'][0]['url_170x135']
            tally += 1
            if tally > 8:
                time.sleep(1)
                tally = 0
            if len(x['title']) > 50:
                x['title'] = x['title'][0:49] + '...'
            if len(x['description']) > 250:
                x['description'] = x['description'][0:249] + '...'
        data = {
            'sponsor_company': sponsor.sponsor_company,
            'items': parse3
        }
        response = render(request, 'portal/catalog_sponsor.html', data)
    else:
        response = redirect('home')
    return response


def sponsor_list(request):
    # Assign the sponsor user data to the user var
    user = request.user
    # Get the sponsor username
    gUser = GenericUser.objects.get(username=user.username)
    userType = gUser.type
    print('user retrieved')
    if userType == 'Sponsor':
        sponsor = Sponsor.objects.get(username=user.username)
        search = sponsor.list_last_search
        search = request.POST.get('search')
        prodID = ''
        prodID = request.POST.get('product-chosen')
        if search != sponsor.list_last_search and search != None:
            sponsor.list_last_search = search
            sponsor.save()
        if prodID != '' and prodID != None:
            if Product.objects.filter(sponsor_company=sponsor.sponsor_company, idNum=prodID).exists() == False:
                newProduct = Product.objects.create(sponsor_company=sponsor.sponsor_company, idNum=prodID,
                                                    priceRaw=float(requests.get(
                                                        'https://openapi.etsy.com/v2/listings/' + prodID + '?api_key=pmewf48x56vb387qgsprzzry').json()[
                                                                       'results'][0]['price']))
        # This is a failsafe in case the database isn't cooperating with older users.
        if sponsor.list_last_search == '':
            sponsor.list_last_search = 'candle'
            sponsor.save()
        response = requests.get(
            'https://openapi.etsy.com/v2/listings/active?keywords=' + sponsor.list_last_search + '&api_key=pmewf48x56vb387qgsprzzry')
        parse1 = response.json()['results']
        tally = 0;
        for x in parse1:
            x['title'] = unescape(x['title'])
            x['description'] = unescape(x['description'])
            x['image'] = requests.get('https://openapi.etsy.com/v2/listings/' + str(
                x['listing_id']) + '/images?api_key=pmewf48x56vb387qgsprzzry').json()['results'][0]['url_170x135']
            tally += 1
            if tally > 8:
                time.sleep(1)
                tally = 0
            if len(x['title']) > 50:
                x['title'] = x['title'][0:49] + '...'
            if len(x['description']) > 250:
                x['description'] = x['description'][0:249] + '...'
        tally = 0
        data = {
            'items': parse1,
            'searchVal': sponsor.list_last_search
        }
        response = render(request, 'portal/sponsor_list_item.html', data)
    else:
        response = redirect('home')
    return response


def select_driver(request):
    # Assign the sponsor user data to the user var
    user = request.user
    # Get the sponsor username
    user = request.user
    gUser = GenericUser.objects.get(username=user.username)
    userType = gUser.type
    if userType == 'Sponsor':
        sponsor = Sponsor.objects.get(username=user.username)
        driverUsername = ''
        driverUsername = request.POST.get('driver-username')
        if driverUsername != '' and driverUsername != None:
            sponsor.driver_vicarious = driverUsername
            sponsor.save()
        sponsorships = Sponsorship.objects.filter(sponsor_company=sponsor.sponsor_company)
        drivers = []
        for sponsorship in sponsorships:
            driversReturned = Driver.objects.filter(username=sponsorship.driver)
            for driver in driversReturned:
                drivers.append(driver)

        data = {
            'sponsor_company': sponsor.sponsor_company,
            'drivers': drivers,
            'current_driver': sponsor.driver_vicarious
        }
        response = render(request, 'portal/sponsor_select_driver.html', data)
    else:
        response = redirect('home')
    return response


def productListView(request, products_per_page, page_number, sponsor_company):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}

    cart2 = request.session.get('cart')
    user = request.user
    currentproduct = 0
    previous_page_number = page_number - 1
    next_page_number = page_number + 1
    paginated = False
    previous_page = False
    next_page = False
    count = 0
    page_low = (page_number - 1) * products_per_page
    page_high = (page_number * products_per_page) - 1
    # Get the sponsor username
    gUser = GenericUser.objects.get(username=user.username)
    userType = gUser.type
    print('user retrieved')
    if userType == 'Driver' or userType == 'Sponsor':
        driver = driverGet(user)
        #sponsor = Sponsor.objects.get(sponsor_company=sponsor_company)
        #search = sponsor.list_last_search
        #search = request.POST.get('search')
        prodID = ''
        prodID = request.POST.get('product-chosen')

        if prodID != '' and prodID != None:
            print('Product ID received!')
            if Product.objects.filter(sponsor_company=sponsor_company, idNum=prodID).exists():
                tempProduct = Product.objects.get(sponsor_company=sponsor_company, idNum=prodID)
                newOrder = DriverOrder.objects.create(product=tempProduct, customer=driver, quantity=1,
                                                      price=tempProduct.priceRaw,sponsor_company=sponsor_company)
        listed_products = Product.objects.filter(sponsor_company=sponsor_company)

        parse1 = []
        for item in listed_products:
            if page_low <= currentproduct <= page_high:
                currentproduct = currentproduct + 1
                parse1.append(requests.get(
                    'https://openapi.etsy.com/v2/listings/' + str(
                        item.idNum) + '?api_key=pmewf48x56vb387qgsprzzry').json()[
                                  'results'][0])
            else:
                currentproduct = currentproduct + 1

        if currentproduct > products_per_page:
            paginated = True

        if page_number == 1:
            previous_page = False
        else:
            previous_page = True

        if page_high >= currentproduct:
            next_page = False
        else:
            next_page = True

        # parse2 = parse1['results']
        parse3 = parse1
        tags = "tags: "
        for x in parse3:
            if len(x['title']) > 50:
                x['title'] = x['title'][0:49] + '...'
            if len(x['description']) > 250:
                x['description'] = x['description'][0:249] + '...'

        data = {
            'sponsor_company': sponsor_company,
            'items': parse3,
            'Driver': driver,
            'paginated': paginated,
            'previous': previous_page,
            'next': next_page,
            'current_page_number': page_number,
            'previous_page_number': previous_page_number,
            'next_page_number': next_page_number,
            'products_per_page': products_per_page,
            'realDriver': (userType == 'Driver'),
        }
        response = render(request, 'portal/driver_product_home.html', data)
    else:
        response = redirect('home')
    return response


def driver_catalogs(request):
    user = request.user
    gUser = GenericUser.objects.get(username=user.username)
    userType = gUser.type
    if userType == 'Driver' or userType == 'Sponsor':
        driver = driverGet(user)

        if userType == 'Sponsor':
            sponsor_list = Sponsorship.objects.filter(driver=driver.username,sponsor_company=Sponsor.objects.get(username=user.username).sponsor_company)
        else:
            sponsor_list = Sponsorship.objects.filter(driver=driver.username)
        #sponsor = Sponsor.objects.get(sponsor_company=driver.sponsor)
        sponsors = []
        for sponsor in sponsor_list:
            sponsors.append(sponsor)
        data = {
            "sponsors": sponsors
        }

        response = render(request, 'portal/driver_catalogs.html', data)

    else:
        response = redirect('home')
    return response


def productDetailView(request, product_ID, sponsor_company):
    user = request.user
    gUser = GenericUser.objects.get(username=user.username)
    userType = gUser.type
    print('user retrieved')
    if userType == 'Driver' or userType == 'Sponsor':
        driver = driverGet(user)
        #sponsor = Sponsor.objects.get(sponsor_company=sponsor_company)
        product = Product.objects.get(idNum=product_ID)
        prodID = ''
        prodID = request.POST.get('product-chosen')

        if prodID != '' and prodID != None:
            print('Product ID received!')
            if Product.objects.filter(sponsor_company=sponsor_company, idNum=prodID).exists():
                tempProduct = Product.objects.get(sponsor_company=sponsor_company, idNum=prodID)
                newOrder = DriverOrder.objects.create(product=tempProduct, customer=driver, quantity=1,
                                                      price=tempProduct.priceRaw, sponsor_company=sponsor_company)
        parse1 = []
        parse1.append(requests.get(
            'https://openapi.etsy.com/v2/listings/' + str(product.idNum) + '?api_key=pmewf48x56vb387qgsprzzry').json()[
                          'results'][0])
        parse3 = parse1
        data = {
            'items': parse3,
            'Driver': driver
        }
        response = render(request, 'portal/product_detail.html', data)
    else:
        response = redirect('home')

    return response


def Cart(request):
    user = request.user
    gUser = GenericUser.objects.get(username=user.username)
    userType = gUser.type
    print('user retrieved')
    if userType == 'Driver' or userType == 'Sponsor':
        driver = driverGet(user)
        orders = []
        if userType == 'Sponsor':
            cartItems = DriverOrder.objects.filter(customer=driver, status=False,sponsor_company=Sponsor.objects.get(username=user.username).sponsor_company)
        else:
            cartItems = DriverOrder.objects.filter(customer=driver, status=False)
        orderID = ''
        orderID = request.POST.get('product-chosen')

        if orderID != '' and orderID != None:
            order = DriverOrder.objects.get(customer=driver,id=orderID).delete()
            
        orderID = ''
        orderID = request.POST.get('place-order-override')

        if orderID != '' and orderID != None:
            for item in cartItems:
                item.orderStatus = 'OVERRIDE'
                item.save()
            response = redirect('Order-Placed')
        else:
            for items in cartItems:
                parse1 = requests.get(
                    'https://openapi.etsy.com/v2/listings/' + str(items.product.idNum) +
                    '?api_key=pmewf48x56vb387qgsprzzry').json()['results'][0]
                items.productName = parse1.get('title')
                orders.append(items)

            data = {
                'cartItems': orders,
                'driver':driver,
            }
            response = render(request, 'portal/cart.html', data)
    else:
        response = redirect('home')

    return response


def Order_History(request):
    user = request.user
    gUser = GenericUser.objects.get(username=user.username)
    userType = gUser.type
    print('user retrieved')
    if userType == 'Driver' or userType == 'Sponsor':
        driver = driverGet(user)
        orderID = ''
        orderID = request.POST.get('cancel-order')

        if orderID != '' and orderID != None:
            order = DriverOrder.objects.get(customer=driver,id=orderID)
            order.orderStatus = 'Cancelled'
            order.save()
        orders = []
        if userType == 'Sponsor':
            cartItems = DriverOrder.objects.filter(customer=driver, status=True, sponsor_company=Sponsor.objects.get(username=user.username).sponsor_company)
        else:
            cartItems = DriverOrder.objects.filter(customer=driver, status=True)
        print("Retrieved "+str(len(cartItems))+" items")
        for items in cartItems:
            parse1 = requests.get(
                'https://openapi.etsy.com/v2/listings/' + str(items.product.idNum) +
                '?api_key=pmewf48x56vb387qgsprzzry').json()['results'][0]
            items.productName = parse1.get('title')
            orders.append(items)

        data = {
            'cartItems': orders,
            'realDriver': (userType == 'Driver'),
            'driver': driver,
        }
        response = render(request, 'portal/Order_History.html', data)
    else:
        response = redirect('home')

    return response


def Order_Placed(request):
    user = request.user
    gUser = GenericUser.objects.get(username=user.username)
    userType = gUser.type
    user_placed_order = False
    user_out_of_points = False
    print('user retrieved')
    if userType == 'Driver' or userType == 'Sponsor':
        driver = driverGet(user)
        orders = []
        wasOverride = False
        if userType == 'Sponsor':
            cartItems = DriverOrder.objects.filter(customer=driver, status=False, sponsor_company=Sponsor.objects.get(username=user.username).sponsor_company)
        else:
            cartItems = DriverOrder.objects.filter(customer=driver, status=False)
        for items in cartItems:
            orders.append(items)

        for order in orders:
            itemsponsor = Sponsorship.objects.get(sponsor_company=order.product.sponsor_company, driver=driver.username)
            temp = itemsponsor.driver_points - (itemsponsor.price_scalar * order.price * int(order.orderStatus != 'OVERRIDE'))
            if order.orderStatus == 'OVERRIDE':
                wasOverride = True
            if temp < 0:
                user_out_of_points = True
            else:
                itemsponsor.driver_points = temp
                itemsponsor.save()
                order.status = True

        if not user_out_of_points:
            for order in orders:
                if order.orderStatus == 'OVERRIDE':
                    order.orderStatus = 'Order Placed By Override'
                else:
                    order.orderStatus = 'Order Placed'
                order.save()
        else:
            for order in orders:
                if order.status:
                    itemsponsor = Sponsorship.objects.get(sponsor_company=order.product.sponsor_company,
                                                          driver=driver.username)
                    temp = itemsponsor.driver_points + (itemsponsor.price_scalar * order.price)
                    itemsponsor.driver_points = temp
                    itemsponsor.save()

        data = {
            'placed': user_placed_order,
            'oop': user_out_of_points,
            'realDriver': (userType == 'Driver'),
            'wasOverride': wasOverride
        }
        response = render(request, 'portal/Order_Placed.html', data)
    else:
        response = redirect('home')

    return response

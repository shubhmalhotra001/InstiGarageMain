from django.shortcuts import render
import rest_framework
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Product
from users.models import User
from users.views import UserView
from rest_framework.response import Response


import json, uuid, jwt
# Create your views here.

# Check if the user is authenticated or not. (Using JWT tokens)
def checkAuth(token):  
    if not token:
        return 'Unauthenticated!'

    try:
        token = token.split('=')[1]
        payload = jwt.decode(token, 'terces', algorithm=['HS256'])
        return payload['id']
    except Exception:   # if invalid or expired token then exeception is thrown
        return 'Unauthenticated!'


# helps in converting the uuid values to json format
class UUIDEncoder(json.JSONEncoder): 
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


# Takes the product object as an input and returns the product info in dictionary format
def return_product(product):  
    return {
            '_id' : product['id'],
            'name': product['name'],
            'bid': product['bid'],
            'desc': product['desc'],
            'img': product['img'],
            'running': product['running'],
            'highestBidder': product['highestBidder'],
            'owner': product['owner'],
            'previousOwner': product['previousOwner'],
    }


# API endpoint to return all the products
# /api/product/product/
def get_all_products(request):
    products = Product.objects.all().values()
    
    result = list()
    for pr in products:
        result.append(return_product(pr))
    result = json.dumps(result, cls=UUIDEncoder)
    
    return HttpResponse(result, content_type='application/json')


# API endpoint to return the product with a specific id 
# /api/product/<productId> using GET method
# Only authenticated users can access it 
def get(request,id):
    token = request.headers.get('Authorization')  
    user_id = checkAuth(token)  # Check if the user is authenticated or not
    response = HttpResponse()
    
    
    if(user_id == 'Unauthenticated!'):
        return HttpResponse(json.dumps({"error":"Unauthenticated!"}), content_type='application/json')

    product = Product.objects.filter(id=id).values()
    if (product.count() == 0):
        return HttpResponse('No product of id ' + str(id)) # Check if the product even exist or not

    pr = return_product(product[0])
    if(user_id == product[0]['owner']):    # Check if the authenticated user is the owner of that product or not.
        pr['isOwner'] = True
    else:
        pr['isOwner'] = False
    
    owner = User.objects.filter(id=product[0]['owner']).values()[0]
    prevOwner = User.objects.filter(id=product[0]['previousOwner']).values()[0]

    pr['ownerName'] = owner['name']
    pr['ownerPhone'] = owner['phone']
    pr['previousOwnerName'] = prevOwner['name']
    pr['previousOwnerPhone'] = prevOwner['phone']

    resData = json.dumps(pr, cls=UUIDEncoder)   # Convert the data into json format

    return HttpResponse(resData, content_type='application/json')


# API endpoint to modify the product with a specific id 
# /api/product/<productId> using PUT method
# Only authorized users can access it 
def put(request,id):

    token = request.headers.get('Authorization')
    user_id = checkAuth(token) # Authentication check
    response = HttpResponse()
    
    if(user_id == 'Unauthenticated!'):
        return HttpResponse(json.dumps({"error":"Unauthenticated!"}), content_type='application/json')

    product = Product.objects.filter(id=id).values()
    if (product.count() == 0):
        return HttpResponse('No product of id ' + str(id)) # Check if the product exist or not

    # Check authorization: If the logged in user is the owner or not
    if(user_id != product[0]['owner']):
        return HttpResponse(json.dumps({"error":"Unauthorized!"}), content_type='application/json')

    pr = product[0]

    #conver request body from a json format to a dictionary one
    data = json.loads(request.body.decode())

    # If user doesn't pass some info in the request body, raise an exception and use the current value
    try:
        name = data['name']
    except:
        name = pr['name']
    
    try:
        bid = int(data['bid'])
    except:
        bid = pr['bid']

    try:
        desc = data['desc']
    except:
        desc = pr['desc']

    # update the product info
    Product.objects.filter(id=id).update(name=name, bid=bid, desc=desc) 

    return HttpResponse(json.dumps({"mssg":"Success"}), content_type='application/json')

# API endpoint to delete the product with a specific id 
# /api/product/<productId> using DELETE method
# Only authorized users can access it 
def delete(request,id):

    token = request.headers.get('Authorization')
    user_id = checkAuth(token) # Authentication check
    
    if(user_id == 'Unauthenticated!'):
        return HttpResponse(json.dumps({"error":"Unauthenticated!"}), content_type='application/json')

    product = Product.objects.filter(id=id).values()
    if (product.count() == 0):
        return HttpResponse('No product of id ' + str(id)) # Check if the product exist or not

    # Check authorization: If the logged in user is the owner or not
    if(user_id != product[0]['owner']):
        return HttpResponse(json.dumps({"error":"Unauthorized!"}), content_type='application/json')

    # delete the product
    Product.objects.filter(id=id).delete()
    
    return HttpResponse(json.dumps({"mssg":"sucess"}), content_type='application/json')


# API endpoint to create a product
# /api/product/ using POST method
# Only authenticated users can access it 
@csrf_exempt # Exemption from using csrf tokens for forms at the front end
def post(request):
    token = request.headers.get('Authorization')
    user_id = checkAuth(token)  # Authentication check
    response = HttpResponse()
    
    if(user_id == 'Unauthenticated!'):
        return HttpResponse(json.dumps({"error":"Unauthenticated!"}), content_type='application/json')

    # loads product info from request body 
    data = json.loads(request.body.decode())
    name = data['name']
    bid = int(data['bid'])
    desc = data['desc']
    running = True
    owner = user_id
    img = data['img']
    
    # When the product is created for the first time set owner = previous owner = highest bidder
    previousOwner = user_id
    highestBidder = user_id 

    # Create product
    Product.objects.create(name=name, bid=bid, desc=desc, owner=owner, img=img, previousOwner=previousOwner, highestBidder=highestBidder)

    return HttpResponse(json.dumps(data), content_type='application/json')


# API endpoint for CRUD on product 
# Call the specific python method based on the request method
# Eg: if method is get, return product info
@csrf_exempt
def product(request,id=''):
    method = request.method
    if(id==''):
        return get_all_products(request)
    if(method=='GET'):
        return get(request,id)
    elif(method=='PUT'):
        return put(request,id)
    elif(method=='POST'):
        return post(request,id)
    elif(method=='DELETE'):
        return delete(request,id)
    else:
        return HttpResponse("Method " + str(method) + " not supported")


# API endpoint to place a bid on a specifi product 
# /api/product/<productId>/bid/place/<bidAmount>
# Only authenticated users can access it 
@csrf_exempt
def placeBid(request,amount,id):
    token = request.headers.get('Authorization')
    user_id = checkAuth(token) # Authentication check
    response = HttpResponse()
    
    if(user_id == 'Unauthenticated!'):
        return HttpResponse(json.dumps({"error":"Unauthenticated!"}), content_type='application/json')

    product = Product.objects.filter(id=id).values()
    if (product.count() == 0): # Check if the product exist or not
        return HttpResponse(json.dumps({"mssg":"Product id not found"}), content_type='application/json')

    pr = Product.objects.filter(id=id).values()[0]
    currentBid = pr['bid']

    # Check if the auction is even running or not.
    if(not pr['running']):  
        return HttpResponse(json.dumps({"mssg":"Failed: Auction has stopped"}), content_type='application/json')

    amount = int(amount)
    wallet = int(User.objects.filter(id=user_id).values()[0]['wallet'])

    # Check if the user have sufficient money in his wallet
    if(amount > wallet): 
        return HttpResponse(json.dumps({"mssg":"Failed: Insufficient money"}), content_type='application/json')
    
    # Check if the placed bid is higher than the current bid
    if(amount < currentBid): 
        return HttpResponse(json.dumps({"mssg":"Failed: Bid amount should be higher than the current bid"}), content_type='application/json')

    Product.objects.filter(id=id).update(bid=amount, highestBidder=user_id)
    
    return get(request,id)
    # return HttpResponse(json.dumps({"mssg":"Success"}), content_type='application/json')


# API endpoint to sell the product to the highest bidder
# /api/product/<productId>/sell/
# Only authorized user (owner of the product) can access it 
@csrf_exempt
def sell(request,id):
    token = request.headers.get('Authorization')
    user_id = checkAuth(token) # Authentication check
    response = HttpResponse()
    
    if(user_id == 'Unauthenticated!'):
        return HttpResponse(json.dumps({"error":"Unauthenticated!"}), content_type='application/json')

    product = Product.objects.filter(id=id).values()
    if (product.count() == 0): # Product exist or not
        return HttpResponse(json.dumps({"mssg":"Product id not found"}), content_type='application/json')

    pr = Product.objects.filter(id=id).values()[0]

    walletOwner = User.objects.filter(id=user_id).values()[0]['wallet']
    walletBuyer = User.objects.filter(id=pr['highestBidder']).values()[0]['wallet']
    bid = pr['bid']

    # If the highest bidder is the owner, just stop the auction and do nothing.
    # Else sell the product to the highest bidder
    if(user_id != pr['highestBidder']):
        # update wallet of the seller and the buyer
        User.objects.filter(id=user_id).update(wallet=walletOwner+bid)
        User.objects.filter(id=pr['highestBidder']).update(wallet=walletBuyer-bid)

    # Make the highest bidder the owner
    Product.objects.filter(id=id).update(running=0, owner=pr['highestBidder'], previousOwner=user_id)

    return get(request,id)
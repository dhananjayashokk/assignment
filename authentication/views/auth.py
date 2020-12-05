from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from .. models import *
from .. serializers import *
from django.contrib.auth.hashers import make_password
import json
from django.contrib.auth import authenticate
import razorpay
from django.http import JsonResponse



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def signin(request):
	request = json.loads(request.body.decode('utf-8'))
	auth = authenticate(username=request['username'], password=request['password'])
	user = AuthUser.objects.filter(username=request['username'])
	if user:
		serializer = AuthSerializer(user, many=True)
		return Response(serializer.data)
	return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def signup(request):
	form_data=request.data.copy() 
	form_data["password"]=make_password(form_data["password"])
	form_data["is_active"]=1
	print(form_data)
	serializer = AuthSerializer(data=form_data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def order(request):
	request = json.loads(request.body.decode('utf-8'))
	try:
		client=razorpay.Client(auth=("rzp_test_RWzCot8F1JlWH4","MjrfFw4GQ0H7J2ICsfKuZqpn"))
		payment=client.order.create({'amount':int(request["amount"])*100,'currency':'INR'})
		print(payment)
	except Exception as e:
		print(e)

	return JsonResponse({"payment_details":payment})

@csrf_exempt
def capture_payment(request):
	request = json.loads(request.body.decode('utf-8'))
	amount=request["amount"]
	order_id=request["paymentId"]
	user_id=request["user_id"]
	try:
		client=razorpay.Client(auth=("rzp_test_RWzCot8F1JlWH4","MjrfFw4GQ0H7J2ICsfKuZqpn"))
		#capture_payment=client.payment.capture( amount*100, {"currency":"INR"})
		serializer = UserSubscriptionsSerializer(data={"amount":amount,"order_id":order_id,"user_id":user_id})
		if serializer.is_valid():
			serializer.save()
		else:
			print("error")
		print("serializer",serializer)
		return JsonResponse({"success":"capture_payment"})
	except Exception as e:
		return JsonResponse({"error":str(e)})

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import AuthenticationFailed


from .serializers import customerSerializer, billSerializer, customerWithBillSerializer, userSerializer

class userViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializer

    def create(self, request=None, user={}):
        print(user)
        
        user_name = None
        password = None
        serializer = None

        if len(user) > 0:
            user_name = user.get('username')
            password = user.get('password')
            serializer = userSerializer(data = user)
        elif len(request) > 0:
            user_name = request.data.get('username')
            password = request.data.get('password')
            serializer = userSerializer(data = request.data)

        if not serializer.is_valid():
            return Response({'status':403, 'errors':serializer.errors,'message':'some error'})

        serializer.save()

        user = User.objects.get(username=user_name)    

        user_token, _ = Token.objects.get_or_create(user=user)

        return Response({'status':200, 'payload':serializer.data, 'token':str(user_token)})


from .models import Customer, Bill, BillItem, Product

class customerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = customerSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

class billViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = billSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class customerDetailViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = customerWithBillSerializer
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

class customerViewSetNew(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = customerWithBillSerializer

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        # Retrieve token from URL parameters
        # print(self.kwargs)
        # full_url = request.build_absolute_uri()
        # print("Full URL:", full_url)
        
        # Access the URL path and query string
        url_path = request.get_full_path()
        print(request)
        print("URL Path and Query String:", url_path)

        token_key = url_path[14:-1]
        print(token_key)
        # token_key = request.query_params.get('token')
        if not token_key:
            raise AuthenticationFailed(_('No token provided.'))

        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            raise AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise AuthenticationFailed(_('User inactive or deleted.'))

        request.user = token.user

        return super().dispatch(request, *args, **kwargs)



#views 
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from .forms import ApiForm

class DashBoardView(TemplateView):
    template_name = 'dashboard.html'

class ApiFormView(FormView):
    def __init__(self):
        super().__init__()
        self.api_key = ''

    template_name = 'dashboard.html'
    form_class = ApiForm
    # success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = userViewSet()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user_dict = {
            'username':username,
            'password':password
        }

        response = user.create({},user_dict)

        print(response.data)
        token = response.data.get('token')
        self.api_key = f'localhost:9000/customer-data{token}'

        context = self.get_context_data()
        context['api_key'] = self.api_key
        return self.render_to_response(context)
        
        def get_context_data(self):
            context = super().get_context_data()

            context['api_key'] = self.api_key

            return context

        


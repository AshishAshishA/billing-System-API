from django.urls import path,include, re_path

from rest_framework import routers

from .views import customerViewSet, billViewSet1, customerDetailViewSet1, userViewSet, customerViewSet1, DashBoardView, ApiFormView

router = routers.DefaultRouter()

router.register(r'customer', customerViewSet1, basename='customer')
router.register(r'bills', billViewSet1, basename='bills')
router.register(r'customerWithBill', customerDetailViewSet1, basename='customer-details')
router.register(r'register', userViewSet, basename='user-register')


urlpatterns = [
    path('apis/', include(router.urls)),
    # re_path(r'^customer-data(?P<token>[^/.]+)/$', customerViewSet1.as_view({'get': 'list'}), name='customer-data-with-token'),
    # path('', DashBoardView.as_view(), name = 'dashboard'),
    path('', ApiFormView.as_view(), name = 'api-form')
]

from django.urls import path,include, re_path

from rest_framework import routers

from .views import customerViewSet, billViewSet, customerDetailViewSet, userViewSet, customerViewSetNew, DashBoardView, ApiFormView

router = routers.DefaultRouter()

router.register(r'customer', customerViewSet, basename='customer')
router.register(r'bills', billViewSet, basename='bills')
router.register(r'customer/detail', customerDetailViewSet, basename='customer-details')
router.register(r'register', userViewSet, basename='user-register')


urlpatterns = [
    path('apis/', include(router.urls)),
    re_path(r'^customer-data(?P<token>[^/.]+)/$', customerViewSetNew.as_view({'get': 'list'}), name='customer-data-with-token'),
    # path('', DashBoardView.as_view(), name = 'dashboard'),
    path('', ApiFormView.as_view(), name = 'api-form')
]

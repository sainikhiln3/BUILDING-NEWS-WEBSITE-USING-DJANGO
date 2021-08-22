from rest_framework import routers
from .views import public_viewset
router= routers.DefaultRouter()
router.register('User_Data',public_viewset)
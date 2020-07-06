from rest_framework import routers

from api.v1 import views


router = routers.DefaultRouter()
router.register(r'elections', views.ElectionViewSet, 'elections')
router.register(r'countries', views.CountryViewSet, 'countries')
router.register(r'digest', views.DigestViewSet, 'digest')
router.register(r'metadata', views.MetadataViewSet, 'metadata')
router.register(r'clients', views.ClientViewSet, 'clients')

router.register(r'elections_demo', views.ElectionDemoViewSet, 'elections_demo')
router.register(r'api_elections', views.ElectionApiViewSet, 'api_elections')

urlpatterns = router.urls

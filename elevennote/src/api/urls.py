from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet, UserViewSet, filter_note, share_note

app_name = 'api'

router = DefaultRouter(trailing_slash=False)
router.register(r'notes', NoteViewSet)

urlpatterns = [
    path('jwt-auth/', obtain_jwt_token),
    path('', include(router.urls)),
    path('notes/filter/<str:name>', filter_note, name='filter_note'),
    path('notes/<int:pk>/share/<int:user_id>', share_note, name='share_note')
]

from django.urls import path, include


urlpatterns = [
    path('authenticate/', include(('authentication.urls', 'authentication'), namespace='authentication')),
    path('users/', include(('users.urls', 'users'), namespace="users")),
    path('doubt/', include(('doubt.urls', 'doubt'), namespace='doubt'))
]
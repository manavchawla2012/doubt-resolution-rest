from django.urls import path, include

from users.api_views import UserLCView, UserDetailsView, UserRUDView

user_urls = [
    path("", UserLCView.as_view(), name="lc"),
    path("details", UserDetailsView.as_view(), name="details"),
    path("<uuid:id>", UserRUDView.as_view(), name='rud')
]

urlpatterns = [
    path("", include((user_urls, 'users'), namespace="users"))
]

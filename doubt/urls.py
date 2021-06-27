from django.urls import include, path

from doubt.api_views import RaiseDoubtLCView, RaiseDoubtRUDView, DoubtQnALCView, DashboardView

create_doubt_urls = [
    path("", RaiseDoubtLCView.as_view(), name="lc"),
    path("<uuid:id>", RaiseDoubtRUDView.as_view(), name="lc")
]

qna_urls = [
    path("", DoubtQnALCView.as_view(), name="lc")
]

urlpatterns = [
    path("", include((create_doubt_urls, 'doubt'), namespace='doubt')),
    path("qna", include((qna_urls, 'doubt'), namespace='qna')),
    path("dashboard", DashboardView.as_view(), name="dashboard")
]
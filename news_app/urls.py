from django.urls import path

from news_app.views import LandingPageView, DetailsPageView, ContactPageView, NotFoundPageView, SinglePageView, \
    CategoriesPageView, CreateNewsPageView, DashboardPageView, UpdateNewsPageView, DeleteNewsPageView, detailsPageView, \
    SearchPageView

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing_page'),
    path('contact/', ContactPageView.as_view(), name='contact_page'),
    path('single_page/', SinglePageView.as_view(), name='single_page'),
    path('404/', NotFoundPageView.as_view(), name='notFound_page'),
    path('detail/date:<int:year>/<int:month>/<int:day>/title:<slug:slug>', DetailsPageView.as_view(), name='detail_page'),
    path('category/<int:pk>/<slug:slug>/', CategoriesPageView.as_view(), name='category_page'),
    path('staff/create/', CreateNewsPageView.as_view(), name='create_news_page'),
    path('staff/', DashboardPageView.as_view(), name='dashboard_page'),
    path('staff/<slug>/update/', UpdateNewsPageView.as_view(), name='update_news_page'),
    path('staff/<slug>/delete/', DeleteNewsPageView.as_view(), name='delete_news_page'),
    path('search/', SearchPageView.as_view(), name='search_page')
]



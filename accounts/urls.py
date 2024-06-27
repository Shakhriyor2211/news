from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, \
    PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView, PasswordChangeDoneView
from accounts.views import loginPageView, ProfilePageView, registerPageView, RegisterPageView, profilePageView

urlpatterns = [
    # path('login/', loginPageView, name='login_page'),
    # path('logout/', LogoutView.as_view(next_page='login_page', http_method_names=['get', 'post', 'options']),
    #      name='logout_page'),
    path('login/', LoginView.as_view(), name='login_page'),
    path('logout/', LogoutView.as_view(next_page='landing_page'),
         name='logout_page'),
    path('profile/', profilePageView, name="profile_page"),
    # path('profile/', ProfilePageView.as_view(), name="profile_page"),
    path('password_change/', PasswordChangeView.as_view(success_url=reverse_lazy('landing_page')), name="password_change"),
    # path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(), name="password_reset"),
    path('password_reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset/complete/', PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('register', registerPageView, name="register_page"),
    # path('register', RegisterPageView.as_view(), name="register_page")
]

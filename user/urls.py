from django.urls import path
import user.views

urlpatterns = [
    path('home/', user.views.main_page),
    path('', user.views.login_handler),
    path('logout/', user.views.logout_handler),
    path('registration/', user.views.registration)
]

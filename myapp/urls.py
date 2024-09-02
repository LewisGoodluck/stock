from django.urls import path
from . import views
urlpatterns = [
    path("",views.dashboard,name="dashboard"),
    # user 
    path("registerProduct/",views.register_product,name="registerProduct"),
    path("login/",views.login_view,name="login"),
    path("logout/",views.logout_view,name="logout"),
    path("register/",views.register,name="register"),
    path("viewProduct/",views.view_product,name="viewProduct"),
    path("updateProduct/<int:id>",views.update_product,name="updateProduct"),
    path("deleteProduct/<int:id>",views.delete_product,name="deleteProduct"),
    path("productOut/",views.productOut,name="productOut"),
    path('search/', views.search, name='search'),
]

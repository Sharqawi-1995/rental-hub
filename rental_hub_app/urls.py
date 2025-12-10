from . import views
from django.urls import path

urlpatterns = [
    path('', views.login_meth, name='login'),
    path('register', views.register_meth, name='register'),
    path('logout', views.logout_meth, name='logout'),
    path('insufficient_priv', views.insufficient_priv_meth,
         name='insufficient_priv'),
    path('add-property', views.add_property_meth, name='add_property'),
    path('view-property/<int:id>', views.view_property_meth, name='view_property'),
    path('edit-property/<int:id>', views.edit_property_meth, name='edit_property'),
    path('delete-property/<int:id>',
         views.delete_property_meth, name='delete_property'),
    path('my_properties', views.dashboard),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update-user/', views.update_user, name='update_user'),
]

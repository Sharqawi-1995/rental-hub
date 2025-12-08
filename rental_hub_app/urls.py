from . import views
from django.urls import path

urlpatterns = [
    path('', views.login_meth),
    path('register', views.register_meth),
    path('logout', views.logout_meth),
    path('insufficient_priv', views.insufficient_priv_meth),
    
    path('add-property', views.add_property_meth),
    path('view-property/<int:id>', views.view_property_meth),
    path('edit-property/<int:id>', views.edit_property_meth),
    path('delete-property/<int:id>', views.delete_property_meth),
    path('my_properties', views.my_properties_meth),
    
	]
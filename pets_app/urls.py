from django.urls import path

from pets_app.views import (
                            PetsView, UserCreateView, UserLoginFormView, 
                            PetInformationCreateView, PetListView, PetDetailView, PetUpdateView, PetDeleteView, 
                            OwnerCreateView, OwnerListView, OwnerDetailView, OwnerUpdateView, OwnerDeleteView,
                            ServiceCreateView, ServiceListView, ServiceDetailView, ServiceUpdateView, ServiceDeleteView
                            ) 

app_name = 'pets_app_name'

urlpatterns = [
    path(route='', view= PetsView.as_view(), name = 'pets_name'),
    path(route='user_create_route/', view=UserCreateView.as_view(), name='user_create_name'),
    path(route='user_login_route/', view=UserLoginFormView.as_view(), name='user_login_name'),
    # path(route='user_logout_route/', view=UserLogoutView.as_view(), name='user_logout_name'),
    path(route= 'owner_create_route/', view=OwnerCreateView.as_view(), name='owner_create_name'),
    path(route= 'owner_list_route/', view=OwnerListView.as_view(), name='owner_list_name'),
    path(route= 'owner_detail_route/<int:pk>/', view=OwnerDetailView.as_view(), name='owner_detail_name'),
    path(route= 'owner_update_route/<int:pk>/', view=OwnerUpdateView.as_view(), name='owner_update_name'),
    path(route= 'owner_delete_route/<int:pk>/', view=OwnerDeleteView.as_view(), name='owner_delete_name'),
    path(route= 'pet_create_route/<int:number>', view=PetInformationCreateView.as_view(), name='pet_create_name'),
    path(route= 'pet_list_route/<int:number>', view=PetListView.as_view(), name='pet_list_name'),
    path(route= 'pet_detail_route/<int:pk>/', view=PetDetailView.as_view(), name='pet_detail_name'),
    path(route= 'pet_update_route/<int:pk>/', view=PetUpdateView.as_view(), name='pet_update_name'),
    path(route= 'pet_delete_route/<int:pk>/', view=PetDeleteView.as_view(), name='pet_delete_name'),
    path(route= 'service_create_route/', view=ServiceCreateView.as_view(), name='service_create_name'),
    path(route= 'service_list_route/', view=ServiceListView.as_view(), name='service_list_name'),
    path(route= 'service_detail_route/<int:pk>/', view=ServiceDetailView.as_view(), name='service_detail_name'),
    path(route= 'service_update_route/<int:pk>/', view=ServiceUpdateView.as_view(), name='service_update_name'),
    path(route= 'service_delete_route/<int:pk>/', view=ServiceDeleteView.as_view(), name='service_delete_name'),

]
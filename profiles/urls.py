from django.urls import path
from profiles.views import (user_profile,
                            user_profile_edit,
                            my_orders,
                            delete_my_orders,
                            my_wish_list,
                            my_wish_list_add,
                            delete_my_wish_list,

                            )

urlpatterns = [
    path('', user_profile, name='user_profile'),
    path('my-orders/', my_orders, name='my_orders'),
    path('my_wish_list/', my_wish_list, name='my_wish_list'),
    path('my_wish_list/add/<int:pk>/', my_wish_list_add, name='my_wish_list_add'),
    path('edit/', user_profile_edit, name='user_profile_edit'),
    path('delete/<int:pk>/delete_my_orders/', delete_my_orders, name='delete_my_orders'),
    path('delete/<int:pk>/delete_my_wish_list/', delete_my_wish_list, name='delete_my_wish_list'),


]

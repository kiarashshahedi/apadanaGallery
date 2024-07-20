from django.urls import path
from .views import (
    create_product_view, edit_product_view, view_product_view, list_product_view, list_product_count_view,
    items_tree_view, item_parents_view, unit_list_view,
    create_depot_view, view_depot_view, edit_depot_view, list_depot_view, list_depot_count_view,
    create_depot_io_view, edit_depot_io_view, view_depot_io_view, list_depot_io_view, depot_holding_view
)

urlpatterns = [
    path('products/create/', create_product_view, name='create_product'),
    path('products/edit/<str:item_guid>/', edit_product_view, name='edit_product'),
    path('products/view/<str:item_guid>/', view_product_view, name='view_product'),
    path('products/', list_product_view, name='product_list'),
    path('products/count/', list_product_count_view, name='product_list_count'),
    path('products/tree/', items_tree_view, name='items_tree'),
    path('products/parents/', item_parents_view, name='item_parents'),
    path('products/units/', unit_list_view, name='unit_list'),
    path('depot/create/', create_depot_view, name='create_depot'),
    path('depot/view/<str:depot_guid>/', view_depot_view, name='view_depot'),
    path('depot/edit/<str:depot_guid>/', edit_depot_view, name='edit_depot'),
    path('depot/', list_depot_view, name='depot_list'),
    path('depot/count/', list_depot_count_view, name='depot_list_count'),
    path('depot_io/create/', create_depot_io_view, name='create_depot_io'),
    path('depot_io/edit/<str:depot_io_guid>/', edit_depot_io_view, name='edit_depot_io'),
    path('depot_io/view/<str:depot_io_guid>/', view_depot_io_view, name='view_depot_io'),
    path('depot_io/', list_depot_io_view, name='depot_io_list'),
    path('depot_holding/', depot_holding_view, name='depot_holding')
]

from django.urls import path,include
from rest_framework import routers,urlpatterns
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register("inventory",InventoryView,'inventory')
router.register("inventory-csv",InventoryCSVLoaderView,'inventory csv')
router.register("shop",ShopView,'shop')
router.register("inventory-group",InventoryGroupView,'inventory group')
router.register("invoice",InvoiceView,'invoice')
router.register("summary",SummaryView,'summary')
router.register("purchase-summary",PurchaseSummaryView,'purchase summary')
router.register("sales-by-shop",SaleByShopView,'sales by shop')
router.register("sale-perfomance",SalePerfomanceView,'sale perfomance')

urlpatterns = [
    path("",include(router.urls))
]
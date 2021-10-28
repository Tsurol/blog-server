from django.urls import re_path
from trade import views

urlpatterns = [
    re_path("order/submit/", views.OrderSubmitView.as_view()),
    # 订单支付页面(get)，立即支付(post)，取消订单(put)，删除订单(delete)
    re_path("order/detail/<int:sn>/", views.OrderDetailView.as_view()),
    re_path("order/list/", views.OrderListView.as_view()),
]

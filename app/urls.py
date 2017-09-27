from django.conf.urls import url
from app import views

# 路由分发层 Router
#   函数名尽量与url对应，或者遵守一定的命名约定只要便于管理即可
#   注意url从上到下的匹配顺序
#

urlpatterns = [
    url(r'^user$', views.user),
    url(r'^q$', views.q),
    url(r'^a$', views.a),

    url(r'^log$', views.log),
    url(r'^index$', views.index),

    url(r'^$', views.index),
]

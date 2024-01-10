from django.urls import path, include
from . import views
app_name = 'courses'
urlpatterns = [
    path('', views.index, name='index'),
    path('chi-tiet-khoa-hoc/<slug>', views.chi_tiet_khoa_hoc, name='chi-tiet-khoa-hoc'),
    path('lich-khai-giang', views.lich_khai_giang, name='lich-khai-giang'),
    path('lich-khai-giang/<slug>', views.lich_khai_giang_lop, name='lich-khai-giang'),
    path('dang-ky/<slug>', views.dang_ky, name='dang-ky'),
    path('dang-nhap', views.dang_nhap, name='dang-nhap'),
    path('tai-khoan/lop-hoc-cua-toi', views.lop_hoc_cua_toi, name='lop-hoc-cua-toi'),
    path('tai-khoan/thong-tin-ca-nhan', views.tai_khoan, name='tai-khoan'),
    path('tai-khoan/huy-dang-ky/<slug>', views.huy_dang_ky, name='huy-dang-ky'),
    path('dang-xuat', views.dang_xuat, name='dang-xuat'),
    path('khoa-hoc', views.khoa_hoc, name='khoa-hoc'),
    path('chu-de/<slug>', views.chu_de, name='chu-de'),
    path('search', views.search_form, name='search'),
    path('dang-ky-tin-moi', views.dang_ky_tin_moi, name='dang-ky-tin-moi'),
]
from django.urls import path,include,re_path
from blog import views

app_name = 'blog'


urlpatterns =[
    path('about/',views.AboutView.as_view(),name='about'),
    path('home/',views.HomeView.as_view(),name='home'),
    path('',views.PostListView.as_view(),name='post_list'),
    re_path(r'^post/(?P<pk>\d+)$',views.PostDetailView.as_view(),name='detail_view'),
    re_path(r'^post/new/$', views.CreatePostView.as_view(), name='post_new'),
    re_path(r'^post/(?P<pk>\d+)/edit/$',views.PostUpdateView.as_view(),name='post_edit'),
    re_path(r'^post/(?P<pk>\d+)/remove/$',views.PostDeleteView.as_view(),name='post_remove'),
    re_path(r'^drafts/$',views.DraftListView.as_view(),name='post_draft_list'),
    re_path(r'^post/(?P<pk>\d+)/comments/$',views.add_comment_to_post,name='add_comment_to_post'),
    re_path(r'^comment/(?P<pk>\d+)/approve/$',views.comment_approve,name='comment_approve'),
    re_path(r'^comment/(?P<pk>\d+)/remove/$',views.comment_remove,name='comment_remove'),
    re_path(r'^post/(?P<pk>\d+)/publish/$',views.post_publish,name='post_publish'),
    re_path(r'^video/$', views.VideoListView.as_view(), name='videolist'),
    re_path(r'^video/new/$', views.UploadVideoView.as_view(), name='upload_video'),
    path('books/<int:pk>/', views.delete_video, name='delete_video'),
    re_path(r'^video/(?P<pk>\d+)$',views.VideoDetailView.as_view(),name='video_detail'),
    path('dashbord/',views.DashboardMainView,name="dashbord"),
    path('user_login/',views.user_login,name='user_login')




]


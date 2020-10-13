from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post,Comment,Video
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from blog.forms import PostForm,CommentForm,VideoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,DeleteView,ListView,UpdateView,DetailView,CreateView
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class HomeView(ListView):
    model = Video
    template_name = 'home.html'
    context_object_name = 'videos'
    
    def get_queryset(self):
        return Video.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')[:3]

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm

    model = Post


class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')

#######################################
## Functions that require a pk match ##
#######################################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:detail_view', pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog:detail_view', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog:detail_view', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog:detail_view', pk=post_pk)

#######################################
## video ##
#######################################
class VideoListView(ListView):
    model = Video
    template_name = 'video_list.html'
    context_object_name = 'videos'
    
    def get_queryset(self):
        return Video.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')


class UploadVideoView(CreateView,LoginRequiredMixin):
    model = Video
    form_class = VideoForm
    success_url = reverse_lazy('blog:videolist')
    template_name = 'upload_video.html'

def delete_video(request, pk):
    if request.method == 'POST':
        video = Video.objects.get(pk=pk)
        video.delete()
    return redirect('blog:videolist')

class VideoDetailView(DetailView):
    template_name = 'single_video.html'
    model = Video

def DashboardMainView(request):
    return render(request,template_name='dashboard_main.html')

def user_login(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('blog:post_list'))
            else:
                return HttpResponse("account not active")
        else:
            print("dozd omade!")
            return HttpResponse("invalid!")

    else:
        return render(request,'login_test.html',{})

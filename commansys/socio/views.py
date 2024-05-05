from datetime import timezone
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Community, Post, PostTemplate, PostTemplateItem, Comment
from .forms import CommunityForm, DefaultPostForm, PostTemplateItemForm
from django.contrib.auth.decorators import login_required

class CommunityCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = CommunityForm()
        context = {
            'form': form,
        }
        return render(request, 'socio/communitycreate.html', context)
        
    
    def post(self, request, *args, **kwargs):
        communities = Community.objects.all().order_by('-createdDate')
        form = CommunityForm(request.POST, request.FILES)
        if form.is_valid():
            new_community = form.save(commit=False)
            new_community.owner = request.user
            new_community.save()

            messages.success(request, 'Community creation is successful.')
        context = {
            'community_list': communities,
            'form': form,
        }
        return render(request, 'socio/communitycreate.html', context)


class CreatedCommunitiesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        communities = Community.objects.filter(owner=request.user).order_by('-createdDate')
        form = CommunityForm()  
        number_of_created_communities = len(communities)
        current_time = timezone.now()
        context = {
            'communities': communities,
            'form': form,  # Pass the form to the template
            'number_of_created_communities': number_of_created_communities,
            'current_time': current_time,
        }
        return render(request, 'socio/createdcommunities.html', context)    

class AllCommunitiesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        communities = Community.objects.all().order_by('-createdDate')
        form = CommunityForm()  
        communities_count = len(communities)
        current_time = timezone.now()
        context = {
            'communities': communities,
            'communities_count': communities_count,
            'current_time': current_time,
        }
        return render(request, 'socio/allcommunities.html', context)


class JoinCommunityView(LoginRequiredMixin, View):
    def get(self, request, community_id, *args, **kwargs):
        community = Community.objects.get(id=community_id)
        
        if community.is_private:

            messages.info(request, "You've sent a join request to the community owner.")
            return redirect('community_detail', community_id=community.id)  
        else:

            community.followers.add(request.user)
            messages.success(request, "You've successfully joined the community!")
            return redirect('community_detail', community_id=community.id) 

def home(request):

    communities = Community.objects.all().order_by('-createdDate')

    return render(request, 'socio/home.html', {'communities': communities})


@login_required
def create_post(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    if not (request.user == community.owner or request.user in community.managers.all() or request.user in community.followers.all()):
        return redirect(reverse('home'))
    
    post_templates = PostTemplate.objects.filter(community=community)
    if request.method == 'POST':
        form = DefaultPostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            
            # Create post template items
            title_item = PostTemplateItem.objects.create(post_type='text', mandatory=True, text=title)
            description_item = None
            if description:
                description_item = PostTemplateItem.objects.create(post_type='text', mandatory=False, text=description)
            
            # Create post with template items
            post = Post.objects.create(communit_id=community, author=request.user, 
                                       created_at = timezone.now(), update_at = timezone.now())
            post.fields.add(title_item)
            if description_item:
                post.fields.add(description_item)
            post.save()
            return redirect('community_detail', community_id=community_id)  # Redirect to community page after creating post
    else:
        form = DefaultPostForm()
    
    context = {'form': form,
               'post_templates': post_templates,
               'community_id': community_id,
               }
    return render(request, 'socio/create_post.html', context)

@login_required
def create_custom_post(request, community_id, template_id):
    community = get_object_or_404(Community, id=community_id)
    template = get_object_or_404(PostTemplate, id=template_id)

    # Handle form submission
    if request.method == 'POST':        
        post = Post.objects.create(communit_id=community, author=request.user, 
                                       created_at = timezone.now(), update_at = timezone.now())
        for field in template.fields.all():
            value = request.POST.get(field.name)
            file_value = request.FILES.get(field.name)
            if value or file_value:
                item = PostTemplateItem.objects.create(post_type=field.post_type, mandatory=field.mandatory)
                if field.name:
                    item.name = field.name
                
                if field.post_type == 'text':
                    item.text = value
                elif field.post_type in ['image', 'video', 'audio']:
                    try:
                        # Ensure file_value is valid before assigning it
                        item.clean_fields(exclude=['name', 'post_type', 'mandatory'])
                        setattr(item, field.post_type, file_value)
                    except ValidationError:
                        # Handle invalid file upload
                        error_message = f"Please upload a valid {field.post_type} file for the '{field.name}' field."
                        return render(request, 'socio/create_custom_post.html', {'community': community, 'template': template, 'error_message': error_message})

                elif field.post_type == 'datetime':
                    item.date = value
                elif field.post_type == 'location':
                    item.location = value
                item.save()
                
                post.fields.add(item)
            elif field.mandatory:
                # If a mandatory field is missing, display an error message
                error_message = f"Please fill in the '{field.name}' field."
                return render(request, 'socio/create_custom_post.html', {'community': community, 'template': template, 'error_message': error_message})
        post.template = template
        post.save()
        return redirect('community_detail', community_id=community_id)  # Redirect to community page after creating post

    # Render the form with the template fields
    return render(request, 'socio/create_custom_post.html', {'community': community, 'template': template})

@login_required
def create_template(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    if not (request.user == community.owner or request.user in community.managers.all()):
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        # Handle form submission
        template_name = request.POST.get('template_name')
        if not template_name:
            messages.error(request, "Template name is required.")
            return redirect('create_template', community_id=community_id)
        
        post_items = request.POST.getlist('post_items')
        if not post_items:
            messages.error(request, "At least one post item is required.")
            return redirect('create_template', community_id=community_id)

        # Create the PostTemplate
        template = PostTemplate.objects.create(name=template_name, community=community)
        item_count = len(post_items) / 3
        all_items = []
        for i in range(int(item_count)):
            name = post_items[i]
            post_type = post_items[i + 1]
            mandatory = post_items[i + 2] == 'false' if False else True
            item = PostTemplateItem.objects.create(name=name, post_type=post_type, mandatory=mandatory)
            all_items.append(item)
        
        if not any(item.mandatory for item in all_items):
            messages.error(request, "At least one post item must be mandatory.")
            return redirect('create_template', community_id=community_id)
        
        template.fields.add(*all_items)
        messages.success(request, "Template created successfully.")
        return redirect('create_template', community_id=community_id)
    else:
        # Handle GET request
        form = PostTemplateItemForm()
        context = {
            'form': form,
            'community_id': community_id,
        }
        return render(request, 'socio/create_template.html', context)

@login_required
def community_detail(request, community_id):
    community = get_object_or_404(Community,id=community_id)
    posts = Post.objects.filter(communit_id=community_id)
    is_admin = request==community.owner or request.user in community.managers.all()
    is_member = is_admin or request.user in community.followers.all()
    return render(request, 'socio/community_detail.html', 
                  {'community': community, 
                   'posts': posts,
                   'is_member': is_member,
                   'is_admin': is_admin})


@login_required
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    # You can add additional context data here if needed
    return render(request, 'socio/post_detail.html', {'post': post})

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        post.dislikes.remove(request.user) if request.user in post.dislikes.all() else None
    # Redirect back to the post detail page
    return HttpResponseRedirect(reverse('postDetailUrl', kwargs={'slug': post.slug}))

@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
        post.likes.remove(request.user) if request.user in post.likes.all() else None
    # Redirect back to the post detail page
    return HttpResponseRedirect(reverse('postDetailUrl', kwargs={'slug': post.slug}))


@login_required
def like_dislike_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        action = request.POST.get('action')
        if post_id:
            post = get_object_or_404(Post, id=post_id)
            if action == 'like':
                if request.user in post.dislikes.all():
                    post.dislikes.remove(request.user) if request.user in post.dislikes.all() else None
                post.likes.add(request.user)
            else:
                if request.user in post.likes.all():
                    post.likes.remove(request.user) if request.user in post.likes.all() else None
                post.dislikes.add(request.user)
            # Return a JSON response indicating success
            return JsonResponse({'success': True})
    
    # If the request method is not POST or post_id is not provided, return a JsonResponse with an error message
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required
def add_comment(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        text = request.POST.get('text')
        if post and text:
            comment = Comment.objects.create(author=request.user, text=text)
            comment.save()
            post.comments.add(comment)
            post.save()
            return JsonResponse({'success': True})

    # Return a JSON response indicating failure if the request method is not POST
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

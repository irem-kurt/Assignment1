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
from django.contrib.auth.models import User
from django.db.models import Q


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

            messages.success(request, 'Community creation is successful. Click My Communities to see your community.')
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
        following = Community.objects.filter(Q(followers__in=[request.user])).order_by('-createdDate')
        owning = Community.objects.filter(Q(owner=request.user)).order_by('-createdDate')
        print(len(following))
        for i in following:
            print(i.owner)
        print(len(owning))
        for i in owning:
            print(i.name)
        communities = following.union(owning)
        communities_count = len(communities)
        current_time = timezone.now()
        context = {
            'communities': communities,
            'communities_count': communities_count,
            'current_time': current_time,
        }
        print("irem")
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
    search_query = request.GET.get('search', '')  # Retrieve search term from GET request
    print(search_query)
    if search_query.strip():
        search_query = search_query.strip()
        named = Community.objects.filter(name__icontains=search_query).order_by('-createdDate')
        descripted = Community.objects.filter(description__icontains=search_query).order_by('-createdDate')
        ruled = Community.objects.filter(rules__icontains=search_query).order_by('-createdDate')
        communities = named.union(descripted, ruled)
    else:
        communities = Community.objects.all().order_by('-createdDate')

    return render(request, 'socio/home.html', {'search_term': search_query, 'communities': communities})



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
        print(template_name + " " + str(community))
        template = PostTemplate.objects.create(name=template_name, community=community)
        print(str(len(post_items)) + " " + str(len(post_items) / 3))
        item_count = len(post_items) / 3
        all_items = []
        for i in range(int(item_count)):
            x = 3*i
            name = post_items[x]
            post_type = post_items[x + 1]
            mandatory = post_items[x + 2] == 'false' if False else True
            print(f'{i}' + " " + name + " " + post_type + " " + str(mandatory))
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


def community_detail(request, community_id): 
    community = get_object_or_404(Community,id=community_id)
    is_pending = request.user in community.requests.all()
    if not request.user.is_authenticated:
        error_message = 'You must be logged in or registered to view this page.'
        return redirect('{}?error_message={}'.format(reverse('my-login'), error_message))

    if is_pending:
        return render(request, 'socio/community_detail.html', 
                {'community': community, 
                 'is_pending': is_pending,})
        
    is_admin = request.user == community.owner or request.user in community.managers.all()
    is_member = is_admin or request.user in community.followers.all()
    
    if request.method == 'POST':
        search_query = request.POST.get('search', '')
        print(search_query)
        if search_query.strip():
            search_query = search_query.strip()
            posts = Post.objects.filter(Q(fields__name__icontains=search_query) | Q(fields__post_type='text', fields__text__icontains=search_query)).distinct()
            return render(request, 'socio/community_detail.html', 
                {'community': community, 
                'posts': posts,
                'is_member': is_member,
                'is_admin': is_admin,
                'is_pending': is_pending,
                'search_term': search_query})
    
    posts = Post.objects.filter(communit_id=community_id)
    return render(request, 'socio/community_detail.html', 
                {'community': community, 
                'posts': posts,
                'is_member': is_member,
                'is_admin': is_admin,
                'is_pending': is_pending,})


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

@login_required
def community_join(request):
    if request.method == 'POST':
        community_id = request.POST.get('community_id')
        if community_id:
            community = get_object_or_404(Community, id=community_id)
            if community and request.user not in community.followers.all() and not community.is_private:
                community.followers.add(request.user)
                community.save()
                return JsonResponse({'success': True})
        
    # If the request method is not POST or post_id is not provided, return a JsonResponse with an error message
    return JsonResponse({'success': False, 'message': 'User cannot join community'})


@login_required
def community_quit(request):
    if request.method == 'POST':
        community_id = request.POST.get('community_id')
        if community_id:
            community = get_object_or_404(Community, id=community_id)
            if community:
                if request.user == community.owner:
                    return JsonResponse({'success': False, 'message': 'Owner cannot quit community'})
                elif request.user in community.managers.all():
                    community.managers.remove(request.user)
                    community.save()
                    return JsonResponse({'success': True})
                elif request.user in community.followers.all():
                    community.followers.remove(request.user)
                    community.save()
                    return JsonResponse({'success': True})
        
    # If the request method is not POST or post_id is not provided, return a JsonResponse with an error message
    return JsonResponse({'success': False, 'message': 'User cannot quit community'})


@login_required
def community_request(request):
    if request.method == 'POST':
        community_id = request.POST.get('community_id')
        if community_id:
            community = get_object_or_404(Community, id=community_id)
            if community and request.user not in community.followers.all() and community.is_private:
                community.requests.add(request.user)
                community.save()
                return JsonResponse({'success': True})
        
    # If the request method is not POST or post_id is not provided, return a JsonResponse with an error message
    return JsonResponse({'success': False, 'message': 'User cannot quit community'})

@login_required
def display_requests(request, community_id):
    community = get_object_or_404(Community,id=community_id)
    is_admin = request.user == community.owner or request.user in community.managers.all()
    if not is_admin:
        return redirect(reverse('home'))
    requests = community.requests.all()
    return render(request, 'socio/community_requests.html', 
                  {'community': community,
                   'requests': requests,
                   'is_admin': is_admin,})
    
@login_required
def display_followers(request, community_id):
    community = get_object_or_404(Community,id=community_id)
    is_owner = request.user == community.owner
    is_admin = is_owner or request.user in community.managers.all()
    is_member = is_admin or request.user in community.followers.all()
    if community.is_private and not is_member:
        return redirect(reverse('home'))
    if request.method == 'POST':
        search_query = request.POST.get('search', '')
        print(search_query)
        followers = community.followers.filter(username__icontains=search_query)
        print(len(followers))
    else:
        followers = community.followers.all()
    return render(request, 'socio/community_followers.html', 
                  {'community': community,
                   'followers': followers,
                   'is_owner': is_owner,})

@login_required
def community_response(request):
    if request.method == 'POST':
        community_id = request.POST.get('community_id')
        community = get_object_or_404(Community,id=community_id)
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        accept = request.POST.get('accept')
        print(user_id + " " + community_id + " " + accept)
        if community and user:
            if user not in community.requests.all() or user in community.followers.all():
                return JsonResponse({'success': False, 'message': 'User cannot be accepted'})
            else:
                community.requests.remove(user)
                if accept == 'true':
                    community.followers.add(user)
                community.save()
                return JsonResponse({'success': True})
        
    # If the request method is not POST or post_id is not provided, return a JsonResponse with an error message
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
def make_remove_manager(request):
    if request.method == 'POST':
        community_id = request.POST.get('community_id')
        community = get_object_or_404(Community,id=community_id)
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        action = request.POST.get('action')
        print(user_id + " " + community_id + " " + action)
        if community and user:
            if user not in community.followers.all():
                return JsonResponse({'success': False, 'message': 'User must be follower'})
            else:
                if action == 'add' and user not in community.managers.all():
                    community.managers.add(user)
                else:
                    community.managers.remove(user)
                community.save()
                return JsonResponse({'success': True})
        
    # If the request method is not POST or post_id is not provided, return a JsonResponse with an error message
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
def follow_unfollow(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        action = request.POST.get('action')
        print(user_id + " " + action + " " + f'{user}' + " " + f'{request.user not in user.profile.followers.all()}')
        if user:
            if action == 'follow' and request.user not in user.profile.followers.all():
                print("added " + action + " " + f'{user.profile.followers.all()}')
                user.profile.followers.add(request.user)
            elif action == 'unfollow' and request.user in user.profile.followers.all():
                print("removed " + action + " " + f'{user.profile.followers.all()}')
                user.profile.followers.remove(request.user)
            user.profile.save()
            return JsonResponse({'success': True})
        
    # If the request method is not POST or post_id is not provided, return a JsonResponse with an error message
    return JsonResponse({'success': False, 'message': 'Invalid request method'})
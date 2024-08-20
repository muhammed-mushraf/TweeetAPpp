from django.shortcuts import redirect, render, get_object_or_404
from .models import Tweet, Like, Comment
from .forms import TweetForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def add_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tweet_id = data.get('tweet_id')
        text = data.get('text')

        tweet = get_object_or_404(Tweet, id=tweet_id)

        # Create a new comment
        comment = Comment.objects.create(tweet=tweet, user=request.user, text=text)

        # Prepare data for the response
        response_data = {
            'text': comment.text,
            'user': comment.user.username,
            'avatar_url': comment.user.profile.avatar.url,  # Assuming avatar is stored in the user's profile
        }

        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request'}, status=400)




def index(request):
    return render(request, 'index.html')

def tweet_detail(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    comments = tweet.comments.all()

    return render(request, 'tweet_detail.html', {'tweet': tweet, 'comments': comments})


def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    context = {'tweets': tweets}
    return render(request, 'tweet_list.html', context)

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    context = {'form': form}
    return render(request, 'tweet_form.html', context)


@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:  
        form = TweetForm(instance=tweet)
    context = {'form': form}   
    return render(request, 'tweet_form.html', context)

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
        
    context = {'tweet': tweet}
    return render(request, 'tweet_delete.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)
@login_required
def toggle_like(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    liked = False

    # Check if the user has already liked the tweet
    like_obj, created = Like.objects.get_or_create(user=request.user, tweet=tweet)

    if not created:  # If the like already exists, unlike it
        like_obj.delete()
        tweet.like_count = max(0, tweet.like_count - 1)
    else:  # If it's a new like, increment the like count
        tweet.like_count += 1
        liked = True

    tweet.save()

    # Return JSON response for AJAX
    return JsonResponse({
        'liked': liked,
        'like_count': tweet.like_count
    })
def profile(request, username):
    user = get_object_or_404(User, username=username)
    tweets = Tweet.objects.filter(user=user).order_by('-created_at')
    context = {
        'user': user,
        'tweets': tweets,
    }
    return render(request, 'profile.html', context)
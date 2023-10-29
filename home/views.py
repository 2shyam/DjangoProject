from django.shortcuts import render,HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post

# html pages
def home(request):
    return render(request, 'home/home.html')
def about(request): 
    return render(request, 'home/about.html')
def contact(request): 
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content= request.POST['content']
        print(name, email, phone, content) 

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,"please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "your message has been successfully sent")
    return render(request, 'home/Contact.html')

def search(request):
    query = request.GET['query']
    if len(query)>80:
        allPosts = Post.objects.none()

    else: 
    #allPosts = Post.objects.all ()
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent =  Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)

    if allPosts.count() == 0:
        messages.warning (request, "no search results found.")
    params = {'allPosts': allPosts, 'query' :query}
    return render(request, 'home/search.html',params)

# anthentication APIs

def handleSignUp(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for errorneous inputs
        if len(username) >15:
            messages.error(request, "Username must be under 15 characters")
            return redirect('home')
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "password do not match ")
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"your account has been successfully created")
        return redirect('home')


    else:
        return HttpResponse('404 - Not Found')
    

def handleLogin(request):
         if request.method == 'POST':
        # Get the post parameters
           loginusername = request.POST['loginusername']
           loginpassword = request.POST['loginpassword']

           user = authenticate( username=loginusername, password=loginpassword)

           if user is not None:
               login(request, user)
               messages.success(request,"successfully logged in")
               return redirect('home')
           else:
               messages.error(request, "Invaild Credentials, please try again")
               return redirect('home')
           
           
    
         return HttpResponse('404 - Not Found')
    
def handleLogout(request):
            logout(request)
            messages.success(request, "successfully logged out")
            return redirect('home')
        
    
    


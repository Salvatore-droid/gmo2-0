from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import GMOProduct, ChatMessage, EducationalResource, VerificationRequest
import json
from django.contrib.auth import login, logout, authenticate
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from .models import Webinar
from django.views.decorators.csrf import csrf_exempt
from transformers import pipeline





@login_required
def dashboard(request):
    # Get latest chat messages (last 10)
    chat_messages = ChatMessage.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    # Get educational resources
    educational_resources = EducationalResource.objects.all().order_by('-created_at')[:4]
    
    # Get verified products
    verified_products = GMOProduct.objects.filter(verification_status='verified').order_by('-created_at')[:3]
    
    # Get all products for directory (paginated)
    all_products = GMOProduct.objects.all().order_by('-created_at')
    paginator = Paginator(all_products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'chat_messages': chat_messages,
        'educational_resources': educational_resources,
        'verified_products': verified_products,
        'page_obj': page_obj,
    }
    return render(request, 'dashboard.html', context)




# Initialize the AI model (agriculture-focused)
agriculture_qa = pipeline(
    "question-answering",
    model="deepset/roberta-base-squad2",
    tokenizer="deepset/roberta-base-squad2"
)

AGRICULTURE_KNOWLEDGE = """
Genetically Modified Organisms (GMOs) are organisms whose genetic material has been altered using genetic engineering techniques. 
In agriculture, GMO crops are designed to improve yield, enhance nutritional content, drought tolerance, and resistance to pests and diseases. 
Common GMO crops include corn, soybeans, cotton, and canola. Regulatory agencies like the FDA, EPA, and USDA evaluate GMO safety before approval.
Organic farming prohibits GMO use, while conventional farming may use them. Farmers should check seed certification and local regulations.
"""

@login_required
def chat_view(request):
    """Render the agriculture chat template"""
    # Get last 5 messages for the current user
    recent_messages = ChatMessage.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'dashboard.html', {
        'recent_messages': recent_messages
    })

@csrf_exempt
@login_required
def chat_api(request):
    """Handle AJAX chat requests"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            # Get AI response
            result = agriculture_qa(
                question=user_message,
                context=AGRICULTURE_KNOWLEDGE,
                max_answer_len=200
            )
            
            # Save to database
            ChatMessage.objects.create(
                user=request.user,
                message=user_message,
                response=result['answer']
            )
            
            return JsonResponse({
                'response': result['answer'],
                'suggestions': [
                    "GMO regulations in my area",
                    "How to verify seed authenticity",
                    "Benefits of GMO corn",
                    "Non-GMO alternatives"
                ]
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)





@login_required
def verify_product(request):
    if request.method == 'POST':
        verification_method = request.POST.get('method')
        verification_code = request.POST.get('code')
        
        # In a real app, you'd validate against your database
        try:
            product = GMOProduct.objects.get(qr_code=verification_code)
            is_verified = product.verification_status == 'verified'
            
            VerificationRequest.objects.create(
                user=request.user,
                product=product,
                verification_code=verification_code,
                verification_method=verification_method,
                is_verified=is_verified,
                verification_result={
                    'product_name': product.name,
                    'company': product.company,
                    'status': product.verification_status,
                    'certification_id': product.certification_id,
                    'certification_date': product.certification_date.strftime('%B %d, %Y') if product.certification_date else '',
                    'certification_authority': product.certification_authority,
                }
            )
            
            return JsonResponse({
                'is_verified': is_verified,
                'product_name': product.name,
                'company': product.company,
                'status': product.verification_status,
                'certification_id': product.certification_id,
                'certification_date': product.certification_date.strftime('%B %d, %Y') if product.certification_date else '',
                'certification_authority': product.certification_authority,
            })
        except GMOProduct.DoesNotExist:
            return JsonResponse({
                'is_verified': False,
                'error': 'Product not found'
            }, status=404)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def filter_products(request):
    crop_type = request.GET.get('crop_type', '')
    season = request.GET.get('season', '')
    region = request.GET.get('region', '')
    status = request.GET.get('status', '')
    
    products = GMOProduct.objects.all()
    
    if crop_type:
        products = products.filter(crop_type=crop_type)
    if season:
        products = products.filter(season=season)
    if status:
        products = products.filter(verification_status=status)
    
    # Note: Region filtering would require a region field in the model
    
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'product_list_partial.html', {
        'page_obj': page_obj
    })



# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")  
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not username:
            messages.error(request, "Username is required.")
            return redirect("register")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("login_view")

    return render(request, "register.html")



def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login_view')


def webinar_redirect(request):
    try:
        # Get the latest active webinar
        webinar = Webinar.objects.filter(
            is_active=True,
            scheduled_time__gte=timezone.now()  # Only future webinars
        ).latest('scheduled_time')
        return redirect(webinar.zoom_registration_url)
    
    except Webinar.DoesNotExist:
        # Fallback URL if no webinars exist
        return redirect('https://zoom.us/webinars')  # Or a custom "no webinars" page
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


# agriculture_app/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import ChatMessage, GMOKnowledgeBase
from .gmo_knowledge import GMO_KNOWLEDGE, get_related_suggestions

def get_gmo_response(user_message, context):
    """
    Enhanced response generation with context awareness
    """
    # 1. Check knowledge base for direct matches
    knowledge_match = GMOKnowledgeBase.objects.filter(
        question_patterns__icontains=user_message.lower()
    ).order_by('-confidence_score').first()
    
    if knowledge_match:
        return {
            'answer': knowledge_match.answer,
            'context': {'last_topic': knowledge_match.topic},
            'confidence': knowledge_match.confidence_score
        }
    
    # 2. Check our static knowledge base
    for topic, content in GMO_KNOWLEDGE.items():
        if topic in user_message.lower():
            return {
                'answer': content,
                'context': {'last_topic': topic},
                'confidence': 0.9  # High confidence for curated content
            }
    
    # 3. Use NLP for more complex queries (example with OpenAI)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an agricultural expert specializing in GMO technology."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=200
        )
        return {
            'answer': response.choices[0].message['content'],
            'context': context,
            'confidence': 0.8  # Default confidence for generated answers
        }
    except Exception:
        # Fallback response
        return {
            'answer': "I'm sorry, I couldn't retrieve information on that GMO topic. Could you try rephrasing?",
            'context': context,
            'confidence': 0.3
        }

@login_required
def chat_view(request):
    """Render the agriculture chat template"""
    recent_messages = ChatMessage.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'dashboard.html', {
        'recent_messages': recent_messages,
        'topics': GMOKnowledgeBase.TOPIC_CHOICES
    })

@csrf_exempt
@login_required
def chat_api(request):
    """Handle AJAX chat requests"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            context = data.get('context', {})
            
            result = get_gmo_response(user_message, context)
            
            chat_msg = ChatMessage.objects.create(
                user=request.user,
                message=user_message,
                response=result['answer'],
                context=result['context']
            )
            
            return JsonResponse({
                'response': result['answer'],
                'context': result['context'],
                'message_id': chat_msg.id,
                'suggestions': get_related_suggestions(result['context'].get('last_topic'))
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
def feedback_api(request):
    """Handle user feedback to improve responses"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message_id = data.get('message_id')
            is_helpful = data.get('is_helpful')
            
            message = ChatMessage.objects.get(id=message_id, user=request.user)
            message.is_helpful = is_helpful
            message.save()
            
            if is_helpful is not None:
                knowledge = GMOKnowledgeBase.objects.filter(
                    answer=message.response
                ).first()
                
                if knowledge:
                    change = 0.1 if is_helpful else -0.15
                    knowledge.confidence_score = max(0.1, min(1.0, knowledge.confidence_score + change))
                    knowledge.save()
            
            return JsonResponse({'status': 'success'})
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
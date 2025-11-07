from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AppointmentForm
from accounts.models import User
from .models import Appointment, Conversation, Notification

@login_required
def book_lawyer(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save(commit=False)
            appt.user = request.user
            appt.save()
            return redirect('booking_success')
    else:
        form = AppointmentForm()
    lawyers = User.objects.filter(role='lawyer').only('id', 'username', 'bio', 'profile_image', 'first_name', 'last_name')
    return render(request, 'booking/book_lawyer.html', {'form': form, 'lawyers': lawyers})

@login_required
def approve_appointment(request, pk):
    try:
        appt = get_object_or_404(Appointment, pk=pk, lawyer=request.user)
        appt.status = 'approved'
        appt.save(update_fields=['status'])
        
        # Ensure conversation exists
        conv, created = Conversation.objects.get_or_create(user=appt.user, lawyer=appt.lawyer)
        
        # Notify the user
        notification = Notification.objects.create(
            sender=request.user,
            recipient=appt.user,
            message=f"Your appointment with {request.user.username} has been approved.",
            conversation=conv,
        )
        
        return redirect('lawyer_dashboard')
    except Exception as e:
        from django.contrib import messages
        messages.error(request, "An error occurred while approving the appointment.")
        return redirect('lawyer_dashboard')

@login_required
def decline_appointment(request, pk):
    appt = get_object_or_404(Appointment, pk=pk, lawyer=request.user)
    appt.status = 'declined'
    appt.save(update_fields=['status'])
    return redirect('lawyer_dashboard')

@login_required
def complete_appointment(request, pk):
    try:
        appt = get_object_or_404(Appointment, pk=pk, lawyer=request.user)
        appt.status = 'completed'
        appt.save(update_fields=['status'])
        
        # Notify the user
        conv = appt.get_conversation()
        if conv:
            notification = Notification.objects.create(
                sender=request.user,
                recipient=appt.user,
                message=f"Your case with {request.user.username} has been marked as completed.",
                conversation=conv,
            )
        
        return redirect('lawyer_dashboard')
    except Exception as e:
        from django.contrib import messages
        messages.error(request, "An error occurred while marking the appointment as complete.")
        return redirect('lawyer_dashboard')

@login_required
def chat(request, user_id=None, lawyer_id=None):
    try:
        # Determine conversation parties based on the current user's role
        if request.user.role == 'lawyer':
            conv = get_object_or_404(Conversation, user_id=user_id, lawyer=request.user)
            other = conv.user
        else:
            conv = get_object_or_404(Conversation, user=request.user, lawyer_id=lawyer_id)
            other = conv.lawyer
        
        if request.method == 'POST':
            text = request.POST.get('text')
            if text and text.strip():  # Only create message if text is not empty
                from .models import Message
                # Check if a similar message was sent recently to prevent duplicates
                from django.utils import timezone
                recent_messages = conv.messages.filter(
                    sender=request.user,
                    text=text.strip(),
                    created_at__gte=timezone.now() - timezone.timedelta(seconds=5)
                )
                if not recent_messages.exists():
                    Message.objects.create(conversation=conv, sender=request.user, text=text.strip())
                # Redirect to prevent form resubmission on refresh
                return redirect(request.path)
        
        # Get messages ordered by creation time
        chat_messages = conv.messages.all().order_by('created_at')
        return render(request, 'booking/chat.html', {
            'conversation': conv, 
            'other': other,
            'chat_messages': chat_messages
        })
    except Conversation.DoesNotExist:
        from django.contrib import messages
        messages.error(request, "Conversation not found. It may have been deleted or never created.")
        return redirect('user_home')
    except Exception as e:
        from django.contrib import messages
        messages.error(request, "An error occurred while loading the conversation.")
        return redirect('user_home')

@login_required
def chat_by_conversation(request, pk):
    try:
        # Check if the conversation exists
        try:
            conv = Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            from django.contrib import messages
            messages.error(request, f"Conversation not found. It may have been deleted or never created.")
            return redirect('user_home')
        
        # Ensure the user is a participant
        if request.user != conv.user and request.user != conv.lawyer:
            return redirect('user_home')
        
        other = conv.lawyer if request.user == conv.user else conv.user
        
        if request.method == 'POST':
            text = request.POST.get('text')
            if text and text.strip():  # Only create message if text is not empty
                from .models import Message
                # Check if a similar message was sent recently to prevent duplicates
                from django.utils import timezone
                recent_messages = conv.messages.filter(
                    sender=request.user,
                    text=text.strip(),
                    created_at__gte=timezone.now() - timezone.timedelta(seconds=5)
                )
                if not recent_messages.exists():
                    Message.objects.create(conversation=conv, sender=request.user, text=text.strip())
                # Redirect to prevent form resubmission on refresh
                return redirect(request.path)
        
        # Get messages ordered by creation time
        chat_messages = conv.messages.all().order_by('created_at')
        return render(request, 'booking/chat.html', {
            'conversation': conv, 
            'other': other,
            'chat_messages': chat_messages
        })
        
    except Exception as e:
        # Log any other errors
        from django.contrib import messages
        messages.error(request, "An error occurred while loading the conversation.")
        return redirect('user_home')

@login_required
def booking_success(request):
    return render(request, 'booking/booking_success.html')

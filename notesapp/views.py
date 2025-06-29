from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import signup_form, login_form, add_note_form
from .models import Note



# Create your views here.
# @login_required


# Home View
def home(request):
    type_filter = request.GET.get('type')
    search_query = request.GET.get('search')

    # Filter public notes if type is selected
    if type_filter:
        public_notes = Note.objects.filter(privacy='public', type__iexact=type_filter).order_by('-created_at')
    else:
        public_notes = Note.objects.filter(privacy='public').order_by('-created_at')

    # Apply search filter if search query is given
    if search_query:
        public_notes = public_notes.filter(title__icontains=search_query)

    # Show private notes only if logged in (no filter applied here)
    private_notes = None
    if request.user.is_authenticated:
        private_notes = Note.objects.filter(user=request.user, privacy='private').order_by('-created_at')

    # Get available public note types for dropdown
    note_types = Note.objects.filter(privacy='public').values_list('type', flat=True).distinct()

    context = {
        'public_notes': public_notes,
        'private_notes': private_notes,
        'note_types': note_types,
        'selected_type': type_filter,
        'search_query': search_query,
    }

    return render(request, 'index.html', context)


# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = signup_form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect('home')
        
        else:
            messages.error(request, "Invalid form data.")
    else:
        form = signup_form()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    form = login_form(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "You have been logged in.")
            
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

# Add Note View
@login_required
def add_note_view(request):
    if request.method == 'POST':
        form = add_note_form(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('home')
    else:
        form = add_note_form() 

    return render(request, 'add_note.html', {'form': form})

# My Notes View
@login_required
def my_notes_view(request):
    user_notes = Note.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_notes.html', {'notes': user_notes})

# Edit Note View
@login_required
def edit_note_view(request, pk):
    note = Note.objects.get(pk=pk)  

    if request.method == 'POST':
        form = add_note_form(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Note updated successfully.")
            return redirect('my_notes')
    else:
        form = add_note_form(instance=note)

    return render(request, 'edit_note.html', {'form': form})

# Delete Note View
@login_required
def delete_note_view(request, pk):
    note = Note.objects.get(pk=pk)  

    if request.method == 'POST':
        note.delete()
        messages.success(request, "Note deleted successfully.")
        return redirect('my_notes')
    

    
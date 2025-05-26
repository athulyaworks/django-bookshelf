from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import BookForm,ReviewForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

def toggle_read(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.is_read = not book.is_read
    book.save()
    return redirect('book_list')

def toggle_favourite(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.is_favourite = not book.is_favourite
    book.save() 
    return redirect('book_list')


def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('book_list')

def genres(request):
    genres = Genre.objects.all().prefetch_related('book_set')
    return render(request, 'genres.html', {'genres': genres})

def blog(request):
    return render(request, 'blog.html')

def reviews(request):
    all_reviews = Review.objects.select_related('book').order_by('-created_at')
    form = ReviewForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('reviews')

    return render(request, 'reviews.html', {
        'form': form,
        'all_reviews': all_reviews,
    })

def myshelf(request):
    favourite_books = Book.objects.filter(is_favourite=True)
    return render(request, 'myshelf.html', {'favourite_books': favourite_books})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Genre, Review, Favourite, UserBookStatus
from .forms import BookForm, ReviewForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from collections import Counter


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'login.html')




@login_required
def home(request):
    user = request.user
    favourite_books_ids = Favourite.objects.filter(user=user).values_list('book_id', flat=True)
    books = Book.objects.all()

    # Fetch all statuses in one query
    user_statuses = UserBookStatus.objects.filter(user=user).values_list('book_id', 'status')
    status_dict = dict(user_statuses)

    # Prepare book attributes and count statuses
    status_counts = Counter()
    for book in books:
        book.is_favourite = book.id in favourite_books_ids
        book.read_status = status_dict.get(book.id, 'not_started')
        status_counts[book.read_status] += 1

    book_count = books.count()

    return render(request, 'home.html', {
        'books': books,
        'book_count': book_count,
        'user': user,
        'status_counts': {
            'not_started': status_counts.get('not_started', 0),
            'reading': status_counts.get('reading', 0),
            'finished': status_counts.get('finished', 0),
        }
    })




def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


@login_required
def book_list(request):
    query = request.GET.get('q', '')
    user = request.user

    if query:
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()

    favourite_ids = set(Favourite.objects.filter(user=user).values_list('book_id', flat=True))

    # Fetch status from UserBookStatus (not just True/False)
    user_statuses = UserBookStatus.objects.filter(user=user, book__in=books).values_list('book_id', 'status')
    status_dict = dict(user_statuses)

    for book in books:
        book.is_favourite = book.id in favourite_ids
        book.read_status = status_dict.get(book.id, 'not_started')

    book_count = books.count()

    return render(request, 'book_list.html', {
        'books': books,
        'book_count': book_count,
        'query': query,
        'favourite_ids': favourite_ids,
        'user': user,
    })



@login_required
def add_book(request):
    if request.method == 'POST':
        
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})



@login_required
def toggle_read(request, book_id):
    user = request.user
    book = get_object_or_404(Book, id=book_id)

    status, created = UserBookStatus.objects.get_or_create(user=user, book=book)

    if status.status == 'not_started':
        status.status = 'reading'
    elif status.status == 'reading':
        status.status = 'finished'
    else:
        status.status = 'not_started'

    status.save()
    return redirect('book_list')



@login_required
def toggle_favourite(request, book_id):
    user = request.user
    book = get_object_or_404(Book, id=book_id)
    favourite, created = Favourite.objects.get_or_create(user=user, book=book)

    if not created:
        favourite.delete()
        messages.info(request, f'"{book.title}" removed from your shelf.')
    else:
        messages.success(request, f'"{book.title}" added to your shelf!')

    return redirect(request.META.get('HTTP_REFERER', 'book_list'))


@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    messages.success(request, 'Book deleted successfully.')
    return redirect('book_list')


def genres(request):
    genres = Genre.objects.all().prefetch_related('book_set')
    return render(request, 'genres.html', {'genres': genres})


def blog(request):
    return render(request, 'blog.html')


@login_required
def reviews(request):
    all_reviews = Review.objects.select_related('book').order_by('-created_at')
    form = ReviewForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Review submitted.')
            return redirect('reviews')

    return render(request, 'reviews.html', {
        'form': form,
        'all_reviews': all_reviews,
    })


@login_required
def myshelf(request):
    user = request.user
    favourites = Favourite.objects.filter(user=user).select_related('book')
    favourite_books = [fav.book for fav in favourites]
    favourite_count = favourites.count()

    return render(request, 'myshelf.html', {
        'favourite_books': favourite_books,
        'favourite_count': favourite_count
    })


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

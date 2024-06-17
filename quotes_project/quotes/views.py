from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm, QuoteForm
from .models import Author, Quote


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:quotes-list')
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form, 'user': request.user})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.created_by = request.user
            quote.save()
            form.save_m2m()
            return redirect('quotes:quotes-list')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form, 'user': request.user})


def quotes_list(request):
    quotes = Quote.objects.all()
    return render(request, 'quotes/quotes_list.html', {'quotes': quotes, 'user': request.user})


def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    quotes = Quote.objects.filter(author=author)
    return render(request, 'quotes/author_detail.html', {'author': author, 'quotes': quotes})


# def quotes_list(request):
#     quotes = Quote.objects.all()
#     return render(request, 'quotes/quotes_list.html', {'quotes': quotes})

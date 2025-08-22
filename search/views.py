
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Document
from .forms import DocumentUploadForm, SearchForm
from .utils import search_in_document
import os


@login_required
def index(request):
    """صفحه اصلی"""
    upload_form = DocumentUploadForm()
    search_form = SearchForm()
    documents = Document.objects.filter(user=request.user).order_by('-uploaded_at')

    context = {
        'upload_form': upload_form,
        'search_form': search_form,
        'documents': documents
    }
    return render(request, 'search/index.html', context)


@login_required
def upload_document(request):
    """آپلود فایل جدید"""
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            messages.success(request, 'فایل با موفقیت آپلود شد.')
            return redirect('index')
        else:
            messages.error(request, 'خطا در آپلود فایل. لطفا مجددا تلاش کنید.')

    return redirect('index')


@login_required
def search_document(request):
    """جستجو در اسناد"""
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_term = search_form.cleaned_data['search_term']
            document_id = request.POST.get('document_id')

            try:
                document = Document.objects.get(id=document_id, user=request.user)
                file_path = document.file.path

                # جستجو در فایل
                results = search_in_document(file_path, search_term)

                context = {
                    'search_term': search_term,
                    'document': document,
                    'results': results,
                    'upload_form': DocumentUploadForm(),
                    'search_form': search_form,
                    'documents': Document.objects.filter(user=request.user).order_by('-uploaded_at')
                }

                if results:
                    messages.success(request, f'عبارت "{search_term}" در {len(results)} مکان پیدا شد.')
                else:
                    messages.warning(request, f'عبارت "{search_term}" در این فایل پیدا نشد.')

                return render(request, 'search/index.html', context)

            except Document.DoesNotExist:
                messages.error(request, 'فایل مورد نظر یافت نشد.')
            except Exception as e:
                messages.error(request, f'خطا در جستجو: {str(e)}')

    return redirect('index')


@login_required
def delete_document(request, document_id):
    """حذف سند"""
    if request.method == 'POST':
        try:
            document = Document.objects.get(id=document_id)

            # حذف فایل فیزیکی
            if os.path.exists(document.file.path):
                os.remove(document.file.path)

            # حذف رکورد از دیتابیس
            document.delete()
            messages.success(request, 'فایل با موفقیت حذف شد.')

        except Document.DoesNotExist:
            messages.error(request, 'فایل مورد نظر یافت نشد.')
        except Exception as e:
            messages.error(request, f'خطا در حذف فایل: {str(e)}')

    return redirect('index')
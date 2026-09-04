from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MangoUsersModelForm
from .models import MangoUsersModel


def mango_users_list(request):
    queryset = MangoUsersModel.objects.all()

    paginator = Paginator(queryset, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'mango_users': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'total_users': queryset.count(),
        'distinct_titles': queryset.values('title').distinct().count(),
        'average_age': queryset.aggregate(avg=Avg('age'))['avg'],
    }
    return render(request, 'mango/mangousers_list.html', context)


def mango_users_detail(request, pk):
    mango_user = get_object_or_404(MangoUsersModel, pk=pk)
    return render(request, 'mango/mangousers_detail.html', {'mango_user': mango_user})


def mango_users_create(request):
    if request.method == 'POST':
        form = MangoUsersModelForm(request.POST)
        if form.is_valid():
            mango_user = form.save()
            messages.success(request, f'User "{mango_user.name}" was created successfully.')
            return redirect('mango:mangousers_list')
    else:
        form = MangoUsersModelForm()
    return render(request, 'mango/mangousers_form.html', {'form': form, 'object': None})


def mango_users_update(request, pk):
    mango_user = get_object_or_404(MangoUsersModel, pk=pk)
    if request.method == 'POST':
        form = MangoUsersModelForm(request.POST, instance=mango_user)
        if form.is_valid():
            mango_user = form.save()
            messages.success(request, f'User "{mango_user.name}" was updated successfully.')
            return redirect('mango:mangousers_list')
    else:
        form = MangoUsersModelForm(instance=mango_user)
    return render(request, 'mango/mangousers_form.html', {'form': form, 'object': mango_user})


def mango_users_delete(request, pk):
    mango_user = get_object_or_404(MangoUsersModel, pk=pk)
    if request.method == 'POST':
        name = mango_user.name
        mango_user.delete()
        messages.success(request, f'User "{name}" was deleted successfully.')
        return redirect('mango:mangousers_list')
    return render(request, 'mango/mangousers_confirm_delete.html', {'mango_user': mango_user})

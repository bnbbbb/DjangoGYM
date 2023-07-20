from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy, reverse

# 아무나 접근 가능
class IndexMain(View):
    def get(self, request):
        profile = request.user
        context = {
            'title' : 'Index',
            'profile': profile
        }
        return render(request, 'index.html', context)
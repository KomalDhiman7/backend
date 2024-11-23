from django.shortcuts import render

# Create your views here.
def superheroes(request):
    return render(request,'superhero/all_superhero')

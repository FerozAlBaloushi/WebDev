from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.db.models import Avg

# Create your views here.
def home(request):
    query = request.GET.get("title")
    allMusics = None
    if query:
        allMusics = Music.objects.filter(name__icontains=query)
    else:
        allMusics = Music.objects.all()

    context = {
        "musics": allMusics,
    }

    return render(request, 'main/index.html', context)


# detail page
def detail(request, id):
    music = Music.objects.get(id=id) # select * from music where id=id
    reviews = Review.objects.filter(music=id).order_by("-comment")

    average = reviews.aggregate(Avg("rating"))["rating__avg"]
    if average == None:
        average = 0
    average = round(average, 2)
    context = {
        "music": music,
        "reviews": reviews,
        "average": average
    }
    return render(request, 'main/details.html', context)


# add musics to the database
def add_musics(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == "POST":
                form = MusicForm(request.POST or None)

                #check if the form is valid
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect("main:home")
            else:
                form = MusicForm()
            return render(request, 'main/addmusics.html', {"form": form, "controller": "Add Musics"})

        # if they are not admin
        else:
            return redirect("main:home")

    # if they are not Logged in
    return redirect("accounts:login")



# edit the musics
def edit_musics(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # get the musics linked with id
            music = Music.objects.get(id=id)

            # form check
            if request.method == "POST":
                form = MusicForm(request.POST or None, instance=music)
                # check if form is valid
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect("main:detail", id)
            else:
                form = MusicForm(instance=music)
            return render(request, 'main/addmusics.html', {"form": form, "controller": "Edit Musics"})

        # if they are not admin
        else:
            return redirect("main:home")

    # if they are not Logged in
    return redirect("accounts:login")


# delete the Musics
def delete_musics(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # get the musics
            music = Music.objects.get(id=id)

            # delete the Music
            music.delete()
            return redirect("main:home")

        # if they are not admin
        else:
            return redirect("main:home")

    # if they are not Logged in
    return redirect("accounts:login")


def add_review(request, id):
    if request.user.is_authenticated:
        music = Music.objects.get(id=id)
        if request.method == "POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.comment = request.POST["comment"]
                data.rating = request.POST["rating"]
                data.user = request.user
                data.music = music
                data.save()
                return redirect("main:detail", id)
        else:
            form = ReviewForm()
        return render(request, 'main/details.html', {"form": form})
    else:
        return redirect("accounts:login")


# edit the review
def edit_review(request, music_id, review_id):
    if request.user.is_authenticated:
        music = Music.objects.get(id=music_id)
        # Review
        review = Review.objects.get(music=music, id=review_id)

        # check if the review was done by logged user
        if request.user == review.user:
            # grant permission
            if request.method == "POST":
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    if (data.rating > 10) or (data.rating < 0):
                        error = "Out of range. Please select rating from 0 to 10."
                        return render(request, 'main/editreview.html', {"error": error, "form": form})
                    else:
                        data.save()
                        return redirect("main:detail", music_id)
            else:
                form = ReviewForm(instance=review)
            return render(request, 'main/editreview.html', {"form": form})
        else:
            return redirect("main:detail", music_id)
    else:
        return redirect("accounts:login")


# delete the review
def delete_review(request, music_id, review_id):
    if request.user.is_authenticated:
        music = Music.objects.get(id=music_id)
        # Review
        review = Review.objects.get(music=music, id=review_id)

        # check if the review was done by logged user
        if request.user == review.user:
            # grant permission to delete
            review.delete()

        return redirect("main:detail", music_id)
    else:
        return redirect("accounts:login")

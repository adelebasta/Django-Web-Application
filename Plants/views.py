from django.db.models.functions import Round
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PlantForm, CommentForm, SearchForm
from .models import Plant, Comment
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from Useradmin.models import MyUser
from django.contrib.auth.decorators import login_required
from Shoppingcart.models import ShoppingCart
from Shoppingcart.forms import ShoppingCartItemForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.db.models import Avg


@login_required(login_url='/useradmin/login/')
def plants_list(request):
    all_the_plants = Plant.objects.all()
    can_delete_or_edit = False
    if request.user.is_authenticated:
        myuser = MyUser.objects.get(id=request.user.id)
        if myuser.type == 'SU' or myuser.type == 'CS':
            can_delete_or_edit = True
    if request.method == "POST":
        form = ShoppingCartItemForm(request.POST)
        if form.is_valid():
            plant_id = form.cleaned_data['product_id']
            plant = Plant.objects.get(id=plant_id)
            ShoppingCart.add_item(myuser, plant)
    context = {'all_the_plants': all_the_plants,
               'can_delete_or_edit': can_delete_or_edit
               }
    return render(request, 'plants-list.html', context)


@login_required(login_url='/useradmin/login/')
def plant_detail(request, **kwargs):
    plant_id = kwargs['pk']
    that_one_plant = Plant.objects.get(id=plant_id)
    comments = Comment.objects.filter(plant=that_one_plant)
    myuser = MyUser.objects.get(id=request.user.id)
    can_delete_or_edit = False
    if myuser.can_modify():
        can_delete_or_edit = True
    if request.method == "POST":
        if 'add' in request.POST:
            ShoppingCart.add_item(myuser, that_one_plant)
        elif 'download' in request.POST:
           buffer = createpdf(that_one_plant)
           return FileResponse(buffer, as_attachment=True, filename="{}.pdf".format(that_one_plant.name))
        else:
            form = CommentForm(request.POST)
            form.instance.myuser = request.user
            form.instance.plant = that_one_plant
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
    for comment in comments:
        if comment.is_reported:
            if comment.is_reported_by_me(myuser):
                comment.is_reported_by_me = True

    context = {'that_one_plant': that_one_plant,
               'comments_for_that_one_plant': comments,
               'can_delete_or_edit': can_delete_or_edit,
               }
    user_comment = Comment.objects.filter(myuser=myuser,
                                         plant=that_one_plant)
    if len(user_comment) != 0:
        return render(request, 'plant-detail.html', context)

    context['comment_form'] = CommentForm
    context['myuser'] = myuser
    return render(request, 'plant-detail.html', context)


@login_required(login_url='/useradmin/login/')
def plant_edit(request, pk: str):
    plant_id = pk
    plant = Plant.objects.get(id=plant_id)
    if request.method == 'POST':
        if 'edit' in request.POST:
            form = PlantForm(request.POST, request.FILES)
            if form.is_valid():
                if form.cleaned_data['plant_picture']:
                    plant.plant_picture = form.cleaned_data['plant_picture']
                plant.name = form.cleaned_data['name']
                plant.description = form.cleaned_data['description']
                plant.sunlight = form.cleaned_data['sunlight']
                plant.size = form.cleaned_data['size']
                plant.price = form.cleaned_data['price']
                plant.timestamp = form.cleaned_data['timestamp']
                plant.save()
                return redirect('plant-detail', plant_id)

        elif 'delete' in request.POST:
            Plant.objects.get(id=plant_id).delete()

    elif request.method == 'GET':
        form = PlantForm(request.POST or None, request.FILES or None, instance=plant)
        context = {'form': form,
                   'that_one_plant': plant
                   }
        return render(request, 'plant-edit.html', context)


class PlantCreateView(LoginRequiredMixin, CreateView):
    login_url = '/useradmin/login/'
    model = Plant
    form_class = PlantForm
    template_name = 'plant-create.html'
    success_url = reverse_lazy('plants-list')

    def form_valid(self, form):
        form.instance.myuser = self.request.user
        return super().form_valid(form)


@login_required(login_url='/useradmin/login/')
def plant_delete(request, pk):
    obj = get_object_or_404(Plant, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('plants-list')
    context = {"plant": obj}
    return render(request, 'plant-delete.html', context)


@login_required(login_url='/useradmin/login/')
def vote(request, pk: str, up_or_down: str):
    plant = Plant.objects.get(id=int(pk))
    myuser = request.user
    plant.vote(myuser, up_or_down)
    return redirect('plant-detail', pk=pk)


@login_required(login_url='/useradmin/login/')
def plant_search(request):
    if request.method == 'POST':
        plants_found = Plant.objects.all().annotate(avg_rating=Avg('rated_plant__stars'))
        search_string_name = request.POST['name']
        if search_string_name:
            plants_found = Plant.objects.filter(name__contains=search_string_name).annotate(avg_rating=Avg('rated_plant__stars'))

        search_string_description = request.POST['description']
        if search_string_description:
            plants_found = plants_found.filter(description__contains=search_string_description).annotate(avg_rating=Avg('rated_plant__stars'))

        search_string_minimum_rating_value = request.POST.get('stars')
        if search_string_minimum_rating_value:
            plants_found = plants_found.filter(avg_rating__gte=search_string_minimum_rating_value)

        form_in_function_based_view = SearchForm()
        context = {'form': form_in_function_based_view,
                   'plants_found': plants_found,
                   'show_results': True}
        return render(request, 'plant-search.html', context)

    else:
        form_in_function_based_view = SearchForm()
        context = {'form': form_in_function_based_view,
                   'show_results': False}
        return render(request, 'plant-search.html', context)


@login_required(login_url='/useradmin/login/')
def vote_on_comment(request, ppk: int, cpk: int, up_or_down: str):
    comment = Comment.objects.get(id=cpk)
    user = MyUser.objects.get(id=request.user.id)
    comment.one_vote_per_user(user, up_or_down)
    return redirect('plant-detail', pk=ppk)


@login_required(login_url='/useradmin/login/')
def comment_delete(request, pk: str):
    comment_id = pk
    comment = Comment.objects.get(id=comment_id)
    comment.delete()

    return redirect('plant-detail', comment.plant_id)


@login_required(login_url='/useradmin/login/')
def report_comment(request, ppk: int, cpk: int):
    comment = Comment.objects.get(id=cpk)
    myuser = MyUser.objects.get(id=request.user.id)
    comment.report(myuser)
    return redirect('plant-detail', pk=ppk)


@staff_member_required(login_url='/useradmin/login/')
def clear_report(request, ppk: int, cpk: int):
    comment = Comment.objects.get(id=cpk)
    comment.clear_report()
    return redirect('plant-detail', pk=ppk)


def createpdf(plant):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(250, 800, plant.name)
    p.drawString(0, 700, plant.description)
    p.drawString(0, 680, "Size: {}".format(plant.size))
    p.drawString(0, 660, "Price: {}".format(plant.price))
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
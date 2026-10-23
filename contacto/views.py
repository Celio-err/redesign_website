# Create your views here.
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .models import Comment


def contacto(request):
    status = request.GET.get("status", "")
    qs = Comment.objects.all()
    if status == "unread":
            qs = qs.filter(is_read=False)
    elif status == "read":
            qs = qs.filter(is_read=True)
    
    q = request.GET.get("q", "").strip()
    if q:
            qs = qs.filter(body__icontains=q) | qs.filter(name__icontains=q)
    
    page = Paginator(qs, 20).get_page(request.GET.get("page"))
    return render(request, "contacto_list.html", {
            "page": page,
            "status": status,
            "q": q,
            "unread_count": Comment.objects.filter(is_read=False).count(),
    }) 

def _back(request):
    """Volta para a página anterior (só URLs do próprio site)."""
    nxt = request.POST.get("next", "")
    if nxt and url_has_allowed_host_and_scheme(nxt, request.get_host()):
        return redirect(nxt)
    return redirect(reverse("backend_comment_list"))

@require_POST
def comment_toggle_read(request, pk):
    c = get_object_or_404(Comment, pk=pk)
    c.is_read = not c.is_read
    c.save(update_fields=["is_read"])
    return _back(request)


@require_POST
def comment_delete(request, pk):
    get_object_or_404(Comment, pk=pk).delete()
    return _back(request)
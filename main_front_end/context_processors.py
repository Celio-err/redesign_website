from mandato_cfp.models import TipoMandato

from noticias.models import TipoNoticias
from dddo.models import TipoDDDO



def tipos_mandato(request):
    return {
        'tipos_mandato_menu': TipoMandato.objects.all().order_by('ordem')
    }

def tipos_noticias(request):
    return {
        'tipo_noticia_menu': TipoNoticias.objects.all().order_by('tipo_noticia')
    }



def tipos_dddo(request):
    return {
        'tipos_dddo_menu': TipoDDDO.objects.all().order_by('tipo_dddo')
    }
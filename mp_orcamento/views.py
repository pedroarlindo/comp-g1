from django.http import Http404
from django.shortcuts import render
from .models import *

# Create your views here.
def orcamentos_lista(request):
    # logica
    orcamentos = Orcamento.objects.all()
    return render(request, 'mp_orcamento/orcamentos.html', {'orcamentos': orcamentos})


def orcamentos_estatisticas(request):
    maior_custo = 0
    menor_custo = 999999999999
    orcamento_maior_custo = None
    orcamento_menor_custo = None
    orcamentos = Orcamento.objects.all()
    somatorio_custo_total = 0
    for orcamento in orcamentos:
        somatorio = 0
        for peca in Peca.objects.filter(orcamento=orcamento):
            """"
            area_frente = peca.largura * peca.altura
            area_lado = peca.altura * peca.profundidade
            area_total = area_frente + area_frente + area_lado + area_lado
            # converte de cm para m
            area_total = area_total / 100
            custo_de_producao = 0
            if peca.tipo_da_mobilia == 'compartimento de armário':
                custo_de_producao += 50 * area_total
            else:
                custo_de_producao += 75 * area_total
            if peca.tipo_do_puxador == 'plástico':
                custo_de_producao += 5
            else:
                custo_de_producao += 8.5
            if peca.pintura == 'acabamento PU':
                custo_de_producao += 15 * area_total
            elif peca.pintura == 'acabamento PU texturizado':
                custo_de_producao += 20 * area_total
            else:
                custo_de_producao += 35 * area_total
            custo_de_producao_ajustado = custo_de_producao * 1.75
            somatorio += custo_de_producao_ajustado
            """
            somatorio += peca.custo_de_producao_ajustado()
        orcamento.custo_total = somatorio * 1.25
        somatorio_custo_total += orcamento.custo_total
        if orcamento.custo_total >= maior_custo:
            orcamento_maior_custo = orcamento
            maior_custo = orcamento.custo_total
        if orcamento.custo_total <= menor_custo:
            orcamento_menor_custo = orcamento
            menor_custo = orcamento.custo_total
    quantidade = Orcamento.objects.count()
    media_custo_total = somatorio_custo_total / quantidade
    return render(request, 'mp_orcamento/estatisticas.html',
        {'quantidade': quantidade,
        'orcamento_maior_custo': orcamento_maior_custo,
        'orcamento_menor_custo': orcamento_menor_custo,
        'media_custo_total': media_custo_total
        })


def dados_cliente(request, id_cliente):
    try:
        primeiro_cliente = Cliente.objects.get(id=id_cliente)
        orcamentos = Orcamento.objects.filter(cliente=primeiro_cliente)
    except Cliente.DoesNotExist:
        raise Http404('O cliente informado não foi encontrado!')

    return render(request, 'mp_orcamento/dados-cliente.html', {'primeiro_cliente': primeiro_cliente, 'orcamentos': orcamentos})

def clientes_estatisticas(request):
    qtd_de_clientes = Cliente.objects.count();

    nome_cliente_maior = None # Guarda o nome do cliente com maior somatório de orçamento
    nome_cliente_menor = None # Guarda o nome do cliente com menor somatório de orçamento
    somatorio_cliente_maior = 0 # Guarda o maior somatório
    somatorio_cliente_menor = 99999999999999 # Guarda o menor somatório

    for cliente in Cliente.objects.all():
        somatorio = 0
        for orcamento in Orcamento.objects.filter(cliente=cliente):
            somatorio += orcamento.custo_total()

        if somatorio >= somatorio_cliente_maior:
            somatorio_cliente_maior = somatorio
            nome_cliente_maior = cliente.nome

        if somatorio <= somatorio_cliente_menor:
            somatorio_cliente_menor = somatorio
            nome_cliente_menor = cliente.nome

    return render(request, 'mp_orcamento/clientes-estatisticas.html',
    {'qtd_de_clientes': qtd_de_clientes,
    'nome_cliente_maior': nome_cliente_maior,
    'nome_cliente_menor': nome_cliente_menor,
    'somatorio_cliente_maior': somatorio_cliente_maior,
    'somatorio_cliente_menor': somatorio_cliente_menor
    })

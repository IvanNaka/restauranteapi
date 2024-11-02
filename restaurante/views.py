from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView

from restaurante.models import ItemMenu, Cliente, Mesa, StatusPedido, Pedido, PedidoItem, Pagamento


# Create your views here.
class CadastrarItem(APIView):
    def post(self, request):
        nome_item = self.request.POST.get('nome')
        descricao = self.request.POST.get('descricao')
        preco = self.request.POST.get('preco')
        categoria = self.request.POST.get('categoria')
        if not nome_item or not descricao or not preco or not categoria:
            return JsonResponse({'erro': 'Todos os campos devem ser preenchidos'}, status=400)
        item = ItemMenu(nome=nome_item, descricao=descricao, preco=preco, categoria=categoria)
        item.save()
        return JsonResponse(data={'status': True}, status=200)

class CadastrarMesa(APIView):
    def post(self, request):
        #adicionar logica pra salvar mesa (algo similar ao de cima)
        return JsonResponse()

class ListarMesa(APIView):
    def get(self, request):
        lista_mesas = list(Mesa.objects.all().values())
        return JsonResponse(data={'mesas': lista_mesas}, status=200)

class CadastrarCliente(APIView):
    def post(self, request):
        # adicionar logica pra salvar cliente (algo similar ao de item)
        return JsonResponse()

class CriarPedido(APIView):
    def post(self, request):
        # adicionar logica pra salvar pedido (algo similar ao de item)
        return JsonResponse()

class ListarPedido(APIView):
    def get(self, request):
        # listar pedidos exceto status cancelado (algo similar ao de listar mesas)
        # mas adicionar a propriedade exclude
        # exemplo: Pedido.objects.exclude(status__descricao='Cancelado')
        return JsonResponse()

class AlterarPedido(APIView):
    def post(self, request):
        # adicionar logica pra alterar pedido
        # 1 pegar no banco o valor com o id q vai vir do request
        # fazer alteracao do valor
        # salvar no banco
        return JsonResponse()

class AtualizarStatusPedido(APIView):
    def post(self, request):
        # adicionar logica pra atualizar status pedido
        # 1 pegar no banco o valor com o id q vai vir do request
        # fazer alteracao do valor
        # salvar no banco
        return JsonResponse()

class CancelarPedido(APIView):
    def post(self, request):
        # adicionar logica pra cancelar pedido
        # 1 pegar no banco o valor com o id q vai vir do request
        # fazer alteracao do valor
        # salvar no banco
        return JsonResponse()

class FecharPedido(APIView):
    def post(self, request):
        # adicionar logica pra fechar pedido
        # 1 pegar no banco o valor com o id q vai vir do request
        # fazer alteracao do valor
        # salvar no banco
        return JsonResponse()
class CalcularValorPedido(APIView):
    def get(self, request):
        #pegar o valor dos itens do pedido e somar
        return JsonResponse()

class DividirValorPedido(APIView):
    def post(self, request):
        # pegar o valor dos itens do pedido e somar e divir pelo numero de pessoas
        return JsonResponse()
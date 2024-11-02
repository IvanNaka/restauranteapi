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

from django.http import JsonResponse
from rest_framework.views import APIView
from restaurante.models import Cliente, Mesa, StatusPedido, Pedido, ItemMenu, PedidoItem

class CadastrarCliente(APIView):
    def post(self, request):
        nome = request.data.get('nome')
        telefone = request.data.get('telefone')
        email = request.data.get('email')

        # Validação das informações obrigatórias
        if not nome or not telefone or not email:
            return JsonResponse({'erro': 'Todos os campos devem ser preenchidos'}, status=400)

        try:
            cliente = Cliente.objects.create(nome=nome, telefone=telefone, email=email)
            return JsonResponse({
                'status': True,
                'mensagem': 'Cliente cadastrado com sucesso',
                'cliente_id': cliente.id
            }, status=201)

        except Exception as e:
            return JsonResponse({'erro': f'Erro ao cadastrar cliente: {str(e)}'}, status=500)

class CriarPedido(APIView):
    def post(self, request):
        cliente_id = request.data.get('cliente_id')
        mesa_id = request.data.get('mesa_id')
        itens = request.data.get('itens', [])

        if not cliente_id or not mesa_id or not itens:
            return JsonResponse({'erro': 'Cliente, mesa e itens são obrigatórios'}, status=400)

        try:
            cliente = Cliente.objects.get(id=cliente_id)
            mesa = Mesa.objects.get(id=mesa_id)
            status_pendente = StatusPedido.objects.get(descricao='Pendente')

            pedido = Pedido.objects.create(
                cliente=cliente,
                mesa=mesa,
                status=status_pendente
            )

            for item in itens:
                item_menu = ItemMenu.objects.get(id=item['item_id'])
                PedidoItem.objects.create(
                    pedido=pedido,
                    item_menu=item_menu,
                    quantidade=item['quantidade'],
                    preco_unitario=item_menu.preco
                )

            return JsonResponse({
                'status': True,
                'mensagem': 'Pedido criado com sucesso',
                'pedido_id': pedido.id
            }, status=201)

        except Cliente.DoesNotExist:
            return JsonResponse({'erro': 'Cliente não encontrado'}, status=404)
        except Mesa.DoesNotExist:
            return JsonResponse({'erro': 'Mesa não encontrada'}, status=404)
        except ItemMenu.DoesNotExist:
            return JsonResponse({'erro': 'Item do menu não encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'erro': f'Erro ao criar pedido: {str(e)}'}, status=500)

class ListarPedido(APIView):
    def get(self, request):
        # Listar pedidos, excluindo aqueles com status "Cancelado"
        pedidos = Pedido.objects.exclude(status__descricao='Cancelado').values(
            'id', 'cliente__nome', 'mesa__numero', 'status__descricao'
        )

        # Converter a QuerySet em uma lista
        pedidos_lista = list(pedidos)

        return JsonResponse({'lista_pedidos': pedidos_lista}, status=200)

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
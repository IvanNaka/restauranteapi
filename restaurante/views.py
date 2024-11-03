from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
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
    class AlterarPedido(APIView):
        def post(self, request, pedido_id):
            try:
                # Obtém o pedido pelo ID
                pedido = Pedido.objects.get(id=pedido_id)

                # Limpa os itens atuais do pedido
                PedidoItem.objects.filter(pedido=pedido).delete()

                # Obtém a lista de IDs dos novos itens e suas quantidades enviadas no request
                itens_data = request.data.get('itens', [])
                for item_data in itens_data:
                    item_id = item_data.get('id')
                    quantidade = item_data.get('quantidade', 1)

                    item = ItemMenu.objects.get(id=item_id)
                    PedidoItem.objects.create(
                        pedido=pedido,
                        item_menu=item,
                        quantidade=quantidade,
                        preco_unitario=item.preco
                    )

                return JsonResponse({"message": "Itens do pedido atualizados com sucesso."}, status=200)
            except Pedido.DoesNotExist:
                return JsonResponse({"error": "Pedido não encontrado."}, status=404)
            except ItemMenu.DoesNotExist:
                return JsonResponse({"error": "Item de menu não encontrado."}, status=404)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)

class AtualizarStatusPedido(APIView):
    def post(self, request, pedido_id):
        novo_status = request.POST.get('status')
        pedido = Pedido.objects.filter(id=pedido_id).first()

        if not pedido:
            return JsonResponse({'erro': 'Pedido não encontrado'}, status=404)

        try:
            status = StatusPedido.objects.get(descricao=novo_status)
            pedido.status = status
            pedido.save()
            return JsonResponse({'status': status.descricao}, status=200)
        except StatusPedido.DoesNotExist:
            return JsonResponse({'erro': 'Seu pedido não tem status, por favor entre em contato com a loja'}, status=404)

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
    def get(self, request, pedido_id):
        pedido = get_object_or_404(Pedido, id=pedido_id)

        total = sum(item.preco for item in pedido.itens.all())

        return JsonResponse({'valor_total': total}, status=200)


class DividirValorPedido(APIView):
    def post(self, request, pedido_id):
        try:
            # Obtém o pedido pelo ID
            pedido = Pedido.objects.get(id=pedido_id)

            # Calcula o valor total do pedido somando (preço unitário * quantidade) de cada item do pedido
            valor_total = sum(item.preco_unitario * item.quantidade for item in pedido.pedidoitem_set.all())

            # Obtém o número de pessoas enviado no request
            numero_pessoas = int(request.data.get('numero_pessoas', 1))
            if numero_pessoas <= 0:
                raise ValueError("O número de pessoas deve ser maior que zero.")

            # Calcula o valor por pessoa
            valor_por_pessoa = valor_total / numero_pessoas

            return JsonResponse({"valor_por_pessoa": round(valor_por_pessoa, 2)}, status=200)
        except Pedido.DoesNotExist:
            return JsonResponse({"error": "Pedido não encontrado."}, status=404)
        except (ValueError, ZeroDivisionError) as e:
            return JsonResponse({"error": str(e)}, status=400)
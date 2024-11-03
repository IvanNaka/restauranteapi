from django.http import JsonResponse
from rest_framework.views import APIView

from restaurante.models import ItemMenu, Cliente, Mesa, StatusPedido, Pedido, PedidoItem, Pagamento

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
        numero_mesa = request.POST.get('numero')
        capacidade_mesa = request.POST.get('capacidade')
        if not numero_mesa or not capacidade_mesa:
            return JsonResponse({'erro': 'Todos os campos devem ser preenchidos'}, status=400)
        if Mesa.objects.filter(numero=numero_mesa).exists():
            return JsonResponse({'erro': 'O número já está em uso'}, status=400)
        Mesa.objects.create(numero=numero_mesa, capacidade=capacidade_mesa)
        return JsonResponse({'status': 'Mesa cadastrada com sucesso'}, status=200)

class ListarMesa(APIView):
    def get(self, request):
        lista_mesas = list(Mesa.objects.all().values())
        return JsonResponse(data={'mesas': lista_mesas}, status=200)

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

        pedidos = Pedido.objects.exclude(status__descricao='Cancelado').values(
            'id', 'cliente__nome', 'mesa__numero', 'status__descricao'
        )

        pedidos_lista = list(pedidos)

        return JsonResponse({'lista_pedidos': pedidos_lista}, status=200)

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
        except Pedido.DoesNotExist:
            return JsonResponse({'erro': 'Pedido não encontrado'}, status=404)

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
        pedido = Pedido.objects.filter(id=pedido_id).first()
        if not pedido:
            return JsonResponse({'erro': 'Pedido não existe'}, status=404)

        total = sum(item.preco for item in pedido.pedidoitem_set.all())
        return JsonResponse({'valor_total': total}, status=200)

class DividirValorPedido(APIView):
    def post(self, request, pedido_id):
        try:
            pedido = Pedido.objects.get(id=pedido_id)
            valor_total = sum(item.preco_unitario * item.quantidade for item in pedido.pedidoitem_set.all())
            numero_pessoas = int(request.data.get('numero_pessoas', 1))
            if numero_pessoas <= 0:
                raise ValueError("O número de pessoas deve ser maior que zero.")
            valor_por_pessoa = valor_total / numero_pessoas

            return JsonResponse({"valor_por_pessoa": round(valor_por_pessoa, 2)}, status=200)
        except Pedido.DoesNotExist:
            return JsonResponse({"error": "Pedido não encontrado."}, status=404)
        except (ValueError, ZeroDivisionError) as e:
            return JsonResponse({"error": str(e)}, status=400)
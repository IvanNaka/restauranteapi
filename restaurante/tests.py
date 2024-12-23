import decimal
import json

from django.test import TestCase
from django.urls import reverse

import restaurante.models as models


class ItemCadastroTest(TestCase):
    def test_cadastrar_item_sucesso(self):
        response = self.client.post(reverse('cadastrar_item'), {
            'nome': 'Pizza',
            'descricao': 'Pizza de mussarela',
            'preco': 25.00,
            'categoria': 'Comida'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(models.ItemMenu.objects.filter(nome='Pizza').exists())

    def test_cadastrar_item_campos_obrigatorios_vazios(self):
        response = self.client.post(reverse('cadastrar_item'), {})
        self.assertEqual(response.status_code, 400)
        erro = json.loads(response.content).get('erro')
        self.assertEqual(erro, "Todos os campos devem ser preenchidos")


class MesaCadastroTest(TestCase):
    def test_cadastrar_mesa_sucesso(self):
        response = self.client.post(reverse('cadastrar_mesa'), {
            'numero': 1,
            'capacidade': 4
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(models.Mesa.objects.filter(numero=1).exists())

    def test_cadastrar_mesa_numero_existente(self):
        models.Mesa.objects.create(numero=10, capacidade=4)
        response = self.client.post(reverse('cadastrar_mesa'), {
            'numero': 10,
            'capacidade': 2
        })
        self.assertEqual(response.status_code, 400)
        erro = json.loads(response.content).get('erro')
        self.assertEqual(erro, "O número já está em uso")


class MesaListarTest(TestCase):
    def setUp(self):
        self.mesa1 = models.Mesa.objects.create(numero=1, capacidade=4)
        self.mesa2 = models.Mesa.objects.create(numero=2, capacidade=2)

    def test_listar_mesas(self):
        response = self.client.get(reverse('listar_mesas'))
        self.assertEqual(response.status_code, 200)
        mesas = json.loads(response.content).get('mesas')
        self.assertEqual(mesas[0].get('numero'), self.mesa1.numero)
        self.assertEqual(mesas[1].get('numero'), self.mesa2.numero)


class ClienteCadastroTest(TestCase):
    def test_cadastrar_cliente_sucesso(self):
        response = self.client.post(reverse('cadastrar_cliente'), {
            'nome': 'João',
            'telefone': '123456789',
            'email': 'joao@example.com'
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(models.Cliente.objects.filter(nome='João').exists())

    def test_cadastrar_cliente_email_repetido(self):
        models.Cliente.objects.create(nome='João', telefone='123456789', email='joao@example.com')
        response = self.client.post(reverse('cadastrar_cliente'), {
            'nome': 'Maria',
            'telefone': '987654321',
            'email': 'joao@example.com'
        })

        self.assertEqual(response.status_code, 400)
        erro = json.loads(response.content).get('erro')
        self.assertEqual("O e-mail já está em uso", erro)


class PedidoCriacaoTest(TestCase):
    def setUp(self):
        self.mesa = models.Mesa.objects.create(numero=1, capacidade=4)
        self.cliente = models.Cliente.objects.create(nome='João', telefone='123456789', email='joao@example.com')
        self.item = models.ItemMenu.objects.create(nome='Pizza', descricao='Pizza de mussarela', preco=25.00,
                                                   categoria='Comida')
        self.status_pendente = models.StatusPedido.objects.create(descricao='Pendente')

    def test_criar_pedido_sucesso(self):
        response = self.client.post(reverse('criar_pedido'), {
            'mesa_id': self.mesa.id,
            'cliente_id': self.cliente.id,
            'itens': [{'item_id': self.item.id, 'quantidade': 1}]
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(models.Pedido.objects.filter(cliente=self.cliente).exists())


class PedidoListarTest(TestCase):
    def setUp(self):
        self.mesa = models.Mesa.objects.create(numero=1, capacidade=4)
        self.mesa2 = models.Mesa.objects.create(numero=2, capacidade=4)
        self.cliente = models.Cliente.objects.create(nome='João', telefone='123456789', email='joao@example.com')
        self.cliente2 = models.Cliente.objects.create(nome='Maria', telefone='123456789', email='maria@example.com')
        self.status = models.StatusPedido.objects.create(descricao='Em preparo')
        self.status2 = models.StatusPedido.objects.create(descricao='Cancelado')
        self.pedido = models.Pedido.objects.create(cliente=self.cliente, mesa=self.mesa, status=self.status)
        self.pedido2 = models.Pedido.objects.create(cliente=self.cliente2, mesa=self.mesa2, status=self.status2)

    def test_listar_pedidos_ativos(self):
        response = self.client.get(reverse('listar_pedidos'))
        self.assertEqual(response.status_code, 200)
        lista_pedidos = json.loads(response.content).get('lista_pedidos')
        self.assertEqual(len(lista_pedidos), 1)


class PedidoAlterarTest(TestCase):
    def setUp(self):
        self.mesa = models.Mesa.objects.create(numero=1, capacidade=4)
        self.cliente = models.Cliente.objects.create(nome='João', telefone='123456789', email='joao@example.com')
        self.status = models.StatusPedido.objects.create(descricao='Em preparo')
        self.pedido = models.Pedido.objects.create(cliente=self.cliente, mesa=self.mesa, status=self.status)
        self.novo_item = models.ItemMenu.objects.create(nome='Pizza', descricao='Pizza de mussarela', preco=25.00,
                                                        categoria='Comida')

    def test_alterar_itens_pedido(self):
        itens = json.dumps([
            {'id': self.novo_item.id, 'quantidade': 2},
        ])
        response = self.client.post(reverse('alterar_pedido', args=[self.pedido.id]), {
            'itens': itens
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.PedidoItem.objects.filter(pedido=self.pedido).count(), 1)


class PedidoAtualizarStatusTest(TestCase):
    def setUp(self):
        self.mesa = models.Mesa.objects.create(numero=1, capacidade=4)
        self.cliente = models.Cliente.objects.create(nome='João', telefone='123456789', email='joao@example.com')
        self.status = models.StatusPedido.objects.create(descricao='Em preparo')
        self.status2 = models.StatusPedido.objects.create(descricao='Finalizado')
        self.pedido = models.Pedido.objects.create(cliente=self.cliente, mesa=self.mesa, status=self.status)

    def test_atualizar_status_pedido(self):
        response = self.client.post(reverse('atualizar_status', args=[self.pedido.id]), {
            'status': 'Finalizado'
        })
        self.assertEqual(response.status_code, 200)
        status = json.loads(response.content).get('status')
        self.assertEqual(status, 'Finalizado')


class PedidoCancelarTest(TestCase):
    def setUp(self):
        self.mesa = models.Mesa.objects.create(numero=1, capacidade=4)
        self.cliente = models.Cliente.objects.create(nome='João', telefone='123456789', email='joao@example.com')
        self.status = models.StatusPedido.objects.create(descricao='Em preparo')
        self.status2 = models.StatusPedido.objects.create(descricao='Cancelado')
        self.pedido = models.Pedido.objects.create(cliente=self.cliente, mesa=self.mesa, status=self.status)

    def test_cancelar_pedido(self):
        response = self.client.post(reverse('cancelar_pedido', args=[self.pedido.id]), {
            'status': 'Em preparo'
        })
        self.assertEqual(response.status_code, 200)
        status = json.loads(response.content).get('status')
        self.assertEqual(status, 'Cancelado')


class PedidoFecharTest(TestCase):
    def setUp(self):
        self.mesa = models.Mesa.objects.create(numero=1, capacidade=4)
        self.cliente = models.Cliente.objects.create(nome='João', telefone='123456789', email='joao@example.com')
        self.status = models.StatusPedido.objects.create(descricao='Entregue')
        self.status2 = models.StatusPedido.objects.create(descricao='Fechado')
        self.pedido = models.Pedido.objects.create(cliente=self.cliente, mesa=self.mesa, status=self.status)

    def test_fechar_pedido(self):
        response = self.client.post(reverse('fechar_pedido', args=[self.pedido.id]), {
            'status': 'Entregue'
        })
        self.assertEqual(response.status_code, 200)
        status = json.loads(response.content).get('status')
        self.assertEqual(status, 'Fechado')


class PedidoCalculoValorTotalTest(TestCase):
    def setUp(self):
        self.mesa = models.Mesa.objects.create(numero=1, capacidade=4)
        self.cliente = models.Cliente.objects.create(nome='João', telefone='123456789', email='joao@example.com')
        self.status = models.StatusPedido.objects.create(descricao='Entregue')
        self.pedido = models.Pedido.objects.create(cliente=self.cliente, mesa=self.mesa, status=self.status, )
        self.item1 = models.ItemMenu.objects.create(nome='Pizza', descricao='Pizza de mussarela', preco=25.00,
                                                    categoria='Comida')
        self.item2 = models.ItemMenu.objects.create(nome='Coca-Cola', descricao='Lata de Coca-Cola', preco=5.00,
                                                    categoria='Bebida')
        self.pedido_item1 = models.PedidoItem.objects.create(item_menu=self.item1, preco_unitario=25.00,
                                                             pedido=self.pedido, quantidade=2)
        self.pedido_item2 = models.PedidoItem.objects.create(item_menu=self.item2, preco_unitario=5.00,
                                                             pedido=self.pedido, quantidade=2)

    def test_calcular_valor_total_pedido(self):
        response = self.client.get(reverse('calcular_valor_total', args=[self.pedido.id]))
        self.assertEqual(response.status_code, 200)
        valor_total = decimal.Decimal(json.loads(response.content).get('valor_total'))
        self.assertEqual(valor_total, 60.00)


class PedidoDividirValorTest(TestCase):
    def setUp(self):
        self.mesa = models.Mesa.objects.create(numero=1, capacidade=4)
        self.cliente = models.Cliente.objects.create(nome='João', telefone='123456789', email='joao@example.com')
        self.status = models.StatusPedido.objects.create(descricao='Entregue')
        self.pedido = models.Pedido.objects.create(cliente=self.cliente, mesa=self.mesa, status=self.status, )
        self.item1 = models.ItemMenu.objects.create(nome='Pizza', descricao='Pizza de mussarela', preco=25.00,
                                                    categoria='Comida')
        self.item2 = models.ItemMenu.objects.create(nome='Coca-Cola', descricao='Lata de Coca-Cola', preco=5.00,
                                                    categoria='Bebida')
        self.pedido_item1 = models.PedidoItem.objects.create(item_menu=self.item1, preco_unitario=35.00,
                                                             pedido=self.pedido, quantidade=2)
        self.pedido_item2 = models.PedidoItem.objects.create(item_menu=self.item2, preco_unitario=5.00,
                                                             pedido=self.pedido, quantidade=2)

    def test_dividir_valor_pedido(self):
        response = self.client.post(reverse('dividir_valor', args=[self.pedido.id]), {
            'numero_pessoas': 4
        })
        self.assertEqual(response.status_code, 200)
        valor_pessoa = decimal.Decimal(json.loads(response.content).get('valor_por_pessoa'))
        self.assertEqual(valor_pessoa, 20.00)

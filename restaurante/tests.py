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
        self.assertEqual(response.status_code, 302)
        self.assertTrue(models.ItemMenu.objects.filter(nome='Pizza').exists())

    def test_cadastrar_item_campos_obrigatorios_vazios(self):
        response = self.client.post(reverse('cadastrar_item'), {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Todos os campos devem ser preenchidos")

class MesaCadastroTest(TestCase):
    def test_cadastrar_mesa_sucesso(self):
        response = self.client.post(reverse('cadastrar_mesa'), {
            'numero': 1,
            'capacidade': 4
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(models.Mesa.objects.filter(numero=1).exists())

    def test_cadastrar_mesa_numero_existente(self):
        models.Mesa.objects.create(numero=10, capacidade=4)
        response = self.client.post(reverse('cadastrar_mesa'), {
            'numero': 10,
            'capacidade': 2
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "O número já está em uso")

class MesaListarTest(TestCase):
    def setUp(self):
        models.Mesa.objects.create(numero=1, capacidade=4)
        models.Mesa.objects.create(numero=2, capacidade=2)

    def test_listar_mesas(self):
        response = self.client.get(reverse('listar_mesas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mesa 1')
        self.assertContains(response, 'Mesa 2')
class ClienteCadastroTest(TestCase):
    def test_cadastrar_cliente_sucesso(self):
        response = self.client.post(reverse('cadastrar_cliente'), {
            'nome': 'João',
            'telefone': '123456789',
            'email': 'joao@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(models.Cliente.objects.filter(nome='João').exists())

class PedidoCriacaoTest(TestCase):
    def setUp(self):
        self.mesa = models.Mesa.objects.create(numero=1, capacidade=4)
        self.cliente = models.Cliente.objects.create(nome='João', telefone='123456789', email='joao@example.com')
        self.item = models.Item.objects.create(nome='Pizza', descricao='Pizza de mussarela', preco=25.00, categoria='Comida')

    def test_criar_pedido_sucesso(self):
        response = self.client.post(reverse('criar_pedido'), {
            'mesa': self.mesa.id,
            'cliente': self.cliente.id,
            'itens': [self.item.id]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(models.Pedido.objects.filter(cliente=self.cliente).exists())
class PedidoListarTest(TestCase):
    def setUp(self):
        self.pedido = models.Pedido.objects.create(cliente=self.cliente, mesa=self.mesa)

    def test_listar_pedidos_ativos(self):
        response = self.client.get(reverse('listar_pedidos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.pedido.id)

class PedidoAlterarTest(TestCase):
    def test_alterar_itens_pedido(self):
        response = self.client.post(reverse('alterar_pedido', args=[self.pedido.id]), {
            'itens': [self.novo_item.id]
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.novo_item, self.pedido.itens.all())

class PedidoAtualizarStatusTest(TestCase):
    def test_atualizar_status_pedido(self):
        response = self.client.post(reverse('atualizar_status', args=[self.pedido.id]), {
            'status': 'Preparando'
        })
        self.assertEqual(response.status_code, 302)
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.status, 'Preparando')

class PedidoCancelarTest(TestCase):
    def test_cancelar_pedido(self):
        response = self.client.post(reverse('cancelar_pedido', args=[self.pedido.id]))
        self.assertEqual(response.status_code, 302)
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.status, 'Cancelado')

class PedidoFecharTest(TestCase):
    def test_fechar_pedido(self):
        response = self.client.post(reverse('fechar_pedido', args=[self.pedido.id]))
        self.assertEqual(response.status_code, 302)
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.status, 'Fechado')

class PedidoCalculoValorTotalTest(TestCase):
    def test_calcular_valor_total_pedido(self):
        response = self.client.get(reverse('calcular_valor_total', args=[self.pedido.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Total')

class PedidoDividirValorTest(TestCase):
    def test_dividir_valor_pedido(self):
        response = self.client.post(reverse('dividir_valor', args=[self.pedido.id]), {
            'numero_pessoas': 4
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Valor por pessoa')
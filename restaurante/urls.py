# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar_item/', views.CadastrarItem.as_view(), name='cadastrar_item'),
    path('cadastrar_mesa/', views.CadastrarMesa.as_view(), name='cadastrar_mesa'),
    path('listar_mesas /', views.ListarMesa.as_view(), name='listar_mesas'),
    path('cadastrar_cliente/', views.CadastrarCliente.as_view(), name='cadastrar_cliente'),
    path('criar_pedido/', views.CriarPedido.as_view(), name='criar_pedido'),
    path('listar_pedidos/', views.ListarPedido.as_view(), name='listar_pedidos'),
    path('alterar_pedido/', views.AlterarPedido.as_view(), name='alterar_pedido'),
    path('atualizar_status/', views.AtualizarStatusPedido.as_view(), name='atualizar_status'),
    path('cancelar_pedido/', views.CancelarPedido.as_view(), name='cancelar_pedido'),
    path('fechar_pedido/', views.FecharPedido.as_view(), name='fechar_pedido'),
    path('calcular_valor_total/', views.CalcularValorPedido.as_view(), name='calcular_valor_total'),
    path('dividir_valor/', views.DividirValorPedido.as_view(), name='dividir_valor'),
]
import React, { useState, useEffect } from 'react';
import { Plus, Search, Filter, Edit, Trash2, Check, X, Eye, ShoppingCart, DollarSign, Package, Users, TrendingUp, MoreHorizontal } from 'lucide-react';
import { salesService, clientService, productService } from '../services/services';
import { Button, Card, Badge, Skeleton, Alert } from '../components/ui';
import toast from 'react-hot-toast';

const Sales = () => {
  const [orders, setOrders] = useState([]);
  const [clients, setClients] = useState([]);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({});
  const [showModal, setShowModal] = useState(false);
  const [editingOrder, setEditingOrder] = useState(null);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  // Dados do formulário
  const [cart, setCart] = useState([]);
  const [formData, setFormData] = useState({
    client: '',
    status: 'pending',
    payment_status: 'pending',
    discount: '0',
    notes: '',
    shipping_address: '',
  });

  useEffect(() => {
    loadData();
    loadClients();
    loadProducts();
  }, [searchTerm, statusFilter]);

  const loadData = async () => {
    try {
      setLoading(true);
      const params = {};
      if (searchTerm) params.search = searchTerm;
      if (statusFilter) params.status = statusFilter;
      
      const [ordersData, statsData] = await Promise.all([
        salesService.getOrders(params),
        salesService.getOrdersSummary()
      ]);
      
      setOrders(ordersData.results || ordersData);
      setStats(statsData);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      toast.error('Erro ao carregar pedidos');
    } finally {
      setLoading(false);
    }
  };

  const loadClients = async () => {
    try {
      const response = await clientService.getAll();
      setClients(response.results || response);
    } catch (error) {
      console.error('Erro ao carregar clientes:', error);
    }
  };

  const loadProducts = async () => {
    try {
      const response = await productService.getProducts();
      setProducts(response.results || response);
    } catch (error) {
      console.error('Erro ao carregar produtos:', error);
    }
  };

  const handleAddToCart = (product) => {
    const existingItem = cart.find(item => item.product === product.id);
    
    if (existingItem) {
      setCart(cart.map(item => 
        item.product === product.id 
          ? { ...item, quantity: item.quantity + 1 }
          : item
      ));
    } else {
      setCart([...cart, {
        product: product.id,
        quantity: 1,
        unit_price: product.price,
        discount: '0',
      }]);
    }
    toast.success('Produto adicionado ao carrinho');
  };

  const handleRemoveFromCart = (index) => {
    setCart(cart.filter((_, i) => i !== index));
  };

  const handleCartUpdate = (index, field, value) => {
    const newCart = [...cart];
    newCart[index][field] = value;
    
    if (field === 'unit_price' || field === 'quantity' || field === 'discount') {
      const item = newCart[index];
      item.total = (item.unit_price * item.quantity) - parseFloat(item.discount || 0);
    }
    
    setCart(newCart);
  };

  const calculateSubtotal = () => {
    return cart.reduce((sum, item) => sum + (item.unit_price * item.quantity), 0);
  };

  const calculateDiscount = () => {
    return parseFloat(formData.discount) || 0;
  };

  const calculateTax = () => {
    const subtotal = calculateSubtotal();
    return subtotal * 0.10; // 10% de taxa
  };

  const calculateTotal = () => {
    const subtotal = calculateSubtotal();
    const discount = calculateDiscount();
    const tax = calculateTax();
    return subtotal - discount + tax;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.client) {
      toast.error('Selecione um cliente');
      return;
    }
    
    if (cart.length === 0) {
      toast.error('Adicione pelo menos um produto ao carrinho');
      return;
    }

    try {
      const orderData = {
        ...formData,
        client: parseInt(formData.client),
        order_items: cart,
      };

      if (editingOrder) {
        await salesService.updateOrder(editingOrder.id, orderData);
        toast.success('Pedido atualizado com sucesso!');
      } else {
        await salesService.createOrder(orderData);
        toast.success('Pedido criado com sucesso!');
      }
      
      resetForm();
      setShowModal(false);
      loadData();
    } catch (error) {
      console.error('Erro ao salvar pedido:', error);
      toast.error('Erro ao salvar pedido');
    }
  };

  const resetForm = () => {
    setFormData({
      client: '',
      status: 'pending',
      payment_status: 'pending',
      discount: '0',
      notes: '',
      shipping_address: '',
    });
    setCart([]);
    setEditingOrder(null);
  };

  const handleEdit = (order) => {
    setEditingOrder(order);
    setFormData({
      client: order.client,
      status: order.status,
      payment_status: order.payment_status,
      discount: order.discount.toString(),
      notes: order.notes || '',
      shipping_address: order.shipping_address || '',
    });
    setCart(order.order_items.map(item => ({
      product: item.product,
      quantity: item.quantity,
      unit_price: item.unit_price,
      discount: item.discount.toString(),
      total: item.total,
    })));
    setShowModal(true);
  };

  const handleView = (order) => {
    setSelectedOrder(order);
    setShowDetailModal(true);
  };

  const handleDelete = async (id) => {
    if (!confirm('Tem certeza que deseja excluir este pedido?')) return;
    
    try {
      await salesService.deleteOrder(id);
      toast.success('Pedido excluído com sucesso!');
      loadData();
    } catch (error) {
      console.error('Erro ao excluir pedido:', error);
      toast.error('Erro ao excluir pedido');
    }
  };

  const handleComplete = async (order) => {
    try {
      await salesService.completeOrder(order.id);
      toast.success('Pedido concluído com sucesso!');
      loadData();
    } catch (error) {
      console.error('Erro ao completar pedido:', error);
      toast.error(error.response?.data?.error || 'Erro ao completar pedido');
    }
  };

  const handleCancel = async (order) => {
    if (!confirm('Tem certeza que deseja cancelar este pedido?')) return;
    
    try {
      await salesService.cancelOrder(order.id);
      toast.success('Pedido cancelado com sucesso!');
      loadData();
    } catch (error) {
      console.error('Erro ao cancelar pedido:', error);
      toast.error(error.response?.data?.error || 'Erro ao cancelar pedido');
    }
  };

  const getStatusBadge = (status) => {
    const variants = {
      pending: { variant: 'warning', label: 'Pendente' },
      processing: { variant: 'info', label: 'Processando' },
      completed: { variant: 'success', label: 'Concluído' },
      cancelled: { variant: 'destructive', label: 'Cancelado' },
      delivered: { variant: 'success', label: 'Entregue' },
    };
    const statusInfo = variants[status] || variants.pending;
    return <Badge variant={statusInfo.variant}>{statusInfo.label}</Badge>;
  };

  const getPaymentStatusBadge = (status) => {
    const variants = {
      pending: { variant: 'warning', label: 'Pendente' },
      partial: { variant: 'info', label: 'Parcial' },
      paid: { variant: 'success', label: 'Pago' },
      overdue: { variant: 'destructive', label: 'Vencido' },
      cancelled: { variant: 'secondary', label: 'Cancelado' },
    };
    const statusInfo = variants[status] || variants.pending;
    return <Badge variant={statusInfo.variant}>{statusInfo.label}</Badge>;
  };

  if (loading && orders.length === 0) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-10 w-64" />
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map(i => <Skeleton key={i} className="h-24" />)}
        </div>
        <Skeleton className="h-96" />
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div className="space-y-1">
          <h1 className="text-3xl font-bold tracking-tight text-gray-900">Vendas</h1>
          <p className="text-gray-600">Gerencie seus pedidos e vendas</p>
        </div>
        <Button onClick={() => setShowModal(true)} className="w-full sm:w-auto">
          <Plus className="h-4 w-4 mr-2" />
          Novo Pedido
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total de Pedidos</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total_orders || 0}</p>
            </div>
            <ShoppingCart className="h-12 w-12 text-blue-500 bg-blue-50 rounded-lg p-3" />
          </div>
        </Card>
        
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Receita Total</p>
              <p className="text-2xl font-bold text-gray-900">
                R$ {stats.total_revenue?.toLocaleString('pt-BR', { minimumFractionDigits: 2 }) || '0,00'}
              </p>
            </div>
            <DollarSign className="h-12 w-12 text-green-500 bg-green-50 rounded-lg p-3" />
          </div>
        </Card>
        
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Pedidos Pendentes</p>
              <p className="text-2xl font-bold text-gray-900">{stats.pending_orders || 0}</p>
            </div>
            <Package className="h-12 w-12 text-yellow-500 bg-yellow-50 rounded-lg p-3" />
          </div>
        </Card>
        
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Produtos Vendidos</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total_items_sold || 0}</p>
            </div>
            <TrendingUp className="h-12 w-12 text-purple-500 bg-purple-50 rounded-lg p-3" />
          </div>
        </Card>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
          <input
            type="text"
            placeholder="Buscar pedidos..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">Todos os Status</option>
          <option value="pending">Pendente</option>
          <option value="processing">Processando</option>
          <option value="completed">Concluído</option>
          <option value="delivered">Entregue</option>
          <option value="cancelled">Cancelado</option>
        </select>
      </div>

      {/* Orders Table */}
      <Card padding="none">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Pedido</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cliente</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Pagamento</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {orders.map((order) => (
                <tr key={order.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">{order.order_number}</div>
                    <div className="text-sm text-gray-500">{order.item_count} itens</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">{order.client_detail?.name || 'N/A'}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {getStatusBadge(order.status)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {getPaymentStatusBadge(order.payment_status)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    R$ {parseFloat(order.total).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(order.created_at).toLocaleDateString('pt-BR')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                    <Button variant="ghost" size="sm" onClick={() => handleView(order)}>
                      <Eye className="h-4 w-4" />
                    </Button>
                    {order.status !== 'completed' && order.status !== 'cancelled' && (
                      <>
                        <Button variant="ghost" size="sm" onClick={() => handleComplete(order)}>
                          <Check className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="sm" onClick={() => handleCancel(order)}>
                          <X className="h-4 w-4" />
                        </Button>
                      </>
                    )}
                    <Button variant="ghost" size="sm" onClick={() => handleEdit(order)}>
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button variant="ghost" size="sm" onClick={() => handleDelete(order.id)}>
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </td>
                </tr>
              ))}
              {orders.length === 0 && (
                <tr>
                  <td colSpan="7" className="px-6 py-12 text-center text-gray-500">
                    Nenhum pedido encontrado
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Create/Edit Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-2xl font-bold text-gray-900">
                {editingOrder ? 'Editar Pedido' : 'Novo Pedido'}
              </h2>
            </div>
            
            <form onSubmit={handleSubmit} className="p-6 space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Cliente *
                  </label>
                  <select
                    value={formData.client}
                    onChange={(e) => setFormData({ ...formData, client: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    required
                  >
                    <option value="">Selecione um cliente</option>
                    {clients.map(client => (
                      <option key={client.id} value={client.id}>{client.name}</option>
                    ))}
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Status do Pedido
                  </label>
                  <select
                    value={formData.status}
                    onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="pending">Pendente</option>
                    <option value="processing">Processando</option>
                    <option value="completed">Concluído</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Status de Pagamento
                  </label>
                  <select
                    value={formData.payment_status}
                    onChange={(e) => setFormData({ ...formData, payment_status: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="pending">Pendente</option>
                    <option value="partial">Parcial</option>
                    <option value="paid">Pago</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Desconto (R$)
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.discount}
                    onChange={(e) => setFormData({ ...formData, discount: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Produtos
                  </label>
                  <div className="border border-gray-300 rounded-lg p-4 space-y-4 max-h-64 overflow-y-auto">
                    {cart.length === 0 ? (
                      <p className="text-gray-500 text-center py-8">
                        Adicione produtos ao carrinho
                      </p>
                    ) : (
                      cart.map((item, index) => {
                        const product = products.find(p => p.id === item.product);
                        return (
                          <div key={index} className="flex items-center gap-4 p-3 bg-gray-50 rounded-lg">
                            <div className="flex-1">
                              <p className="font-medium text-gray-900">{product?.name || 'Produto'}</p>
                              <p className="text-sm text-gray-500">
                                R$ {item.unit_price?.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                              </p>
                            </div>
                            <input
                              type="number"
                              min="1"
                              value={item.quantity}
                              onChange={(e) => handleCartUpdate(index, 'quantity', parseInt(e.target.value))}
                              className="w-20 px-2 py-1 border border-gray-300 rounded"
                            />
                            <input
                              type="number"
                              step="0.01"
                              value={item.unit_price}
                              onChange={(e) => handleCartUpdate(index, 'unit_price', parseFloat(e.target.value))}
                              className="w-32 px-2 py-1 border border-gray-300 rounded"
                              placeholder="Preço"
                            />
                            <span className="font-medium text-gray-900">
                              R$ {(item.unit_price * item.quantity).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                            </span>
                            <Button
                              type="button"
                              variant="ghost"
                              size="sm"
                              onClick={() => handleRemoveFromCart(index)}
                            >
                              <Trash2 className="h-4 w-4 text-red-500" />
                            </Button>
                          </div>
                        );
                      })
                    )}
                  </div>
                  
                  {/* Product Selection */}
                  <div className="mt-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Adicionar Produto
                    </label>
                    <select
                      onChange={(e) => {
                        if (e.target.value) {
                          const product = products.find(p => p.id === parseInt(e.target.value));
                          if (product) handleAddToCart(product);
                          e.target.value = '';
                        }
                      }}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">Selecione um produto</option>
                      {products.map(product => (
                        <option key={product.id} value={product.id}>
                          {product.name} - R$ {parseFloat(product.price).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Observações
                  </label>
                  <textarea
                    value={formData.notes}
                    onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                    rows="3"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
              
              {/* Totals */}
              <div className="border-t border-gray-200 pt-4">
                <div className="flex justify-between mb-2">
                  <span className="text-gray-600">Subtotal:</span>
                  <span className="font-medium">R$ {calculateSubtotal().toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</span>
                </div>
                <div className="flex justify-between mb-2">
                  <span className="text-gray-600">Desconto:</span>
                  <span className="font-medium text-red-600">
                    - R$ {calculateDiscount().toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                  </span>
                </div>
                <div className="flex justify-between mb-2">
                  <span className="text-gray-600">Taxa (10%):</span>
                  <span className="font-medium">R$ {calculateTax().toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</span>
                </div>
                <div className="flex justify-between text-lg font-bold border-t border-gray-200 pt-2">
                  <span>Total:</span>
                  <span>R$ {calculateTotal().toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</span>
                </div>
              </div>
              
              <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
                <Button type="button" variant="outline" onClick={() => { setShowModal(false); resetForm(); }}>
                  Cancelar
                </Button>
                <Button type="submit">
                  {editingOrder ? 'Atualizar' : 'Criar'} Pedido
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Detail Modal */}
      {showDetailModal && selectedOrder && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <Card className="max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-2xl font-bold text-gray-900">Detalhes do Pedido</h2>
              <p className="text-gray-600">{selectedOrder.order_number}</p>
            </div>
            
            <div className="p-6 space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-600">Cliente:</p>
                  <p className="font-medium text-gray-900">{selectedOrder.client_detail?.name}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Status:</p>
                  {getStatusBadge(selectedOrder.status)}
                </div>
                <div>
                  <p className="text-sm text-gray-600">Pagamento:</p>
                  {getPaymentStatusBadge(selectedOrder.payment_status)}
                </div>
                <div>
                  <p className="text-sm text-gray-600">Total:</p>
                  <p className="font-medium text-gray-900">
                    R$ {parseFloat(selectedOrder.total).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                  </p>
                </div>
              </div>
              
              <div>
                <h3 className="font-medium text-gray-900 mb-4">Itens do Pedido</h3>
                <div className="space-y-2">
                  {selectedOrder.order_items?.map((item, index) => (
                    <div key={index} className="flex justify-between p-3 bg-gray-50 rounded-lg">
                      <div>
                        <p className="font-medium">{item.product_detail?.name || item.product}</p>
                        <p className="text-sm text-gray-600">
                          Qtd: {item.quantity} x R$ {item.unit_price?.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                        </p>
                      </div>
                      <p className="font-medium">
                        R$ {parseFloat(item.total).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="flex justify-end">
                <Button onClick={() => setShowDetailModal(false)}>Fechar</Button>
              </div>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
};

export default Sales;



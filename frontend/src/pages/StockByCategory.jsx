import React, { useState, useEffect } from 'react';
import { Search, Package, AlertTriangle, CheckCircle, XCircle, TrendingUp, TrendingDown } from 'lucide-react';
import { productService } from '../services/services';
import Tabs from '../components/Tabs';
import CategorySummary from '../components/CategorySummary';
import ExportButton from '../components/ExportButton';
import DateRangeExport from '../components/DateRangeExport';
import toast from 'react-hot-toast';

const StockByCategory = () => {
  const [categories, setCategories] = useState([]);
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setIsLoading(true);
      const [categoriesResponse, productsResponse] = await Promise.all([
        productService.getCategories(),
        productService.getProducts()
      ]);
      
      setCategories(categoriesResponse.results || categoriesResponse);
      setProducts(productsResponse.results || productsResponse);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      toast.error('Erro ao carregar dados do estoque');
    } finally {
      setIsLoading(false);
    }
  };

  const getProductsByCategory = (categoryId) => {
    if (categoryId === 'all') {
      return products;
    }
    return products.filter(product => product.category === parseInt(categoryId));
  };

  const getFilteredProducts = (categoryId) => {
    let filtered = getProductsByCategory(categoryId);

    // Filtrar por busca
    if (searchTerm) {
      filtered = filtered.filter(product =>
        product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.sku.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.description?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    return filtered;
  };

  const getStockStatus = (product) => {
    if (product.quantity === 0) {
      return { status: 'Sem estoque', color: 'text-red-600', bgColor: 'bg-red-100', icon: XCircle };
    } else if (product.quantity <= product.min_quantity) {
      return { status: 'Estoque baixo', color: 'text-yellow-600', bgColor: 'bg-yellow-100', icon: AlertTriangle };
    } else {
      return { status: 'Normal', color: 'text-green-600', bgColor: 'bg-green-100', icon: CheckCircle };
    }
  };

  const getStockTrend = (product) => {
    // Simulação de tendência baseada na quantidade vs mínimo
    const ratio = product.quantity / product.min_quantity;
    if (ratio > 3) {
      return { trend: 'Alto', color: 'text-green-600', icon: TrendingUp };
    } else if (ratio < 1.5) {
      return { trend: 'Baixo', color: 'text-red-600', icon: TrendingDown };
    } else {
      return { trend: 'Estável', color: 'text-gray-600', icon: TrendingUp };
    }
  };

  const getCategoryStats = (categoryId) => {
    const categoryProducts = getProductsByCategory(categoryId);
    const totalProducts = categoryProducts.length;
    const outOfStock = categoryProducts.filter(p => p.quantity === 0).length;
    const lowStock = categoryProducts.filter(p => p.quantity > 0 && p.quantity <= p.min_quantity).length;
    const normalStock = totalProducts - outOfStock - lowStock;
    const totalValue = categoryProducts.reduce((sum, p) => sum + (p.quantity * parseFloat(p.price)), 0);
    
    return { totalProducts, outOfStock, lowStock, normalStock, totalValue };
  };

  const getAllStats = () => {
    const totalProducts = products.length;
    const outOfStock = products.filter(p => p.quantity === 0).length;
    const lowStock = products.filter(p => p.quantity > 0 && p.quantity <= p.min_quantity).length;
    const normalStock = totalProducts - outOfStock - lowStock;
    const totalValue = products.reduce((sum, p) => sum + (p.quantity * parseFloat(p.price)), 0);
    
    return { totalProducts, outOfStock, lowStock, normalStock, totalValue };
  };

  const renderProductTable = (productsToShow, categoryName = 'Todos') => {
    if (productsToShow.length === 0) {
      return (
        <div className="text-center py-12">
          <Package className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">Nenhum produto encontrado</h3>
          <p className="mt-1 text-sm text-gray-500">
            {searchTerm ? 'Tente ajustar sua busca.' : `Não há produtos na categoria ${categoryName}.`}
          </p>
        </div>
      );
    }

    return (
      <div className="space-y-4">
        {/* Header da Tabela */}
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-semibold text-gray-900">
            {categoryName} - {productsToShow.length} produto(s)
          </h3>
          <div className="text-sm text-gray-500">
            Valor total: R$ {productsToShow.reduce((sum, p) => sum + (p.quantity * parseFloat(p.price)), 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
          </div>
        </div>

        {/* Tabela */}
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Produto
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  SKU
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Preço
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Estoque Atual
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Estoque Mínimo
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Tendência
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Valor Total
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {productsToShow.map((product) => {
                const stockStatus = getStockStatus(product);
                const stockTrend = getStockTrend(product);
                const totalValue = product.quantity * parseFloat(product.price);
                
                return (
                  <tr key={product.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="p-2 rounded-lg bg-blue-100">
                          <Package className="h-4 w-4 text-blue-600" />
                        </div>
                        <div className="ml-3">
                          <div className="text-sm font-medium text-gray-900">
                            {product.name}
                          </div>
                          <div className="text-sm text-gray-500">
                            {product.description?.substring(0, 50)}...
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {product.sku}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      R$ {parseFloat(product.price).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <span className={`font-semibold ${stockStatus.color}`}>
                        {product.quantity}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {product.min_quantity}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${stockStatus.bgColor} ${stockStatus.color}`}>
                        <stockStatus.icon className="h-3 w-3 mr-1" />
                        {stockStatus.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center text-xs font-medium ${stockTrend.color}`}>
                        <stockTrend.icon className="h-3 w-3 mr-1" />
                        {stockTrend.trend}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      R$ {totalValue.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  const renderStatsCards = () => {
    const stats = activeTab === 'all' ? getAllStats() : getCategoryStats(parseInt(activeTab));
    
    return (
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <Package className="h-8 w-8 text-blue-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Total</p>
              <p className="text-2xl font-bold text-gray-900">{stats.totalProducts}</p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <CheckCircle className="h-8 w-8 text-green-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Normal</p>
              <p className="text-2xl font-bold text-gray-900">{stats.normalStock}</p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <AlertTriangle className="h-8 w-8 text-yellow-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Estoque Baixo</p>
              <p className="text-2xl font-bold text-gray-900">{stats.lowStock}</p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <XCircle className="h-8 w-8 text-red-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Sem Estoque</p>
              <p className="text-2xl font-bold text-gray-900">{stats.outOfStock}</p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center">
            <TrendingUp className="h-8 w-8 text-purple-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Valor Total</p>
              <p className="text-lg font-bold text-gray-900">
                R$ {stats.totalValue.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  const filteredProducts = getFilteredProducts(activeTab);
  const currentCategory = activeTab === 'all' ? 'Todos' : categories.find(c => c.id === parseInt(activeTab))?.name || 'Categoria';

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Estoque por Categoria</h1>
          <p className="mt-1 text-sm text-gray-500">
            Visualize o estoque organizado por categorias
          </p>
        </div>
        <div className="flex gap-3">
          <ExportButton type="products">
            Exportar Produtos
          </ExportButton>
          <DateRangeExport type="movements">
            Exportar Movimentações
          </DateRangeExport>
        </div>
      </div>

      {/* Stats Cards */}
      {renderStatsCards()}

      {/* Category Summaries */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Resumo por Categoria</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {categories.map((category) => {
            const categoryProducts = getProductsByCategory(category.id);
            return (
              <CategorySummary
                key={category.id}
                category={category}
                products={categoryProducts}
                isActive={activeTab === category.id.toString()}
              />
            );
          })}
        </div>
      </div>

      {/* Search */}
      <div className="bg-white p-4 rounded-lg shadow">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          <input
            type="text"
            placeholder={`Buscar produtos em ${currentCategory.toLowerCase()}...`}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10 pr-4 py-2 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      {/* Tabs */}
      <Tabs
        categories={categories}
        activeTab={activeTab}
        onTabChange={setActiveTab}
      >
        {renderProductTable(filteredProducts, currentCategory)}
      </Tabs>
    </div>
  );
};

export default StockByCategory;
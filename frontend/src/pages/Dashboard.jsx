import React, { useState, useEffect } from 'react';
import { 
  Package, 
  TrendingUp, 
  AlertTriangle, 
  DollarSign,
  Activity,
  ArrowUpRight,
  ArrowDownRight
} from 'lucide-react';
import { dashboardService } from '../services/services';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [chartsData, setChartsData] = useState(null);
  const [recentActivity, setRecentActivity] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [statsData, chartsDataResponse, activityData] = await Promise.all([
          dashboardService.getStats(),
          dashboardService.getChartsData(),
          dashboardService.getRecentActivity(),
        ]);

        setStats(statsData);
        setChartsData(chartsDataResponse);
        setRecentActivity(activityData);
      } catch (error) {
        console.error('Erro ao carregar dados do dashboard:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  const statCards = [
    {
      name: 'Total de Produtos',
      value: stats?.products?.total || 0,
      icon: Package,
      color: 'bg-blue-500',
    },
    {
      name: 'Valor do Estoque',
      value: `R$ ${stats?.stock_value?.toLocaleString('pt-BR', { minimumFractionDigits: 2 }) || '0,00'}`,
      icon: DollarSign,
      color: 'bg-green-500',
    },
    {
      name: 'Estoque Baixo',
      value: stats?.products?.low_stock || 0,
      icon: AlertTriangle,
      color: 'bg-yellow-500',
    },
    {
      name: 'Sem Estoque',
      value: stats?.products?.out_of_stock || 0,
      icon: TrendingUp,
      color: 'bg-red-500',
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          Visão geral do seu sistema de estoque
        </p>
      </div>

      {/* Cards de estatísticas */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {statCards.map((card) => (
          <div key={card.name} className="card">
            <div className="flex items-center">
              <div className={`p-3 rounded-lg ${card.color}`}>
                <card.icon className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">{card.name}</p>
                <p className="text-2xl font-semibold text-gray-900">{card.value}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Gráficos */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Gráfico de movimentações */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Movimentações (30 dias)</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartsData?.daily_movements || []}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Line 
                  type="monotone" 
                  dataKey="quantity" 
                  stroke="#3b82f6" 
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Gráfico de produtos por categoria */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Produtos por Categoria</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartsData?.products_by_category || []}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="product_count" fill="#10b981" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Atividade recente */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Movimentações recentes */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Movimentações Recentes</h3>
          <div className="space-y-3">
            {recentActivity?.recent_movements?.map((movement) => (
              <div key={movement.id} className="flex items-center space-x-3">
                <div className={`p-2 rounded-full ${
                  movement.movement_type === 'Entrada' ? 'bg-green-100' : 'bg-red-100'
                }`}>
                  {movement.movement_type === 'Entrada' ? (
                    <ArrowUpRight className="h-4 w-4 text-green-600" />
                  ) : (
                    <ArrowDownRight className="h-4 w-4 text-red-600" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {movement.product_name}
                  </p>
                  <p className="text-sm text-gray-500">
                    {movement.movement_type} - {movement.quantity} unidades
                  </p>
                </div>
                <div className="text-sm text-gray-500">
                  {new Date(movement.created_at).toLocaleDateString('pt-BR')}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Produtos recentes */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Produtos Adicionados Recentemente</h3>
          <div className="space-y-3">
            {recentActivity?.recent_products?.map((product) => (
              <div key={product.id} className="flex items-center space-x-3">
                <div className="p-2 rounded-full bg-blue-100">
                  <Package className="h-4 w-4 text-blue-600" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {product.name}
                  </p>
                  <p className="text-sm text-gray-500">
                    {product.category_name} - R$ {product.price.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                  </p>
                </div>
                <div className="text-sm text-gray-500">
                  {new Date(product.created_at).toLocaleDateString('pt-BR')}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;



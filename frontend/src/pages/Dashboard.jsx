import React, { useState, useEffect } from 'react';
import { 
  Package, 
  TrendingUp, 
  AlertTriangle, 
  DollarSign,
  Activity,
  ArrowUpRight,
  ArrowDownRight,
  Wifi,
  WifiOff,
  Download,
  Plus,
  MoreHorizontal,
  Eye,
  Edit,
  Trash2,
  BarChart3,
  Users,
  ShoppingCart,
  Calendar,
  Clock,
  CheckCircle,
  XCircle,
  Info
} from 'lucide-react';
import { dashboardService } from '../services/services';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import { usePWA } from '../hooks/usePWA';
import { 
  Button, 
  Card, 
  Badge, 
  Skeleton, 
  Alert, 
  Avatar,
  Progress,
  Separator,
  DropdownMenu
} from '../components/ui';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [chartsData, setChartsData] = useState(null);
  const [recentActivity, setRecentActivity] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const { isOnline, canInstall, installPWA, updateAvailable, updatePWA } = usePWA();

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setError(null);
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
        setError('Erro ao carregar dados do dashboard. Tente novamente.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const handleInstallPWA = async () => {
    const installed = await installPWA();
    if (installed) {
      console.log('PWA instalado com sucesso!');
    }
  };

  const handleUpdatePWA = () => {
    updatePWA();
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        {/* Header skeleton */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="space-y-2">
            <Skeleton className="h-8 w-48" />
            <Skeleton className="h-4 w-64" />
          </div>
          <div className="flex items-center gap-3">
            <Skeleton className="h-8 w-24" />
            <Skeleton className="h-8 w-32" />
          </div>
        </div>

        {/* Cards skeleton */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {Array.from({ length: 4 }).map((_, i) => (
            <Card key={i} className="p-6">
              <div className="flex items-center justify-between">
                <div className="space-y-2">
                  <Skeleton className="h-4 w-24" />
                  <Skeleton className="h-8 w-16" />
                </div>
                <Skeleton className="h-12 w-12 rounded-lg" />
              </div>
            </Card>
          ))}
        </div>

        {/* Charts skeleton */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
          {Array.from({ length: 2 }).map((_, i) => (
            <Card key={i} className="p-6">
              <Skeleton className="h-6 w-32 mb-4" />
              <Skeleton className="h-64 w-full" />
            </Card>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-4">
        <Alert variant="destructive">
          <XCircle className="h-4 w-4" />
          <div>
            <h4 className="font-medium">Erro ao carregar dados</h4>
            <p className="text-sm mt-1">{error}</p>
          </div>
        </Alert>
        <Button onClick={() => window.location.reload()} className="w-full sm:w-auto">
          Tentar novamente
        </Button>
      </div>
    );
  }

  const statCards = [
    {
      name: 'Total de Produtos',
      value: stats?.products?.total || 0,
      icon: Package,
      color: 'bg-blue-500',
      change: '+12%',
      changeType: 'positive',
      trend: [1, 3, 2, 4, 3, 5, 4],
    },
    {
      name: 'Valor do Estoque',
      value: `R$ ${stats?.stock_value?.toLocaleString('pt-BR', { minimumFractionDigits: 2 }) || '0,00'}`,
      icon: DollarSign,
      color: 'bg-green-500',
      change: '+8%',
      changeType: 'positive',
      trend: [2, 4, 3, 5, 4, 6, 5],
    },
    {
      name: 'Estoque Baixo',
      value: stats?.products?.low_stock || 0,
      icon: AlertTriangle,
      color: 'bg-yellow-500',
      change: '-3%',
      changeType: 'negative',
      trend: [5, 4, 3, 2, 3, 2, 1],
    },
    {
      name: 'Sem Estoque',
      value: stats?.products?.out_of_stock || 0,
      icon: TrendingUp,
      color: 'bg-red-500',
      change: '+2%',
      changeType: 'negative',
      trend: [1, 2, 1, 3, 2, 4, 3],
    },
  ];

  const pieData = [
    { name: 'Em Estoque', value: 75, color: '#22c55e' },
    { name: 'Estoque Baixo', value: 15, color: '#f59e0b' },
    { name: 'Sem Estoque', value: 10, color: '#ef4444' },
  ];

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header moderno */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div className="space-y-1">
          <h1 className="text-3xl font-bold tracking-tight text-foreground">
            Dashboard
          </h1>
          <p className="text-muted-foreground">
          Visão geral do seu sistema de estoque
        </p>
      </div>

        <div className="flex items-center gap-3">
          {/* Status de conexão */}
          <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-muted/50">
            {isOnline ? (
              <Wifi className="h-4 w-4 text-green-500" />
            ) : (
              <WifiOff className="h-4 w-4 text-red-500" />
            )}
            <span className="text-sm font-medium">
              {isOnline ? 'Online' : 'Offline'}
            </span>
          </div>
          
          {/* Botão de instalação PWA */}
          {canInstall && (
            <Button
              variant="outline"
              size="sm"
              onClick={handleInstallPWA}
              className="hover-lift"
            >
              <Download className="h-4 w-4 mr-2" />
              Instalar App
            </Button>
          )}
          
          {/* Botão de atualização */}
          {updateAvailable && (
            <Button
              variant="default"
              size="sm"
              onClick={handleUpdatePWA}
              className="gradient-primary hover-glow"
            >
              Atualizar
            </Button>
          )}
        </div>
      </div>

      {/* Alertas de status */}
      {!isOnline && (
        <Alert variant="warning" className="animate-slide-in">
          <Info className="h-4 w-4" />
          <div>
            <h4 className="font-medium">Modo Offline</h4>
            <p className="text-sm mt-1">
              Você está offline. Algumas funcionalidades podem estar limitadas.
            </p>
          </div>
        </Alert>
      )}

      {/* Cards de estatísticas modernos */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((card, index) => (
          <Card 
            key={card.name} 
            variant="elevated" 
            className="relative overflow-hidden hover-lift group animate-slide-in"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <div className="p-6">
              <div className="flex items-center justify-between">
                <div className="space-y-2">
                  <p className="text-sm font-medium text-muted-foreground">
                    {card.name}
                  </p>
                  <p className="text-2xl font-bold text-foreground">
                    {card.value}
                  </p>
                  <div className="flex items-center gap-2">
                    <Badge 
                      variant={card.changeType === 'positive' ? 'success' : 'destructive'}
                      className="text-xs"
                    >
                      {card.change}
                    </Badge>
                    <span className="text-xs text-muted-foreground">vs mês anterior</span>
                  </div>
                </div>
                
                <div className={`p-3 rounded-xl ${card.color} shadow-lg group-hover:scale-110 transition-transform duration-200`}>
                <card.icon className="h-6 w-6 text-white" />
                </div>
              </div>
              
              {/* Mini gráfico de tendência */}
              <div className="mt-4 h-8 flex items-end gap-1">
                {card.trend.map((value, i) => (
                  <div
                    key={i}
                    className="flex-1 bg-primary/20 rounded-sm hover:bg-primary/30 transition-colors"
                    style={{ height: `${(value / 6) * 100}%` }}
                  />
                ))}
              </div>
            </div>
            
            {/* Gradiente de fundo */}
            <div className="absolute inset-0 bg-gradient-to-br from-transparent to-primary/5 opacity-0 group-hover:opacity-100 transition-opacity duration-200" />
          </Card>
        ))}
      </div>

      {/* Gráficos modernos */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        {/* Gráfico de movimentações */}
        <Card variant="elevated" className="animate-slide-in-left">
          <div className="p-6">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-lg font-semibold text-foreground">
                  Movimentações
                </h3>
                <p className="text-sm text-muted-foreground">
                  Últimos 30 dias
                </p>
              </div>
              <Badge variant="outline" className="flex items-center gap-1">
                <BarChart3 className="h-3 w-3" />
                Tendência
              </Badge>
            </div>
            
            <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartsData?.daily_movements || []}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis 
                    dataKey="day" 
                    stroke="hsl(var(--muted-foreground))"
                    fontSize={12}
                  />
                  <YAxis 
                    stroke="hsl(var(--muted-foreground))"
                    fontSize={12}
                  />
                  <Tooltip 
                    contentStyle={{
                      backgroundColor: 'hsl(var(--popover))',
                      border: '1px solid hsl(var(--border))',
                      borderRadius: '8px',
                      boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
                    }}
                  />
                <Line 
                  type="monotone" 
                  dataKey="quantity" 
                    stroke="hsl(var(--primary))" 
                    strokeWidth={3}
                    dot={{ fill: 'hsl(var(--primary))', strokeWidth: 2, r: 4 }}
                    activeDot={{ r: 6, stroke: 'hsl(var(--primary))', strokeWidth: 2 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
          </div>
        </Card>

        {/* Gráfico de pizza */}
        <Card variant="elevated" className="animate-slide-in-right">
          <div className="p-6">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-lg font-semibold text-foreground">
                  Status do Estoque
                </h3>
                <p className="text-sm text-muted-foreground">
                  Distribuição atual
                </p>
              </div>
              <Badge variant="outline" className="flex items-center gap-1">
                <Activity className="h-3 w-3" />
                Atual
              </Badge>
        </div>

            <div className="h-80 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                <Tooltip />
                </PieChart>
            </ResponsiveContainer>
            </div>
            
            {/* Legenda */}
            <div className="flex justify-center gap-6 mt-4">
              {pieData.map((item) => (
                <div key={item.name} className="flex items-center gap-2">
                  <div 
                    className="w-3 h-3 rounded-full" 
                    style={{ backgroundColor: item.color }}
                  />
                  <span className="text-sm text-muted-foreground">{item.name}</span>
                </div>
              ))}
            </div>
          </div>
        </Card>
      </div>

      {/* Atividade recente moderna */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Movimentações recentes */}
        <Card variant="elevated" className="animate-slide-in-left">
          <div className="p-6">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-lg font-semibold text-foreground">
                  Movimentações Recentes
                </h3>
                <p className="text-sm text-muted-foreground">
                  Últimas atividades
                </p>
              </div>
              <Button variant="ghost" size="sm">
                <Eye className="h-4 w-4 mr-2" />
                Ver todas
              </Button>
            </div>
            
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {recentActivity?.recent_movements?.length > 0 ? (
                recentActivity.recent_movements.map((movement, index) => (
                  <div 
                    key={movement.id} 
                    className="flex items-center gap-4 p-4 rounded-lg hover:bg-muted/50 transition-colors group"
                    style={{ animationDelay: `${index * 50}ms` }}
                  >
                <div className={`p-2 rounded-full ${
                  movement.movement_type === 'Entrada' ? 'bg-green-100' : 'bg-red-100'
                    } group-hover:scale-110 transition-transform duration-200`}>
                  {movement.movement_type === 'Entrada' ? (
                    <ArrowUpRight className="h-4 w-4 text-green-600" />
                  ) : (
                    <ArrowDownRight className="h-4 w-4 text-red-600" />
                  )}
                </div>
                    
                <div className="flex-1 min-w-0">
                      <p className="font-medium text-foreground truncate">
                    {movement.product_name}
                  </p>
                      <p className="text-sm text-muted-foreground">
                        {movement.movement_type} • {movement.quantity} unidades
                  </p>
                </div>
                    
                    <div className="text-right">
                      <p className="text-sm font-medium text-foreground">
                  {new Date(movement.created_at).toLocaleDateString('pt-BR')}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {new Date(movement.created_at).toLocaleTimeString('pt-BR', { 
                          hour: '2-digit', 
                          minute: '2-digit' 
                        })}
                      </p>
                    </div>
                    
                    <DropdownMenu
                      trigger={
                        <Button variant="ghost" size="sm" className="opacity-0 group-hover:opacity-100 transition-opacity">
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      }
                      items={[
                        { label: 'Ver detalhes', icon: <Eye className="h-4 w-4" />, onClick: () => {} },
                        { label: 'Editar', icon: <Edit className="h-4 w-4" />, onClick: () => {} },
                        { label: 'Excluir', icon: <Trash2 className="h-4 w-4" />, onClick: () => {} },
                      ]}
                    />
                  </div>
                ))
              ) : (
                <div className="text-center py-12 text-muted-foreground">
                  <Activity className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p className="font-medium">Nenhuma movimentação recente</p>
                  <p className="text-sm">As movimentações aparecerão aqui</p>
                </div>
              )}
              </div>
          </div>
        </Card>

        {/* Produtos recentes */}
        <Card variant="elevated" className="animate-slide-in-right">
          <div className="p-6">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-lg font-semibold text-foreground">
                  Produtos Recentes
                </h3>
                <p className="text-sm text-muted-foreground">
                  Adicionados recentemente
                </p>
              </div>
              <Button variant="ghost" size="sm">
                <Plus className="h-4 w-4 mr-2" />
                Adicionar
              </Button>
                </div>
            
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {recentActivity?.recent_products?.length > 0 ? (
                recentActivity.recent_products.map((product, index) => (
                  <div 
                    key={product.id} 
                    className="flex items-center gap-4 p-4 rounded-lg hover:bg-muted/50 transition-colors group"
                    style={{ animationDelay: `${index * 50}ms` }}
                  >
                    <Avatar className="h-10 w-10">
                      <Package className="h-5 w-5" />
                    </Avatar>
                    
                <div className="flex-1 min-w-0">
                      <p className="font-medium text-foreground truncate">
                    {product.name}
                  </p>
                      <p className="text-sm text-muted-foreground">
                        {product.category_name} • R$ {product.price.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                  </p>
                </div>
                    
                    <div className="text-right">
                      <p className="text-sm font-medium text-foreground">
                  {new Date(product.created_at).toLocaleDateString('pt-BR')}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {new Date(product.created_at).toLocaleTimeString('pt-BR', { 
                          hour: '2-digit', 
                          minute: '2-digit' 
                        })}
                      </p>
                    </div>
                    
                    <DropdownMenu
                      trigger={
                        <Button variant="ghost" size="sm" className="opacity-0 group-hover:opacity-100 transition-opacity">
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      }
                      items={[
                        { label: 'Ver detalhes', icon: <Eye className="h-4 w-4" />, onClick: () => {} },
                        { label: 'Editar', icon: <Edit className="h-4 w-4" />, onClick: () => {} },
                        { label: 'Excluir', icon: <Trash2 className="h-4 w-4" />, onClick: () => {} },
                      ]}
                    />
                  </div>
                ))
              ) : (
                <div className="text-center py-12 text-muted-foreground">
                  <Package className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p className="font-medium">Nenhum produto adicionado</p>
                  <p className="text-sm">Os produtos aparecerão aqui</p>
                </div>
              )}
              </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;



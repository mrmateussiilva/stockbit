import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Package, 
  TrendingUp, 
  BarChart3,
  Users,
  Truck,
  Tag,
  Settings,
  LogOut,
  ChevronLeft,
  ChevronRight,
  Sparkles,
  ShoppingCart
} from 'lucide-react';
import { useAuth } from '../services/AuthContext';
import { useSidebar } from '../services/SidebarContext';
import { Button, Avatar, Badge } from '../components/ui';

const Sidebar = () => {
  const location = useLocation();
  const { logout, user } = useAuth();
  const { isCollapsed, toggleSidebar } = useSidebar();

  const navigation = [
    { name: 'Dashboard', href: '/', icon: LayoutDashboard, badge: null },
    { name: 'Vendas', href: '/sales', icon: ShoppingCart, badge: null },
    { name: 'Produtos', href: '/products', icon: Package, badge: '12' },
    { name: 'Categorias', href: '/categories', icon: Tag, badge: null },
    { name: 'Estoque', href: '/stock', icon: TrendingUp, badge: '3' },
    { name: 'Estoque por Categoria', href: '/stock-category', icon: BarChart3, badge: null },
    { name: 'Clientes', href: '/clients', icon: Users, badge: '5' },
    { name: 'Fornecedores', href: '/suppliers', icon: Truck, badge: null },
    { name: 'Configurações', href: '/settings', icon: Settings, badge: null },
  ];

  const handleLogout = async () => {
    await logout();
  };

  return (
    <aside 
      className={`hidden lg:flex lg:flex-col lg:fixed lg:inset-y-0 lg:z-50 transition-all duration-300 relative ${
        isCollapsed ? 'lg:w-20' : 'lg:w-72'
      }`}
      role="navigation"
      aria-label="Navegação principal"
    >
      <div className="flex flex-col h-full bg-white border-r border-gray-200 pt-6 pb-4 shadow-lg relative overflow-hidden">
        {/* Header da sidebar */}
        <div className={`flex items-center flex-shrink-0 px-2 mb-2 ${isCollapsed ? 'justify-center' : 'justify-between'}`}>
          <div className="flex items-center">
            <div className="gradient-primary p-2.5 rounded-xl shadow-md">
              <Sparkles className="h-5 w-5 text-white" />
            </div>
            {!isCollapsed && (
              <div className="ml-3">
                <h1 className="text-xl font-bold text-gray-900">
                  Stockbit
                </h1>
                <p className="text-xs text-gray-500">
                  Sistema de Estoque
                </p>
              </div>
            )}
          </div>
          {!isCollapsed && (
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleSidebar}
              className="hover:bg-gray-100 rounded-lg"
              aria-label="Recolher sidebar"
            >
              <ChevronLeft className="h-5 w-5 text-gray-600" />
            </Button>
          )}
        </div>
        
        {/* Botão para expandir quando recolhida */}
        {isCollapsed && (
          <div className="absolute top-6 right-0 transform translate-x-3/4 z-10">
            <Button
              variant="default"
              size="icon"
              onClick={toggleSidebar}
              className="h-10 w-10 bg-white shadow-lg hover:bg-blue-50 border-2 border-blue-100 hover:border-blue-200 rounded-full transition-all"
              aria-label="Expandir sidebar"
            >
              <ChevronRight className="h-5 w-5 text-blue-600" />
            </Button>
          </div>
        )}
        
        {/* Navegação principal */}
        <nav className="mt-2 flex-1 px-2 space-y-1 overflow-y-auto" role="navigation" aria-label="Menu principal">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`
                  group flex items-center text-sm font-medium rounded-xl transition-all duration-200
                  ${isActive 
                    ? 'bg-blue-50 text-blue-600 shadow-sm' 
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                  }
                  ${isCollapsed ? 'justify-center px-2 py-3' : 'px-3 py-3'}
                `}
                title={isCollapsed ? item.name : ''}
                aria-current={isActive ? 'page' : undefined}
                aria-label={isCollapsed ? item.name : undefined}
              >
                <item.icon 
                  className={`h-5 w-5 ${isCollapsed ? '' : 'mr-3'} transition-transform duration-200 ${isActive ? 'text-blue-600' : 'text-gray-500 group-hover:text-gray-900'}`}
                  aria-hidden="true"
                />
                {!isCollapsed && (
                  <div className="flex items-center justify-between flex-1">
                    <span className="truncate">{item.name}</span>
                    {item.badge && (
                      <Badge variant="secondary" className="ml-2 text-xs bg-blue-100 text-blue-700">
                        {item.badge}
                      </Badge>
                    )}
                  </div>
                )}
              </Link>
            );
          })}
        </nav>

        {/* Footer da sidebar */}
        <div className="flex-shrink-0 px-2 pt-4 space-y-2 border-t border-gray-200">
          {/* Informações do usuário */}
          {!isCollapsed && user && (
            <div className="px-3 py-3 rounded-xl bg-gray-50 mb-3">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-primary">
                  <span className="text-xs font-semibold text-white">
                    {user.first_name?.[0]}{user.last_name?.[0]}
                  </span>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {user.first_name} {user.last_name}
                  </p>
                  <p className="text-xs text-gray-500 truncate">
                    {user.email}
                  </p>
                </div>
              </div>
            </div>
          )}
          
          {!isCollapsed && (
            <Button
              variant="ghost"
              onClick={handleLogout}
              className="w-full justify-start text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-xl"
              aria-label="Sair do sistema"
            >
              <LogOut className="h-4 w-4 mr-3" />
              <span>Sair</span>
            </Button>
          )}
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;


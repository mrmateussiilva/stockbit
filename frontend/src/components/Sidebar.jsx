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
  ChevronRight
} from 'lucide-react';
import { useAuth } from '../services/AuthContext';
import { useSidebar } from '../services/SidebarContext';

const Sidebar = () => {
  const location = useLocation();
  const { logout } = useAuth();
  const { isCollapsed, toggleSidebar } = useSidebar();

  const navigation = [
    { name: 'Dashboard', href: '/', icon: LayoutDashboard },
    { name: 'Produtos', href: '/products', icon: Package },
    { name: 'Categorias', href: '/categories', icon: Tag },
    { name: 'Estoque', href: '/stock', icon: TrendingUp },
    { name: 'Estoque por Categoria', href: '/stock-category', icon: BarChart3 },
    { name: 'Clientes', href: '/clients', icon: Users },
    { name: 'Fornecedores', href: '/suppliers', icon: Truck },
    { name: 'Configurações', href: '/settings', icon: Settings },
  ];

  const handleLogout = async () => {
    await logout();
  };

  return (
    <div className={`hidden lg:flex lg:flex-col lg:fixed lg:inset-y-0 lg:z-50 transition-all duration-300 ${
      isCollapsed ? 'lg:w-16' : 'lg:w-64'
    }`}>
      <div className="flex flex-col flex-grow bg-white border-r border-gray-200 pt-5 pb-4 overflow-y-auto">
        <div className={`flex items-center flex-shrink-0 px-4 ${isCollapsed ? 'justify-center' : 'justify-between'}`}>
          <div className="flex items-center">
            <div className="bg-primary-600 p-2 rounded-lg">
              <Package className="h-6 w-6 text-white" />
            </div>
            {!isCollapsed && (
              <h1 className="ml-3 text-xl font-bold text-gray-900">Tecidos & Papéis</h1>
            )}
          </div>
          {!isCollapsed && (
            <button
              onClick={toggleSidebar}
              className="p-1 rounded-lg hover:bg-gray-100 transition-colors duration-200"
              title="Recolher sidebar"
            >
              <ChevronLeft className="h-5 w-5 text-gray-600" />
            </button>
          )}
        </div>
        
        <nav className="mt-8 flex-1 px-2 space-y-1">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`sidebar-item ${isActive ? 'active' : ''} ${
                  isCollapsed ? 'justify-center' : ''
                }`}
                title={isCollapsed ? item.name : ''}
              >
                <item.icon className={`h-5 w-5 ${isCollapsed ? '' : 'mr-3'}`} />
                {!isCollapsed && item.name}
              </Link>
            );
          })}
        </nav>

        <div className="flex-shrink-0 px-2 py-4 space-y-2">
          {/* Botão para expandir quando recolhida */}
          {isCollapsed && (
            <button
              onClick={toggleSidebar}
              className="w-full flex items-center justify-center px-3 py-2 text-gray-700 rounded-lg hover:bg-gray-100 transition-colors duration-200"
              title="Expandir sidebar"
            >
              <ChevronRight className="h-5 w-5" />
            </button>
          )}
          
          <button
            onClick={handleLogout}
            className={`w-full flex items-center px-3 py-2 text-gray-700 rounded-lg hover:bg-gray-100 transition-colors duration-200 ${
              isCollapsed ? 'justify-center' : ''
            }`}
            title={isCollapsed ? 'Sair' : ''}
          >
            <LogOut className={`h-5 w-5 ${isCollapsed ? '' : 'mr-3'}`} />
            {!isCollapsed && 'Sair'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;


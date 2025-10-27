import React, { useState } from 'react';
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
  Menu,
  X,
  ChevronDown
} from 'lucide-react';
import { useAuth } from '../services/AuthContext';
import { Button } from '../design-system/components';

const MobileNavigation = () => {
  const location = useLocation();
  const { logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);

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
    setIsOpen(false);
  };

  const toggleMenu = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
  };

  const closeMenu = () => {
    setIsOpen(false);
    document.body.style.overflow = 'unset';
  };

  return (
    <>
      {/* Botão do menu mobile */}
      <div className="lg:hidden fixed top-4 left-4 z-50">
        <Button
          variant="outline"
          size="sm"
          onClick={toggleMenu}
          className="bg-white shadow-lg"
          aria-label="Abrir menu de navegação"
        >
          <Menu className="h-5 w-5" />
        </Button>
      </div>

      {/* Overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={closeMenu}
          aria-hidden="true"
        />
      )}

      {/* Menu mobile */}
      <div className={`
        fixed top-0 left-0 h-full w-80 bg-white shadow-xl z-50 transform transition-transform duration-300 ease-in-out lg:hidden
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        {/* Header do menu */}
        <div className="flex items-center justify-between p-4 border-b border-neutral-200">
          <div className="flex items-center">
            <div className="bg-primary-600 p-2 rounded-lg">
              <Package className="h-6 w-6 text-white" />
            </div>
            <h1 className="ml-3 text-xl font-bold text-neutral-900">
              Stockbit
            </h1>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={closeMenu}
            aria-label="Fechar menu"
          >
            <X className="h-5 w-5" />
          </Button>
        </div>

        {/* Navegação */}
        <nav className="flex-1 overflow-y-auto py-4">
          <div className="px-4 space-y-2">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  onClick={closeMenu}
                  className={`
                    flex items-center px-3 py-3 text-neutral-700 rounded-lg transition-colors duration-200
                    ${isActive 
                      ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600' 
                      : 'hover:bg-neutral-100'
                    }
                  `}
                  aria-current={isActive ? 'page' : undefined}
                >
                  <item.icon className="h-5 w-5 mr-3" aria-hidden="true" />
                  <span className="font-medium">{item.name}</span>
                </Link>
              );
            })}
          </div>
        </nav>

        {/* Footer do menu */}
        <div className="border-t border-neutral-200 p-4">
          <Button
            variant="ghost"
            onClick={handleLogout}
            className="w-full justify-start text-neutral-700 hover:bg-neutral-100"
          >
            <Settings className="h-5 w-5 mr-3" aria-hidden="true" />
            <span>Sair</span>
          </Button>
        </div>
      </div>
    </>
  );
};

// Componente de navegação inferior para mobile
export const BottomNavigation = () => {
  const location = useLocation();

  const bottomNavItems = [
    { name: 'Dashboard', href: '/', icon: LayoutDashboard },
    { name: 'Produtos', href: '/products', icon: Package },
    { name: 'Estoque', href: '/stock', icon: TrendingUp },
    { name: 'Clientes', href: '/clients', icon: Users },
  ];

  return (
    <div className="lg:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-neutral-200 z-40">
      <div className="grid grid-cols-4 h-16">
        {bottomNavItems.map((item) => {
          const isActive = location.pathname === item.href;
          return (
            <Link
              key={item.name}
              to={item.href}
              className={`
                flex flex-col items-center justify-center text-xs font-medium transition-colors duration-200
                ${isActive 
                  ? 'text-primary-600' 
                  : 'text-neutral-500 hover:text-neutral-700'
                }
              `}
              aria-current={isActive ? 'page' : undefined}
            >
              <item.icon 
                className={`h-5 w-5 mb-1 ${isActive ? 'text-primary-600' : 'text-neutral-500'}`} 
                aria-hidden="true"
              />
              <span className="truncate">{item.name}</span>
            </Link>
          );
        })}
      </div>
    </div>
  );
};

// Componente de navegação rápida
export const QuickActions = () => {
  const [isOpen, setIsOpen] = useState(false);

  const quickActions = [
    { name: 'Adicionar Produto', href: '/products/new', icon: Package },
    { name: 'Nova Entrada', href: '/stock/movement/new?type=in', icon: TrendingUp },
    { name: 'Nova Saída', href: '/stock/movement/new?type=out', icon: TrendingUp },
    { name: 'Novo Cliente', href: '/clients/new', icon: Users },
  ];

  return (
    <div className="lg:hidden fixed bottom-20 right-4 z-40">
      {/* Botão principal */}
      <Button
        variant="primary"
        size="lg"
        onClick={() => setIsOpen(!isOpen)}
        className="rounded-full shadow-lg"
        aria-label="Ações rápidas"
      >
        <Menu className="h-6 w-6" />
      </Button>

      {/* Menu de ações rápidas */}
      {isOpen && (
        <div className="absolute bottom-16 right-0 space-y-2 min-w-48">
          {quickActions.map((action) => (
            <Link
              key={action.name}
              to={action.href}
              onClick={() => setIsOpen(false)}
              className="flex items-center px-4 py-3 bg-white rounded-lg shadow-lg border border-neutral-200 text-neutral-700 hover:bg-neutral-50 transition-colors"
            >
              <action.icon className="h-5 w-5 mr-3 text-primary-600" />
              <span className="font-medium">{action.name}</span>
            </Link>
          ))}
        </div>
      )}

      {/* Overlay para fechar */}
      {isOpen && (
        <div 
          className="fixed inset-0 z-30"
          onClick={() => setIsOpen(false)}
          aria-hidden="true"
        />
      )}
    </div>
  );
};

export default MobileNavigation;


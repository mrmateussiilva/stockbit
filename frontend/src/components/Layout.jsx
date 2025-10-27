import React, { useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import Navbar from '../components/Navbar';
import MobileNavigation, { BottomNavigation, QuickActions } from '../components/MobileNavigation';
import { useSidebar } from '../services/SidebarContext';

const Layout = () => {
  const { isCollapsed } = useSidebar();

  // Melhorar acessibilidade - anunciar mudanças na sidebar
  useEffect(() => {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = isCollapsed ? 'Sidebar recolhida' : 'Sidebar expandida';
    document.body.appendChild(announcement);
    
    // Remover após um tempo
    setTimeout(() => {
      document.body.removeChild(announcement);
    }, 1000);
  }, [isCollapsed]);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Skip link para navegação por teclado */}
      <a 
        href="#main-content" 
        className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 z-50 bg-primary-600 text-white px-4 py-2 rounded-lg"
      >
        Pular para o conteúdo principal
      </a>
      
      {/* Sidebar desktop */}
      <Sidebar />
      
      {/* Navegação mobile */}
      <MobileNavigation />
      
      <div 
        className={`transition-all duration-300 ${isCollapsed ? 'lg:pl-20' : 'lg:pl-72'}`}
        role="main"
        id="main-content"
        tabIndex="-1"
      >
        <Navbar />
        <main 
          className="py-6 pb-20 lg:pb-6" 
          aria-label="Conteúdo principal"
        >
          <div className="w-[95%] mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
      
      {/* Navegação inferior mobile */}
      <BottomNavigation />
      
      {/* Ações rápidas mobile */}
      <QuickActions />
      
      {/* Indicador de carregamento para screen readers */}
      <div 
        id="loading-indicator" 
        className="sr-only" 
        aria-live="polite" 
        aria-label="Status de carregamento"
      />
    </div>
  );
};

export default Layout;



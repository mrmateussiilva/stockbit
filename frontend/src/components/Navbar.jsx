import React, { useState } from 'react';
import { Bell, User, Menu, X } from 'lucide-react';
import { useAuth } from '../services/AuthContext';

const Navbar = () => {
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const { user } = useAuth();

  return (
    <div className="sticky top-0 z-40 bg-white border-b border-gray-200 shadow-sm">
      <div className="flex h-16 items-center gap-x-4 px-4 sm:gap-x-6 sm:px-6 lg:px-8">
        <button
          type="button"
          className="-m-2.5 p-2.5 text-gray-700 lg:hidden"
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
        >
          <span className="sr-only">Abrir sidebar</span>
          {isMobileMenuOpen ? (
            <X className="h-6 w-6" aria-hidden="true" />
          ) : (
            <Menu className="h-6 w-6" aria-hidden="true" />
          )}
        </button>

        <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
          <div className="flex flex-1"></div>
          <div className="flex items-center gap-x-4 lg:gap-x-6">
            <button
              type="button"
              className="relative -m-2.5 p-2.5 text-gray-500 hover:text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <span className="sr-only">Ver notificações</span>
              <Bell className="h-5 w-5" aria-hidden="true" />
              <span className="absolute top-1 right-1 block h-2 w-2 rounded-full bg-red-500 ring-2 ring-white"></span>
            </button>

            <div className="hidden lg:block h-8 w-px bg-gray-200" />

            <div className="relative">
              <button
                type="button"
                className="-m-1.5 flex items-center gap-3 p-1.5 rounded-lg hover:bg-gray-50 transition-colors"
                onClick={() => setIsProfileOpen(!isProfileOpen)}
              >
                <span className="sr-only">Abrir menu do usuário</span>
                <div className="h-9 w-9 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center shadow-sm">
                  <span className="text-sm font-semibold text-white">
                    {user?.first_name?.[0]}{user?.last_name?.[0]}
                  </span>
                </div>
                <span className="hidden lg:block text-left">
                  <span className="block text-sm font-semibold text-gray-900" aria-hidden="true">
                    {user?.first_name} {user?.last_name}
                  </span>
                  <span className="text-xs text-gray-500">{user?.email}</span>
                </span>
              </button>

              {isProfileOpen && (
                <div className="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-lg bg-white py-2 shadow-lg ring-1 ring-gray-900/5 focus:outline-none border border-gray-200">
                  <a
                    href="#"
                    className="block px-4 py-2 text-sm leading-6 text-gray-700 hover:bg-gray-50 transition-colors"
                  >
                    Perfil
                  </a>
                  <a
                    href="#"
                    className="block px-4 py-2 text-sm leading-6 text-gray-700 hover:bg-gray-50 transition-colors"
                  >
                    Configurações
                  </a>
                  <div className="border-t border-gray-100 my-1"></div>
                  <a
                    href="#"
                    className="block px-4 py-2 text-sm leading-6 text-red-600 hover:bg-red-50 transition-colors"
                  >
                    Sair
                  </a>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Navbar;


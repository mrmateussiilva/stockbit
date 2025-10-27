import { useState, useEffect } from 'react';

// Hook para gerenciar PWA
export const usePWA = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [isInstalled, setIsInstalled] = useState(false);
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [updateAvailable, setUpdateAvailable] = useState(false);

  useEffect(() => {
    // Detectar mudanças no status da conexão
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Detectar se o app está instalado
    const checkIfInstalled = () => {
      const isStandalone = window.matchMedia('(display-mode: standalone)').matches;
      const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
      const isInStandaloneMode = ('standalone' in window.navigator) && window.navigator.standalone;
      
      setIsInstalled(isStandalone || (isIOS && isInStandaloneMode));
    };

    checkIfInstalled();

    // Detectar prompt de instalação
    const handleBeforeInstallPrompt = (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);

    // Detectar se o app foi instalado
    const handleAppInstalled = () => {
      setIsInstalled(true);
      setDeferredPrompt(null);
    };

    window.addEventListener('appinstalled', handleAppInstalled);

    // Registrar service worker
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js')
        .then((registration) => {
          console.log('Service Worker registrado com sucesso:', registration);
          
          // Verificar atualizações
          registration.addEventListener('updatefound', () => {
            const newWorker = registration.installing;
            if (newWorker) {
              newWorker.addEventListener('statechange', () => {
                if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                  setUpdateAvailable(true);
                }
              });
            }
          });
        })
        .catch((error) => {
          console.error('Erro ao registrar Service Worker:', error);
        });
    }

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
      window.removeEventListener('appinstalled', handleAppInstalled);
    };
  }, []);

  // Instalar PWA
  const installPWA = async () => {
    if (!deferredPrompt) {
      return false;
    }

    try {
      const result = await deferredPrompt.prompt();
      console.log('Resultado do prompt de instalação:', result);
      
      const choiceResult = await result.userChoice;
      console.log('Escolha do usuário:', choiceResult);
      
      setDeferredPrompt(null);
      return choiceResult.outcome === 'accepted';
    } catch (error) {
      console.error('Erro ao instalar PWA:', error);
      return false;
    }
  };

  // Atualizar PWA
  const updatePWA = async () => {
    if ('serviceWorker' in navigator) {
      const registration = await navigator.serviceWorker.getRegistration();
      if (registration && registration.waiting) {
        registration.waiting.postMessage({ type: 'SKIP_WAITING' });
        window.location.reload();
      }
    }
  };

  // Verificar se pode instalar
  const canInstall = !isInstalled && deferredPrompt !== null;

  return {
    isOnline,
    isInstalled,
    canInstall,
    updateAvailable,
    installPWA,
    updatePWA,
  };
};

// Hook para notificações push
export const useNotifications = () => {
  const [permission, setPermission] = useState(Notification.permission);
  const [isSupported, setIsSupported] = useState('Notification' in window);

  useEffect(() => {
    if (isSupported) {
      setPermission(Notification.permission);
    }
  }, [isSupported]);

  const requestPermission = async () => {
    if (!isSupported) {
      return false;
    }

    try {
      const result = await Notification.requestPermission();
      setPermission(result);
      return result === 'granted';
    } catch (error) {
      console.error('Erro ao solicitar permissão de notificação:', error);
      return false;
    }
  };

  const showNotification = (title, options = {}) => {
    if (permission !== 'granted' || !isSupported) {
      return false;
    }

    try {
      const notification = new Notification(title, {
        icon: '/icons/icon-192x192.png',
        badge: '/icons/badge-72x72.png',
        ...options,
      });

      notification.onclick = () => {
        window.focus();
        notification.close();
      };

      return true;
    } catch (error) {
      console.error('Erro ao mostrar notificação:', error);
      return false;
    }
  };

  return {
    permission,
    isSupported,
    canRequest: permission === 'default',
    requestPermission,
    showNotification,
  };
};

// Hook para sincronização offline
export const useOfflineSync = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [pendingSync, setPendingSync] = useState([]);

  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      // Executar sincronização quando voltar online
      if (pendingSync.length > 0) {
        syncPendingData();
      }
    };

    const handleOffline = () => {
      setIsOnline(false);
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [pendingSync]);

  const addToSyncQueue = (data) => {
    setPendingSync(prev => [...prev, { ...data, id: Date.now() }]);
  };

  const syncPendingData = async () => {
    if (!isOnline || pendingSync.length === 0) {
      return;
    }

    try {
      for (const item of pendingSync) {
        await fetch(item.url, {
          method: item.method,
          headers: item.headers,
          body: item.body,
        });
      }
      
      setPendingSync([]);
    } catch (error) {
      console.error('Erro na sincronização:', error);
    }
  };

  return {
    isOnline,
    pendingSync,
    addToSyncQueue,
    syncPendingData,
  };
};

export default usePWA;


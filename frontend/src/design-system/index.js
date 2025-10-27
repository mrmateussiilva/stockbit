// Design System Stockbit - Exportações principais
export { designTokens, semanticTokens } from './tokens';
export {
  Button,
  Input,
  Card,
  Badge,
  Spinner,
  Alert,
} from './components';

// Utilitários de acessibilidade
export const accessibilityUtils = {
  // Gerar IDs únicos para elementos
  generateId: (prefix = 'element') => {
    return `${prefix}-${Math.random().toString(36).substr(2, 9)}`;
  },
  
  // Verificar se o usuário prefere movimento reduzido
  prefersReducedMotion: () => {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  },
  
  // Verificar se o usuário prefere modo escuro
  prefersDarkMode: () => {
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  },
  
  // Verificar se o usuário prefere contraste alto
  prefersHighContrast: () => {
    return window.matchMedia('(prefers-contrast: high)').matches;
  },
  
  // Focar elemento de forma acessível
  focusElement: (element) => {
    if (element && typeof element.focus === 'function') {
      element.focus();
    }
  },
  
  // Adicionar listener para tecla Escape
  addEscapeListener: (callback) => {
    const handleEscape = (event) => {
      if (event.key === 'Escape') {
        callback();
      }
    };
    
    document.addEventListener('keydown', handleEscape);
    
    return () => {
      document.removeEventListener('keydown', handleEscape);
    };
  },
};

// Utilitários responsivos
export const responsiveUtils = {
  // Verificar se é mobile
  isMobile: () => {
    return window.innerWidth < 640;
  },
  
  // Verificar se é tablet
  isTablet: () => {
    return window.innerWidth >= 640 && window.innerWidth < 1024;
  },
  
  // Verificar se é desktop
  isDesktop: () => {
    return window.innerWidth >= 1024;
  },
  
  // Obter breakpoint atual
  getCurrentBreakpoint: () => {
    const width = window.innerWidth;
    if (width < 640) return 'sm';
    if (width < 768) return 'md';
    if (width < 1024) return 'lg';
    if (width < 1280) return 'xl';
    return '2xl';
  },
  
  // Adicionar listener para mudanças de tamanho
  addResizeListener: (callback) => {
    const handleResize = () => {
      callback(responsiveUtils.getCurrentBreakpoint());
    };
    
    window.addEventListener('resize', handleResize);
    
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  },
};

// Utilitários de validação
export const validationUtils = {
  // Validar email
  isValidEmail: (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  },
  
  // Validar CPF
  isValidCPF: (cpf) => {
    const cleanCPF = cpf.replace(/[^\d]/g, '');
    if (cleanCPF.length !== 11) return false;
    
    // Verificar se todos os dígitos são iguais
    if (/^(\d)\1{10}$/.test(cleanCPF)) return false;
    
    // Validar primeiro dígito verificador
    let sum = 0;
    for (let i = 0; i < 9; i++) {
      sum += parseInt(cleanCPF[i]) * (10 - i);
    }
    let digit1 = 11 - (sum % 11);
    if (digit1 >= 10) digit1 = 0;
    
    // Validar segundo dígito verificador
    sum = 0;
    for (let i = 0; i < 10; i++) {
      sum += parseInt(cleanCPF[i]) * (11 - i);
    }
    let digit2 = 11 - (sum % 11);
    if (digit2 >= 10) digit2 = 0;
    
    return digit1 === parseInt(cleanCPF[9]) && digit2 === parseInt(cleanCPF[10]);
  },
  
  // Validar CNPJ
  isValidCNPJ: (cnpj) => {
    const cleanCNPJ = cnpj.replace(/[^\d]/g, '');
    if (cleanCNPJ.length !== 14) return false;
    
    // Verificar se todos os dígitos são iguais
    if (/^(\d)\1{13}$/.test(cleanCNPJ)) return false;
    
    // Validar primeiro dígito verificador
    const weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];
    let sum = 0;
    for (let i = 0; i < 12; i++) {
      sum += parseInt(cleanCNPJ[i]) * weights1[i];
    }
    let digit1 = sum % 11 < 2 ? 0 : 11 - (sum % 11);
    
    // Validar segundo dígito verificador
    const weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];
    sum = 0;
    for (let i = 0; i < 13; i++) {
      sum += parseInt(cleanCNPJ[i]) * weights2[i];
    }
    let digit2 = sum % 11 < 2 ? 0 : 11 - (sum % 11);
    
    return digit1 === parseInt(cleanCNPJ[12]) && digit2 === parseInt(cleanCNPJ[13]);
  },
  
  // Validar telefone brasileiro
  isValidPhone: (phone) => {
    const cleanPhone = phone.replace(/[^\d]/g, '');
    return cleanPhone.length >= 10 && cleanPhone.length <= 11;
  },
};

// Utilitários de formatação
export const formatUtils = {
  // Formatar moeda brasileira
  formatCurrency: (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(value);
  },
  
  // Formatar número brasileiro
  formatNumber: (value, decimals = 0) => {
    return new Intl.NumberFormat('pt-BR', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    }).format(value);
  },
  
  // Formatar data brasileira
  formatDate: (date, options = {}) => {
    const defaultOptions = {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    };
    
    return new Intl.DateTimeFormat('pt-BR', {
      ...defaultOptions,
      ...options,
    }).format(new Date(date));
  },
  
  // Formatar CPF
  formatCPF: (cpf) => {
    const cleanCPF = cpf.replace(/[^\d]/g, '');
    return cleanCPF.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
  },
  
  // Formatar CNPJ
  formatCNPJ: (cnpj) => {
    const cleanCNPJ = cnpj.replace(/[^\d]/g, '');
    return cleanCNPJ.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
  },
  
  // Formatar telefone
  formatPhone: (phone) => {
    const cleanPhone = phone.replace(/[^\d]/g, '');
    if (cleanPhone.length === 11) {
      return cleanPhone.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
    } else if (cleanPhone.length === 10) {
      return cleanPhone.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
    }
    return phone;
  },
};

export default {
  designTokens,
  semanticTokens,
  accessibilityUtils,
  responsiveUtils,
  validationUtils,
  formatUtils,
};


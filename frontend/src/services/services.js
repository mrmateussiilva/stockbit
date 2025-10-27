import api from './api';

// Serviços de autenticação
export const authService = {
  login: async (credentials) => {
    const response = await api.post('/auth/login/', credentials);
    return response.data;
  },

  register: async (userData) => {
    const response = await api.post('/auth/register/', userData);
    return response.data;
  },

  logout: async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken) {
      await api.post('/auth/logout/', { refresh: refreshToken });
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  getProfile: async () => {
    const response = await api.get('/auth/profile/');
    return response.data;
  },

  updateProfile: async (userData) => {
    const response = await api.put('/auth/profile/update/', userData);
    return response.data;
  },

  forgotPassword: async (email) => {
    const response = await api.post('/auth/forgot-password/', { email });
    return response.data;
  },

  resetPassword: async (email, newPassword, token) => {
    const response = await api.post('/auth/reset-password/', { email, new_password: newPassword, token });
    return response.data;
  },

  changePassword: async (oldPassword, newPassword) => {
    const response = await api.post('/auth/change-password/', { 
      old_password: oldPassword, 
      new_password: newPassword 
    });
    return response.data;
  },

  verifyEmail: async (email, code) => {
    const response = await api.post('/auth/verify-email/', { email, code });
    return response.data;
  },
};

// Serviços de produtos
export const productService = {
  getProducts: async (params = {}) => {
    const response = await api.get('/products/products/', { params });
    return response.data;
  },

  getProduct: async (id) => {
    const response = await api.get(`/products/products/${id}/`);
    return response.data;
  },

  createProduct: async (productData) => {
    const response = await api.post('/products/products/', productData);
    return response.data;
  },

  updateProduct: async (id, productData) => {
    const response = await api.put(`/products/products/${id}/`, productData);
    return response.data;
  },

  deleteProduct: async (id) => {
    const response = await api.delete(`/products/products/${id}/`);
    return response.data;
  },

  getCategories: async () => {
    const response = await api.get('/products/categories/');
    return response.data;
  },

  createCategory: async (categoryData) => {
    const response = await api.post('/products/categories/', categoryData);
    return response.data;
  },

  updateCategory: async (id, categoryData) => {
    const response = await api.put(`/products/categories/${id}/`, categoryData);
    return response.data;
  },

  deleteCategory: async (id) => {
    const response = await api.delete(`/products/categories/${id}/`);
    return response.data;
  },

  getCategoryById: async (id) => {
    const response = await api.get(`/products/categories/${id}/`);
    return response.data;
  },

  getLowStockProducts: async () => {
    const response = await api.get('/products/products/low_stock/');
    return response.data;
  },

  getOutOfStockProducts: async () => {
    const response = await api.get('/products/products/out_of_stock/');
    return response.data;
  },

  getProductStats: async () => {
    const response = await api.get('/products/products/stats/');
    return response.data;
  },
};

// Serviços de estoque
export const stockService = {
  getMovements: async (params = {}) => {
    const response = await api.get('/stock/movements/', { params });
    return response.data;
  },

  createMovement: async (movementData) => {
    const response = await api.post('/stock/movements/', movementData);
    return response.data;
  },

  getStockSummary: async () => {
    const response = await api.get('/stock/movements/summary/');
    return response.data;
  },

  getStockStats: async () => {
    const response = await api.get('/stock/movements/stats/');
    return response.data;
  },
};

// Serviços de dashboard
export const dashboardService = {
  getStats: async () => {
    const response = await api.get('/dashboard/stats/');
    return response.data;
  },

  getChartsData: async () => {
    const response = await api.get('/dashboard/charts/');
    return response.data;
  },

  getRecentActivity: async () => {
    const response = await api.get('/dashboard/activity/');
    return response.data;
  },
};

// Serviços de exportação
export const exportService = {
  exportProducts: async () => {
    const response = await api.get('/products/export/products/', {
      responseType: 'blob',
    });
    return response.data;
  },

  exportMovements: async (startDate = null, endDate = null) => {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    
    const url = `/stock/export/movements/${params.toString() ? '?' + params.toString() : ''}`;
    const response = await api.get(url, {
      responseType: 'blob',
    });
    return response.data;
  },

  exportInventoryReport: async () => {
    const response = await api.get('/products/export/inventory-report/', {
      responseType: 'blob',
    });
    return response.data;
  },
};

// Serviços de clientes
export const clientService = {
  getAll: async (params = {}) => {
    const response = await api.get('/contacts/clients/', { params });
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/contacts/clients/${id}/`);
    return response.data;
  },

  create: async (data) => {
    const response = await api.post('/contacts/clients/', data);
    return response.data;
  },

  update: async (id, data) => {
    const response = await api.put(`/contacts/clients/${id}/`, data);
    return response.data;
  },

  delete: async (id) => {
    const response = await api.delete(`/contacts/clients/${id}/`);
    return response.data;
  },

  toggleStatus: async (id) => {
    const response = await api.post(`/contacts/clients/${id}/toggle_status/`);
    return response.data;
  },

  getStats: async () => {
    const response = await api.get('/contacts/clients/stats/');
    return response.data;
  },
};

// Serviços de fornecedores
export const supplierService = {
  getAll: async (params = {}) => {
    const response = await api.get('/contacts/suppliers/', { params });
    return response.data;
  },

  getById: async (id) => {
    const response = await api.get(`/contacts/suppliers/${id}/`);
    return response.data;
  },

  create: async (data) => {
    const response = await api.post('/contacts/suppliers/', data);
    return response.data;
  },

  update: async (id, data) => {
    const response = await api.put(`/contacts/suppliers/${id}/`, data);
    return response.data;
  },

  delete: async (id) => {
    const response = await api.delete(`/contacts/suppliers/${id}/`);
    return response.data;
  },

  toggleStatus: async (id) => {
    const response = await api.post(`/contacts/suppliers/${id}/toggle_status/`);
    return response.data;
  },

  getStats: async () => {
    const response = await api.get('/contacts/suppliers/stats/');
    return response.data;
  },
};

// Serviços de vendas/pedidos
export const salesService = {
  getOrders: async (params = {}) => {
    const response = await api.get('/sales/orders/', { params });
    return response.data;
  },

  getOrder: async (id) => {
    const response = await api.get(`/sales/orders/${id}/`);
    return response.data;
  },

  createOrder: async (orderData) => {
    const response = await api.post('/sales/orders/', orderData);
    return response.data;
  },

  updateOrder: async (id, orderData) => {
    const response = await api.put(`/sales/orders/${id}/`, orderData);
    return response.data;
  },

  deleteOrder: async (id) => {
    const response = await api.delete(`/sales/orders/${id}/`);
    return response.data;
  },

  completeOrder: async (id) => {
    const response = await api.post(`/sales/orders/${id}/complete/`);
    return response.data;
  },

  cancelOrder: async (id) => {
    const response = await api.post(`/sales/orders/${id}/cancel/`);
    return response.data;
  },

  markOrderAsPaid: async (id) => {
    const response = await api.post(`/sales/orders/${id}/mark_paid/`);
    return response.data;
  },

  getOrdersSummary: async () => {
    const response = await api.get('/sales/orders/summary/');
    return response.data;
  },

  getRecentOrders: async () => {
    const response = await api.get('/sales/orders/recent/');
    return response.data;
  },

  getOrderItems: async (params = {}) => {
    const response = await api.get('/sales/order-items/', { params });
    return response.data;
  },

  createOrderItem: async (itemData) => {
    const response = await api.post('/sales/order-items/', itemData);
    return response.data;
  },

  updateOrderItem: async (id, itemData) => {
    const response = await api.put(`/sales/order-items/${id}/`, itemData);
    return response.data;
  },

  deleteOrderItem: async (id) => {
    const response = await api.delete(`/sales/order-items/${id}/`);
    return response.data;
  },
};

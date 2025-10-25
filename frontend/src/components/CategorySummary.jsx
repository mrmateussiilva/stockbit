import React from 'react';
import { Package, CheckCircle, AlertTriangle, XCircle, TrendingUp } from 'lucide-react';

const CategorySummary = ({ category, products, isActive }) => {
  const stats = {
    total: products.length,
    normal: products.filter(p => p.quantity > p.min_quantity).length,
    low: products.filter(p => p.quantity > 0 && p.quantity <= p.min_quantity).length,
    out: products.filter(p => p.quantity === 0).length,
    totalValue: products.reduce((sum, p) => sum + (p.quantity * parseFloat(p.price)), 0)
  };

  return (
    <div className={`p-4 rounded-lg border-2 transition-all duration-200 ${
      isActive 
        ? 'border-blue-500 bg-blue-50' 
        : 'border-gray-200 bg-white hover:border-gray-300'
    }`}>
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold text-gray-900">{category.name}</h3>
        <span className="text-sm text-gray-500">{stats.total} produto(s)</span>
      </div>
      
      <div className="grid grid-cols-2 gap-3 mb-3">
        <div className="flex items-center">
          <CheckCircle className="h-4 w-4 text-green-600 mr-2" />
          <span className="text-sm text-gray-600">Normal: {stats.normal}</span>
        </div>
        <div className="flex items-center">
          <AlertTriangle className="h-4 w-4 text-yellow-600 mr-2" />
          <span className="text-sm text-gray-600">Baixo: {stats.low}</span>
        </div>
        <div className="flex items-center">
          <XCircle className="h-4 w-4 text-red-600 mr-2" />
          <span className="text-sm text-gray-600">Sem estoque: {stats.out}</span>
        </div>
        <div className="flex items-center">
          <TrendingUp className="h-4 w-4 text-purple-600 mr-2" />
          <span className="text-sm text-gray-600">
            R$ {stats.totalValue.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
          </span>
        </div>
      </div>
      
      {category.description && (
        <p className="text-xs text-gray-500 mt-2">{category.description}</p>
      )}
    </div>
  );
};

export default CategorySummary;


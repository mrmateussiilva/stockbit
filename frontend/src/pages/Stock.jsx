import React, { useState, useEffect } from 'react';
import { Plus, Search, ArrowUpRight, ArrowDownRight, Package } from 'lucide-react';
import { stockService, productService } from '../services/services';
import ExportButton from '../components/ExportButton';
import DateRangeExport from '../components/DateRangeExport';
import toast from 'react-hot-toast';

const Stock = () => {
  const [movements, setMovements] = useState([]);
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetchMovements();
    fetchProducts();
  }, []);

  const fetchMovements = async () => {
    try {
      const response = await stockService.getMovements();
      setMovements(response.results || response);
    } catch (error) {
      toast.error('Erro ao carregar movimentações');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchProducts = async () => {
    try {
      const response = await productService.getProducts();
      setProducts(response.results || response);
    } catch (error) {
      console.error('Erro ao carregar produtos:', error);
    }
  };

  const filteredMovements = movements.filter(movement =>
    movement.product_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    movement.product_sku.toLowerCase().includes(searchTerm.toLowerCase()) ||
    movement.reason.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getMovementIcon = (type) => {
    switch (type) {
      case 'Entrada':
        return <ArrowUpRight className="h-4 w-4 text-green-600" />;
      case 'Saída':
        return <ArrowDownRight className="h-4 w-4 text-red-600" />;
      default:
        return <Package className="h-4 w-4 text-blue-600" />;
    }
  };

  const getMovementColor = (type) => {
    switch (type) {
      case 'Entrada':
        return 'bg-green-100';
      case 'Saída':
        return 'bg-red-100';
      default:
        return 'bg-blue-100';
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Movimentações de Estoque</h1>
          <p className="mt-1 text-sm text-gray-500">
            Acompanhe todas as entradas e saídas do estoque
          </p>
        </div>
        <div className="flex gap-3">
          <ExportButton type="movements">
            Exportar Todas
          </ExportButton>
          <DateRangeExport type="movements">
            Exportar por Período
          </DateRangeExport>
          <button
            onClick={() => setShowModal(true)}
            className="btn-primary flex items-center"
          >
            <Plus className="h-4 w-4 mr-2" />
            Nova Movimentação
          </button>
        </div>
      </div>

      {/* Filtros */}
      <div className="card">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder="Buscar movimentações..."
            className="input-field pl-10"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {/* Lista de movimentações */}
      <div className="card">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Produto
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Tipo
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Quantidade
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Motivo
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Usuário
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Data
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredMovements.map((movement) => (
                <tr key={movement.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="p-2 rounded-lg bg-primary-100">
                        <Package className="h-4 w-4 text-primary-600" />
                      </div>
                      <div className="ml-3">
                        <div className="text-sm font-medium text-gray-900">
                          {movement.product_name}
                        </div>
                        <div className="text-sm text-gray-500">
                          SKU: {movement.product_sku}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className={`p-2 rounded-full ${getMovementColor(movement.movement_type_display)}`}>
                        {getMovementIcon(movement.movement_type_display)}
                      </div>
                      <span className="ml-2 text-sm font-medium text-gray-900">
                        {movement.movement_type_display}
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {movement.quantity}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {movement.reason}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {movement.user_name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(movement.created_at).toLocaleDateString('pt-BR')}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal de movimentação será implementado posteriormente */}
      {showModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Nova Movimentação
              </h3>
              <p className="text-sm text-gray-500 mb-4">
                Funcionalidade será implementada em breve
              </p>
              <div className="flex justify-end space-x-2">
                <button
                  onClick={() => setShowModal(false)}
                  className="btn-secondary"
                >
                  Fechar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Stock;


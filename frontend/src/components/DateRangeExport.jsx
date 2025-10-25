import React, { useState } from 'react';
import { Calendar, Download, X } from 'lucide-react';
import { exportService } from '../services/services';
import toast from 'react-hot-toast';

const DateRangeExport = ({ type, children }) => {
  const [showModal, setShowModal] = useState(false);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [isExporting, setIsExporting] = useState(false);

  const handleExport = async () => {
    if (!startDate && !endDate) {
      toast.error('Selecione pelo menos uma data');
      return;
    }

    if (startDate && endDate && new Date(startDate) > new Date(endDate)) {
      toast.error('A data inicial deve ser anterior à data final');
      return;
    }

    setIsExporting(true);
    try {
      let data;
      let filename = 'export.xlsx';

      if (type === 'movements') {
        data = await exportService.exportMovements(startDate, endDate);
        
        if (startDate && endDate) {
          filename = `movimentacoes_${startDate}_a_${endDate}.xlsx`;
        } else if (startDate) {
          filename = `movimentacoes_desde_${startDate}.xlsx`;
        } else if (endDate) {
          filename = `movimentacoes_ate_${endDate}.xlsx`;
        } else {
          filename = `movimentacoes_${new Date().toISOString().split('T')[0]}.xlsx`;
        }
      } else {
        toast.error('Tipo de exportação inválido.');
        return;
      }

      const url = window.URL.createObjectURL(new Blob([data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      
      toast.success('Exportação concluída com sucesso!');
      setShowModal(false);
      setStartDate('');
      setEndDate('');
    } catch (error) {
      console.error('Erro ao exportar:', error);
      toast.error('Erro ao exportar dados.');
    } finally {
      setIsExporting(false);
    }
  };

  const handleQuickSelect = (days) => {
    const today = new Date();
    const pastDate = new Date();
    pastDate.setDate(today.getDate() - days);
    
    setStartDate(pastDate.toISOString().split('T')[0]);
    setEndDate(today.toISOString().split('T')[0]);
  };

  return (
    <>
      <button
        onClick={() => setShowModal(true)}
        className="btn-secondary flex items-center"
      >
        <Calendar className="h-4 w-4 mr-2" />
        {children}
      </button>

      {showModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-medium text-gray-900">
                  Exportar por Período
                </h3>
                <button
                  onClick={() => setShowModal(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <X className="h-6 w-6" />
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Data Inicial
                  </label>
                  <input
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Data Final
                  </label>
                  <input
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Seleção Rápida
                  </label>
                  <div className="flex flex-wrap gap-2">
                    <button
                      onClick={() => handleQuickSelect(7)}
                      className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
                    >
                      Últimos 7 dias
                    </button>
                    <button
                      onClick={() => handleQuickSelect(30)}
                      className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
                    >
                      Últimos 30 dias
                    </button>
                    <button
                      onClick={() => handleQuickSelect(90)}
                      className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
                    >
                      Últimos 90 dias
                    </button>
                  </div>
                </div>

                <div className="flex justify-end space-x-3 pt-4">
                  <button
                    onClick={() => setShowModal(false)}
                    className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300"
                  >
                    Cancelar
                  </button>
                  <button
                    onClick={handleExport}
                    disabled={isExporting}
                    className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center"
                  >
                    {isExporting ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                        Exportando...
                      </>
                    ) : (
                      <>
                        <Download className="h-4 w-4 mr-2" />
                        Exportar
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default DateRangeExport;


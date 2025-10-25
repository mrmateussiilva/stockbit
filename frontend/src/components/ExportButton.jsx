import React, { useState } from 'react';
import { Download, FileSpreadsheet, Loader } from 'lucide-react';
import { exportService } from '../services/services';
import toast from 'react-hot-toast';

const ExportButton = ({ type, children, className = '' }) => {
  const [isLoading, setIsLoading] = useState(false);

  const handleExport = async () => {
    setIsLoading(true);
    
    try {
      let blob;
      let filename;
      
      switch (type) {
        case 'products':
          blob = await exportService.exportProducts();
          filename = `produtos_${new Date().toISOString().split('T')[0]}.xlsx`;
          break;
        case 'movements':
          blob = await exportService.exportMovements();
          filename = `movimentacoes_${new Date().toISOString().split('T')[0]}.xlsx`;
          break;
        case 'inventory-report':
          blob = await exportService.exportInventoryReport();
          filename = `relatorio_inventario_${new Date().toISOString().split('T')[0]}.xlsx`;
          break;
        default:
          throw new Error('Tipo de exportação não reconhecido');
      }

      // Criar link de download
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      toast.success('Arquivo exportado com sucesso!');
    } catch (error) {
      console.error('Erro ao exportar:', error);
      toast.error('Erro ao exportar arquivo. Tente novamente.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      onClick={handleExport}
      disabled={isLoading}
      className={`btn-secondary flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed ${className}`}
    >
      {isLoading ? (
        <Loader className="h-4 w-4 animate-spin" />
      ) : (
        <FileSpreadsheet className="h-4 w-4" />
      )}
      {children}
    </button>
  );
};

export default ExportButton;


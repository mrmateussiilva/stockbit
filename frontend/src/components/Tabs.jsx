import React, { useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const Tabs = ({ categories, activeTab, onTabChange, children }) => {
  const [scrollPosition, setScrollPosition] = useState(0);
  const [isScrolling, setIsScrolling] = useState(false);

  const scrollLeft = () => {
    setScrollPosition(Math.max(0, scrollPosition - 200));
  };

  const scrollRight = () => {
    const containerWidth = 800; // Aproximadamente a largura do container
    const tabWidth = 200; // Largura aproximada de cada tab
    const maxScroll = Math.max(0, categories.length * tabWidth - containerWidth);
    setScrollPosition(Math.min(maxScroll, scrollPosition + 200));
  };

  const handleTabClick = (categoryId) => {
    onTabChange(categoryId);
  };

  return (
    <div className="bg-white rounded-lg shadow">
      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <div className="flex items-center justify-between px-4 py-2">
          <div className="flex items-center space-x-2">
            <button
              onClick={scrollLeft}
              disabled={scrollPosition === 0}
              className="p-1 rounded-md hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronLeft className="h-4 w-4" />
            </button>
            
            <div className="flex-1 overflow-hidden">
              <div 
                className="flex space-x-1 transition-transform duration-300 ease-in-out"
                style={{ transform: `translateX(-${scrollPosition}px)` }}
              >
                <button
                  onClick={() => handleTabClick('all')}
                  className={`px-4 py-2 text-sm font-medium rounded-t-lg transition-colors ${
                    activeTab === 'all'
                      ? 'bg-blue-50 text-blue-700 border-b-2 border-blue-500'
                      : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  Todos ({categories.reduce((total, cat) => total + cat.products_count, 0)})
                </button>
                {categories.map((category) => (
                  <button
                    key={category.id}
                    onClick={() => handleTabClick(category.id)}
                    className={`px-4 py-2 text-sm font-medium rounded-t-lg transition-colors whitespace-nowrap ${
                      activeTab === category.id
                        ? 'bg-blue-50 text-blue-700 border-b-2 border-blue-500'
                        : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    {category.name} ({category.products_count})
                  </button>
                ))}
              </div>
            </div>
            
            <button
              onClick={scrollRight}
              disabled={scrollPosition >= Math.max(0, categories.length * 200 - 800)}
              className="p-1 rounded-md hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Tab Content */}
      <div className="p-6">
        {children}
      </div>
    </div>
  );
};

export default Tabs;

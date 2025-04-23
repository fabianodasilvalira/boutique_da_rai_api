import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import ProductFilter from './ProductFilter';
import './Products.css';

const Products = () => {
  const [activeFilter, setActiveFilter] = useState('all');
  const [visibleProducts, setVisibleProducts] = useState([]);
  
  const categories = [
    {
      id: 1,
      title: 'Perfumes Masculinos',
      description: 'Fragrâncias marcantes e sofisticadas para homens modernos',
      image: '/images/perfume_1.webp',
      category: 'masculino'
    },
    {
      id: 2,
      title: 'Perfumes Femininos',
      description: 'Aromas delicados e envolventes para mulheres de atitude',
      image: '/images/perfume_2.webp',
      category: 'feminino'
    },
    {
      id: 3,
      title: 'Perfumes Unissex',
      description: 'Fragrâncias versáteis para todos os estilos e personalidades',
      image: '/images/perfume_3.webp',
      category: 'unissex'
    },
    {
      id: 4,
      title: 'Perfumes Infantis',
      description: 'Aromas suaves e divertidos para os pequenos',
      image: '/images/perfume_1.webp',
      category: 'infantil'
    },
    {
      id: 5,
      title: 'Cosméticos',
      description: 'Produtos de beleza e cuidados pessoais de alta qualidade',
      image: '/images/perfume_2.webp',
      category: 'cosmeticos'
    },
    {
      id: 6,
      title: 'Bijuterias',
      description: 'Acessórios elegantes para complementar seu estilo',
      image: '/images/perfume_3.webp',
      category: 'cosmeticos'
    }
  ];

  // Filtrar produtos com base na categoria selecionada
  useEffect(() => {
    if (activeFilter === 'all') {
      setVisibleProducts(categories);
    } else {
      const filtered = categories.filter(product => product.category === activeFilter);
      setVisibleProducts(filtered);
    }
  }, [activeFilter]);

  // Função para atualizar o filtro ativo
  const handleFilterChange = (filter) => {
    setActiveFilter(filter);
  };

  return (
    <section id="products" className="section products-section">
      <div className="container">
        <h2 className="section-title">Nossos Produtos</h2>
        <p className="section-description">
          Descubra nossa seleção exclusiva de perfumes e cosméticos para todos os gostos e ocasiões
        </p>
        
        <ProductFilter activeFilter={activeFilter} onFilterChange={handleFilterChange} />
        
        <div className="grid grid-3">
          {visibleProducts.map(category => (
            <div key={category.id} className="product-card card animate-fade-in">
              <div className="product-image">
                <img src={category.image} alt={category.title} className="card-img" />
              </div>
              <div className="card-content">
                <h3 className="card-title">{category.title}</h3>
                <p className="card-text">{category.description}</p>
                <Link to={`/produtos/${category.id}`} className="product-link">Ver produtos</Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Products;

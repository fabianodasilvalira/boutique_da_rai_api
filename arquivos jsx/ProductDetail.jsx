import React from 'react';
import { useParams } from 'react-router-dom';
import { FaArrowLeft, FaShoppingCart, FaWhatsapp } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import './ProductDetail.css';

const ProductDetail = () => {
  const { id } = useParams();
  
  // Dados simulados de produtos para cada categoria
  const productData = {
    1: { // Perfumes Masculinos
      title: 'Perfumes Masculinos',
      description: 'Fragrâncias marcantes e sofisticadas para homens modernos',
      image: '/images/perfume_1.webp',
      products: [
        {
          id: 101,
          name: 'Elegance Pour Homme',
          description: 'Fragrância amadeirada com notas de sândalo e bergamota',
          price: 'R$ 189,90',
          image: '/images/perfume_1.webp'
        },
        {
          id: 102,
          name: 'Blue Ocean',
          description: 'Aroma fresco e aquático para o dia a dia',
          price: 'R$ 159,90',
          image: '/images/perfume_2.webp'
        },
        {
          id: 103,
          name: 'Black Intense',
          description: 'Perfume intenso com notas de couro e especiarias',
          price: 'R$ 219,90',
          image: '/images/perfume_3.webp'
        }
      ]
    },
    2: { // Perfumes Femininos
      title: 'Perfumes Femininos',
      description: 'Aromas delicados e envolventes para mulheres de atitude',
      image: '/images/perfume_2.webp',
      products: [
        {
          id: 201,
          name: 'Floral Essence',
          description: 'Fragrância floral com notas de jasmim e rosa',
          price: 'R$ 179,90',
          image: '/images/perfume_2.webp'
        },
        {
          id: 202,
          name: 'Sweet Vanilla',
          description: 'Aroma doce e envolvente com notas de baunilha',
          price: 'R$ 169,90',
          image: '/images/perfume_1.webp'
        },
        {
          id: 203,
          name: 'Midnight Rose',
          description: 'Perfume sofisticado com notas de rosa e âmbar',
          price: 'R$ 199,90',
          image: '/images/perfume_3.webp'
        }
      ]
    },
    3: { // Perfumes Unissex
      title: 'Perfumes Unissex',
      description: 'Fragrâncias versáteis para todos os estilos e personalidades',
      image: '/images/perfume_3.webp',
      products: [
        {
          id: 301,
          name: 'Fresh Citrus',
          description: 'Fragrância cítrica refrescante para qualquer ocasião',
          price: 'R$ 149,90',
          image: '/images/perfume_3.webp'
        },
        {
          id: 302,
          name: 'Urban Style',
          description: 'Aroma moderno com notas de lavanda e cedro',
          price: 'R$ 179,90',
          image: '/images/perfume_1.webp'
        },
        {
          id: 303,
          name: 'Pure White',
          description: 'Perfume clean com notas de algodão e almíscar',
          price: 'R$ 159,90',
          image: '/images/perfume_2.webp'
        }
      ]
    },
    4: { // Perfumes Infantis
      title: 'Perfumes Infantis',
      description: 'Aromas suaves e divertidos para os pequenos',
      image: '/images/perfume_1.webp',
      products: [
        {
          id: 401,
          name: 'Sweet Dreams',
          description: 'Colônia suave com aroma de lavanda para acalmar',
          price: 'R$ 89,90',
          image: '/images/perfume_1.webp'
        },
        {
          id: 402,
          name: 'Fruity Fun',
          description: 'Fragrância divertida com notas de frutas vermelhas',
          price: 'R$ 79,90',
          image: '/images/perfume_2.webp'
        },
        {
          id: 403,
          name: 'Baby Care',
          description: 'Colônia delicada especial para bebês',
          price: 'R$ 99,90',
          image: '/images/perfume_3.webp'
        }
      ]
    },
    5: { // Cosméticos
      title: 'Cosméticos',
      description: 'Produtos de beleza e cuidados pessoais de alta qualidade',
      image: '/images/perfume_2.webp',
      products: [
        {
          id: 501,
          name: 'Hidratante Facial',
          description: 'Creme hidratante para todos os tipos de pele',
          price: 'R$ 69,90',
          image: '/images/perfume_2.webp'
        },
        {
          id: 502,
          name: 'Máscara Capilar',
          description: 'Tratamento intensivo para cabelos danificados',
          price: 'R$ 59,90',
          image: '/images/perfume_1.webp'
        },
        {
          id: 503,
          name: 'Kit Maquiagem',
          description: 'Kit completo com produtos essenciais para maquiagem',
          price: 'R$ 129,90',
          image: '/images/perfume_3.webp'
        }
      ]
    },
    6: { // Bijuterias
      title: 'Bijuterias',
      description: 'Acessórios elegantes para complementar seu estilo',
      image: '/images/perfume_3.webp',
      products: [
        {
          id: 601,
          name: 'Conjunto Colar e Brincos',
          description: 'Conjunto elegante banhado a ouro',
          price: 'R$ 89,90',
          image: '/images/perfume_3.webp'
        },
        {
          id: 602,
          name: 'Pulseira Charm',
          description: 'Pulseira ajustável com pingentes decorativos',
          price: 'R$ 49,90',
          image: '/images/perfume_1.webp'
        },
        {
          id: 603,
          name: 'Anel Ajustável',
          description: 'Anel com design moderno e acabamento premium',
          price: 'R$ 39,90',
          image: '/images/perfume_2.webp'
        }
      ]
    }
  };

  const category = productData[id];

  if (!category) {
    return (
      <div className="product-detail-container">
        <div className="container">
          <h2>Categoria não encontrada</h2>
          <Link to="/" className="btn btn-primary">Voltar para a página inicial</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="product-detail-container">
      <div className="container">
        <div className="product-detail-header">
          <Link to="/" className="back-button">
            <FaArrowLeft /> Voltar
          </Link>
          <h2 className="category-title">{category.title}</h2>
          <p className="category-description">{category.description}</p>
        </div>

        <div className="products-grid">
          {category.products.map(product => (
            <div key={product.id} className="product-item">
              <div className="product-image">
                <img src={product.image} alt={product.name} />
              </div>
              <div className="product-info">
                <h3 className="product-name">{product.name}</h3>
                <p className="product-description">{product.description}</p>
                <p className="product-price">{product.price}</p>
                <div className="product-actions">
                  <button className="btn btn-primary">
                    <FaShoppingCart /> Comprar
                  </button>
                  <a 
                    href={`https://wa.me/5500000000000?text=Olá! Tenho interesse no produto ${product.name}`} 
                    className="btn btn-whatsapp"
                    target="_blank" 
                    rel="noopener noreferrer"
                  >
                    <FaWhatsapp /> Consultar
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProductDetail;

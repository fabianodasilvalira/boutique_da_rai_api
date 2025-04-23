import React from 'react';
import { Link } from 'react-router-dom';
import './Contact.css';
import { FaWhatsapp, FaEnvelope, FaMapMarkerAlt, FaPhone } from 'react-icons/fa';

const Contact = () => {
  return (
    <div className="contact-container">
      <div className="container">
        <div className="contact-header">
          <h1 className="contact-title">Entre em Contato</h1>
          <p className="contact-subtitle">
            Estamos à disposição para atender você e responder todas as suas dúvidas sobre nossos produtos.
          </p>
        </div>

        <div className="contact-content">
          <div className="contact-info">
            <div className="info-card">
              <div className="info-icon">
                <FaMapMarkerAlt />
              </div>
              <div className="info-text">
                <h3>Endereço</h3>
                <p>Rua dos Perfumes, 123</p>
                <p>São Paulo, SP - 01234-567</p>
              </div>
            </div>

            <div className="info-card">
              <div className="info-icon">
                <FaPhone />
              </div>
              <div className="info-text">
                <h3>Telefone</h3>
                <p>(11) 99999-9999</p>
                <p>(11) 5555-5555</p>
              </div>
            </div>

            <div className="info-card">
              <div className="info-icon">
                <FaEnvelope />
              </div>
              <div className="info-text">
                <h3>E-mail</h3>
                <p>contato@perfumes.com.br</p>
                <p>vendas@perfumes.com.br</p>
              </div>
            </div>

            <div className="info-card">
              <div className="info-icon">
                <FaWhatsapp />
              </div>
              <div className="info-text">
                <h3>WhatsApp</h3>
                <p>(11) 99999-9999</p>
                <a 
                  href="https://wa.me/5511999999999" 
                  className="whatsapp-link"
                  target="_blank" 
                  rel="noopener noreferrer"
                >
                  Enviar mensagem
                </a>
              </div>
            </div>
          </div>

          <div className="contact-form-container">
            <h2>Envie-nos uma mensagem</h2>
            <form className="contact-form">
              <div className="form-group">
                <label htmlFor="name">Nome</label>
                <input 
                  type="text" 
                  id="name" 
                  placeholder="Seu nome completo"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="email">E-mail</label>
                <input 
                  type="email" 
                  id="email" 
                  placeholder="Seu e-mail"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="phone">Telefone</label>
                <input 
                  type="tel" 
                  id="phone" 
                  placeholder="Seu telefone"
                />
              </div>

              <div className="form-group">
                <label htmlFor="subject">Assunto</label>
                <input 
                  type="text" 
                  id="subject" 
                  placeholder="Assunto da mensagem"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="message">Mensagem</label>
                <textarea 
                  id="message" 
                  rows="5" 
                  placeholder="Digite sua mensagem aqui..."
                  required
                ></textarea>
              </div>

              <button type="submit" className="submit-button">
                Enviar Mensagem
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Contact;

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Quiz.css';

const Quiz = () => {
  const [step, setStep] = useState(1);
  const [name, setName] = useState('');
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [selectedOption, setSelectedOption] = useState(null);

  // Efeito para rolar para o topo quando mudar de pergunta
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [step]);

  // Perguntas do quiz
  const questions = [
    {
      id: 1,
      question: "Qual é o seu dia a dia?",
      options: [
        { id: "trabalho", text: "Trabalho em escritório" },
        { id: "casa", text: "Fico mais em casa" },
        { id: "ar_livre", text: "Atividades ao ar livre" },
        { id: "variado", text: "Bastante variado" }
      ]
    },
    {
      id: 2,
      question: "Qual intensidade de fragrância você prefere?",
      options: [
        { id: "suave", text: "Suave" },
        { id: "moderada", text: "Moderada" },
        { id: "intensa", text: "Intensa" }
      ]
    },
    {
      id: 3,
      question: "Para qual ocasião você está buscando um perfume?",
      options: [
        { id: "dia_a_dia", text: "Dia a dia" },
        { id: "trabalho", text: "Trabalho" },
        { id: "encontro", text: "Encontro romântico" },
        { id: "ocasiao_especial", text: "Ocasião especial" }
      ]
    },
    {
      id: 4,
      question: "Qual tipo de fragrância mais lhe agrada?",
      options: [
        { id: "floral", text: "Floral", image: "/images/floral.webp" },
        { id: "frutal", text: "Frutal", image: "/images/frutal.webp" },
        { id: "oriental", text: "Oriental", image: "/images/oriental.jpeg" },
        { id: "amadeirado", text: "Amadeirado", image: "/images/amadeirado.jpeg" }
      ]
    },
    {
      id: 5,
      question: "Quais sensações e sentimentos você quer despertar?",
      options: [
        { id: "frescor", text: "Frescor e liberdade" },
        { id: "sensualidade", text: "Sensualidade e mistério" },
        { id: "elegancia", text: "Elegância e sofisticação" },
        { id: "conforto", text: "Conforto e aconchego" }
      ]
    }
  ];

  // Resultados possíveis
  const perfumeResults = [
    {
      id: "floral_suave",
      name: "Floral Delicado",
      description: "Um perfume floral suave com notas de jasmim e rosa, ideal para o dia a dia e ambientes de trabalho. Transmite delicadeza e feminilidade.",
      image: "/images/perfume_1.webp",
      recommendation: "Ideal para mulheres que preferem fragrâncias sutis e elegantes para o cotidiano."
    },
    {
      id: "floral_intenso",
      name: "Floral Intenso",
      description: "Uma fragrância floral marcante com notas de gardênia e ylang-ylang. Perfeita para ocasiões especiais e encontros românticos.",
      image: "/images/perfume_2.webp",
      recommendation: "Perfeito para mulheres que desejam marcar presença com uma fragrância memorável."
    },
    {
      id: "frutal_suave",
      name: "Frutal Refrescante",
      description: "Um perfume frutal leve com notas cítricas de laranja e maçã verde. Ideal para o dia a dia e atividades ao ar livre.",
      image: "/images/perfume_3.webp",
      recommendation: "Excelente para mulheres dinâmicas que buscam frescor durante todo o dia."
    },
    {
      id: "oriental_intenso",
      name: "Oriental Misterioso",
      description: "Uma fragrância oriental intensa com notas de baunilha e âmbar. Perfeita para noites especiais e encontros românticos.",
      image: "/images/woman_perfume_1.webp",
      recommendation: "Ideal para mulheres que desejam transmitir sensualidade e mistério."
    },
    {
      id: "amadeirado_moderado",
      name: "Amadeirado Sofisticado",
      description: "Um perfume amadeirado com notas de sândalo e cedro. Equilibrado e versátil, adequado para diversas ocasiões.",
      image: "/images/woman_perfume_2.webp",
      recommendation: "Perfeito para mulheres que apreciam fragrâncias sofisticadas e atemporais."
    }
  ];

  // Função para determinar o resultado com base nas respostas
  const calculateResult = () => {
    // Lógica simplificada para determinar o resultado
    // Em uma implementação real, seria mais complexa
    
    const intensidade = answers[2] || "";
    const tipo = answers[4] || "";
    
    if (tipo === "floral") {
      if (intensidade === "suave") {
        return perfumeResults[0]; // Floral Delicado
      } else {
        return perfumeResults[1]; // Floral Intenso
      }
    } else if (tipo === "frutal") {
      return perfumeResults[2]; // Frutal Refrescante
    } else if (tipo === "oriental") {
      return perfumeResults[3]; // Oriental Misterioso
    } else {
      return perfumeResults[4]; // Amadeirado Sofisticado
    }
  };

  // Função para avançar para a próxima pergunta automaticamente
  const handleNext = () => {
    if (step === 1 && !name) {
      alert("Por favor, digite seu nome para continuar.");
      return;
    }
    
    if (step === questions.length) {
      // Calcular resultado
      setResult(calculateResult());
    }
    
    setStep(step + 1);
    setSelectedOption(null); // Resetar a opção selecionada para a próxima pergunta
  };

  // Função para voltar para a pergunta anterior
  const handleBack = () => {
    setStep(step - 1);
    setSelectedOption(null); // Resetar a opção selecionada
  };

  // Função para selecionar uma resposta e avançar automaticamente
  const selectAnswer = (questionId, answerId) => {
    setAnswers({
      ...answers,
      [questionId]: answerId
    });
    
    setSelectedOption(answerId);
    
    // Avançar automaticamente após um breve delay para mostrar a seleção
    setTimeout(() => {
      handleNext();
    }, 500);
  };

  // Função para reiniciar o quiz
  const restartQuiz = () => {
    setStep(1);
    setName('');
    setAnswers({});
    setResult(null);
    setSelectedOption(null);
  };

  // Renderiza a tela de boas-vindas
  const renderWelcome = () => (
    <div className="quiz-welcome">
      <h2>Descubra seu Aroma Ideal</h2>
      <p>Responda algumas perguntas simples e descubra qual perfume combina perfeitamente com você.</p>
      
      <div className="name-input">
        <label htmlFor="name">Como podemos te chamar?</label>
        <input 
          type="text" 
          id="name" 
          value={name} 
          onChange={(e) => setName(e.target.value)}
          placeholder="Digite seu nome"
        />
      </div>
      
      <button className="quiz-button" onClick={handleNext}>Começar</button>
    </div>
  );

  // Renderiza uma pergunta
  const renderQuestion = () => {
    const currentQuestion = questions[step - 2];
    
    return (
      <div className="quiz-question">
        <h2>{currentQuestion.question}</h2>
        
        <div className={`options-container ${currentQuestion.options.length > 3 ? 'grid-2' : ''}`}>
          {currentQuestion.options.map(option => (
            <div 
              key={option.id}
              className={`option ${selectedOption === option.id ? 'selected' : ''}`}
              onClick={() => selectAnswer(step, option.id)}
            >
              {option.image && (
                <div className="option-image">
                  <img src={option.image} alt={option.text} />
                </div>
              )}
              <span>{option.text}</span>
            </div>
          ))}
        </div>
        
        <div className="quiz-navigation">
          <button className="quiz-button secondary" onClick={handleBack}>Voltar</button>
        </div>
      </div>
    );
  };

  // Renderiza o resultado
  const renderResult = () => (
    <div className="quiz-result">
      <h2>Seu Aroma Ideal</h2>
      
      {result && (
        <div className="result-container">
          <div className="result-image">
            <img src={result.image} alt={result.name} />
          </div>
          
          <div className="result-content">
            <h3>{result.name}</h3>
            <p className="result-description">{result.description}</p>
            <p className="result-recommendation">{result.recommendation}</p>
            
            <div className="result-actions">
              <button className="quiz-button" onClick={restartQuiz}>Refazer o Quiz</button>
              <Link to="/#products" className="quiz-button secondary">Ver Produtos</Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );

  // Renderiza o progresso
  const renderProgress = () => {
    if (step === 1 || step > questions.length + 1) return null;
    
    const progress = ((step - 1) / questions.length) * 100;
    
    return (
      <div className="quiz-progress">
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${progress}%` }}></div>
        </div>
        <span className="progress-text">Pergunta {step - 1} de {questions.length}</span>
      </div>
    );
  };

  return (
    <div className="quiz-container">
      {renderProgress()}
      
      <div className="quiz-content">
        {step === 1 && renderWelcome()}
        {step > 1 && step <= questions.length + 1 && step - 2 < questions.length && renderQuestion()}
        {step === questions.length + 2 && renderResult()}
      </div>
    </div>
  );
};

export default Quiz;

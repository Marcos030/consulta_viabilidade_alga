// Configuração da URL base da API
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Consulta viabilidade de um endereço
 * @param {string} cep - CEP sem máscara (apenas números)
 * @param {string} codLogradouro - Código do logradouro
 */
export const consultarViabilidade = async (cep, codLogradouro) => {
  const response = await fetch(
    `${API_URL}/consultar?cep=${cep}&cod_logradouro=${codLogradouro}`
  );

  if (!response.ok) {
    throw new Error('Erro ao consultar endereço');
  }

  return response.json();
};

/**
 * Faz upload de planilha Excel
 * @param {File} file - Arquivo Excel
 */
export const uploadPlanilha = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_URL}/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Erro ao fazer upload');
  }

  return response.json();
};

/**
 * Limpa a base de dados
 */
export const limparBase = async () => {
  const response = await fetch(`${API_URL}/limpar`, {
    method: 'DELETE',
  });

  if (!response.ok) {
    throw new Error('Erro ao limpar base de dados');
  }

  return response.json();
};

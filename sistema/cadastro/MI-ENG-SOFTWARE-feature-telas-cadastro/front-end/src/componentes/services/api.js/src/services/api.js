// Este arquivo vai ter todas as suas chamadas de API
const API_URL = 'http://localhost:8000/api'; // URL base da sua API Django

// Função exportada para buscar os dados
export async function getMeusDados() {
  try {
    const response = await fetch(`${API_URL}/meus-dados/`); // Usando a URL base
    if (!response.ok) {
      throw new Error('Erro na resposta da rede');
    }
    const data = await response.json();
    return data; // Retorna os dados
  } catch (error) {
    console.error('Erro ao buscar dados:', error);
    throw error; // Propaga o erro para o componente tratar
  }
}

// Você pode adicionar outras funções aqui (POST, PUT, etc.)
// export async function criarDado(novoDado) { ... }
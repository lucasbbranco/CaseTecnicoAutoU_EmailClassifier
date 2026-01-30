/**
 * API Client
 * ===========
 * Módulo para comunicação com a API backend.
 */

// Configuração da API
const API_CONFIG = {
    // IMPORTANTE: Trocar por URL do backend deployado
    baseURL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:8000/api'  // Desenvolvimento local
        : '/api',  // Produção (mesmo domínio)
    
    timeout: 30000  // 30 segundos
};

/**
 * Cliente HTTP para requisições à API
 */
class APIClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    /**
     * Classifica um email enviado como texto
     * @param {string} emailText - Texto do email
     * @returns {Promise<Object>} Resultado da classificação
     */
    async classifyText(emailText) {
        try {
            const response = await fetch(`${this.baseURL}/classify-text`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email_text: emailText
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Erro ao classificar texto');
            }

            return await response.json();
        } catch (error) {
            console.error('Erro ao classificar texto:', error);
            throw error;
        }
    }

    /**
     * Classifica um email enviado como arquivo
     * @param {File} file - Arquivo (.txt ou .pdf)
     * @returns {Promise<Object>} Resultado da classificação
     */
    async classifyFile(file) {
        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`${this.baseURL}/classify-file`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Erro ao processar arquivo');
            }

            return await response.json();
        } catch (error) {
            console.error('Erro ao processar arquivo:', error);
            throw error;
        }
    }

    /**
     * Verifica saúde da API
     * @returns {Promise<Object>} Status da API
     */
    async healthCheck() {
        try {
            const response = await fetch(`${this.baseURL}/health`);
            return await response.json();
        } catch (error) {
            console.error('Erro ao verificar saúde da API:', error);
            throw error;
        }
    }
}

// Instância global do cliente
const apiClient = new APIClient(API_CONFIG.baseURL);

// Exportar para uso no app.js
window.apiClient = apiClient;
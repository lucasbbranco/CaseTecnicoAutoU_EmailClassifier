/**
 * Email Classifier App
 * ====================
 * Lógica principal da aplicação frontend.
 */

// ==================== ELEMENTOS DO DOM ====================

const elements = {
    // Tabs
    tabBtns: document.querySelectorAll('.tab-btn'),
    tabContents: document.querySelectorAll('.tab-content'),
    
    // File upload
    dropzone: document.getElementById('dropzone'),
    fileInput: document.getElementById('file-input'),
    filePreview: document.getElementById('file-preview'),
    fileName: document.getElementById('file-name'),
    removeFileBtn: document.getElementById('remove-file'),
    
    // Text input
    emailTextarea: document.getElementById('email-text'),
    charCount: document.getElementById('char-count'),
    
    // Buttons
    classifyBtn: document.getElementById('classify-btn'),
    newClassificationBtn: document.getElementById('new-classification-btn'),
    copyBtn: document.getElementById('copy-btn'),
    
    // Results
    resultsSection: document.getElementById('results-section'),
    categoryBadge: document.getElementById('category-badge'),
    badgeText: document.getElementById('badge-text'),
    confidenceFill: document.getElementById('confidence-fill'),
    confidenceValue: document.getElementById('confidence-value'),
    justificationText: document.getElementById('justification-text'),
    responseText: document.getElementById('response-text'),
    processingTime: document.getElementById('processing-time'),
    
    // Loading & Error
    loadingOverlay: document.getElementById('loading-overlay'),
    errorMessage: document.getElementById('error-message'),
    errorText: document.getElementById('error-text'),
    closeErrorBtn: document.getElementById('close-error-btn')
};

// ==================== STATE ====================

let state = {
    activeTab: 'file',
    selectedFile: null,
    isProcessing: false
};

// ==================== INICIALIZAÇÃO ====================

document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    initializeFileUpload();
    initializeTextInput();
    initializeClassification();
    initializeResultActions();
    checkAPIHealth();
});

// ==================== TABS ====================

function initializeTabs() {
    elements.tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;
            switchTab(tab);
        });
    });
}

function switchTab(tab) {
    state.activeTab = tab;
    
    // Atualizar botões
    elements.tabBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tab);
    });
    
    // Atualizar conteúdo
    elements.tabContents.forEach(content => {
        const contentTab = content.id.replace('-tab', '');
        content.classList.toggle('active', contentTab === tab);
    });
    
    // Resetar estado
    resetUploadState();
}

// ==================== FILE UPLOAD ====================

function initializeFileUpload() {
    // Click no dropzone abre file input
    elements.dropzone.addEventListener('click', () => {
        if (!state.selectedFile) {
            elements.fileInput.click();
        }
    });
    
    // Drag & Drop
    elements.dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        elements.dropzone.classList.add('dragover');
    });
    
    elements.dropzone.addEventListener('dragleave', () => {
        elements.dropzone.classList.remove('dragover');
    });
    
    elements.dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        elements.dropzone.classList.remove('dragover');
        
        const file = e.dataTransfer.files[0];
        handleFileSelection(file);
    });
    
    // File input change
    elements.fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        handleFileSelection(file);
    });
    
    // Remover arquivo
    elements.removeFileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetUploadState();
    });
}

function handleFileSelection(file) {
    if (!file) return;
    
    // Validar tipo
    const validTypes = ['.txt', '.pdf'];
    const fileExt = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!validTypes.includes(fileExt)) {
        showError('Apenas arquivos .txt e .pdf são aceitos');
        return;
    }
    
    // Validar tamanho (5MB)
    const maxSize = 5 * 1024 * 1024;
    if (file.size > maxSize) {
        showError('Arquivo muito grande. Máximo: 5MB');
        return;
    }
    
    // Atualizar estado
    state.selectedFile = file;
    
    // Mostrar preview
    elements.dropzone.querySelector('.dropzone-content').style.display = 'none';
    elements.filePreview.style.display = 'flex';
    elements.fileName.textContent = file.name;
}

function resetUploadState() {
    state.selectedFile = null;
    elements.fileInput.value = '';
    elements.dropzone.querySelector('.dropzone-content').style.display = 'block';
    elements.filePreview.style.display = 'none';
    elements.emailTextarea.value = '';
    elements.charCount.textContent = '0';
}

// ==================== TEXT INPUT ====================

function initializeTextInput() {
    elements.emailTextarea.addEventListener('input', (e) => {
        const length = e.target.value.length;
        elements.charCount.textContent = length.toLocaleString('pt-BR');
        
        // Limitar a 10.000 caracteres
        if (length > 10000) {
            e.target.value = e.target.value.substring(0, 10000);
            elements.charCount.textContent = '10.000';
        }
    });
}

// ==================== CLASSIFICAÇÃO ====================

function initializeClassification() {
    elements.classifyBtn.addEventListener('click', handleClassification);
}

async function handleClassification() {
    if (state.isProcessing) return;
    
    try {
        // Validar input
        if (state.activeTab === 'file' && !state.selectedFile) {
            showError('Por favor, selecione um arquivo');
            return;
        }
        
        if (state.activeTab === 'text' && !elements.emailTextarea.value.trim()) {
            showError('Por favor, digite ou cole o texto do email');
            return;
        }
        
        // Mostrar loading
        state.isProcessing = true;
        showLoading();
        hideResults();
        
        // Fazer requisição
        let result;
        if (state.activeTab === 'file') {
            result = await window.apiClient.classifyFile(state.selectedFile);
        } else {
            result = await window.apiClient.classifyText(elements.emailTextarea.value);
        }
        
        // Verificar sucesso
        if (!result.success) {
            throw new Error(result.error || 'Erro desconhecido');
        }
        
        // Mostrar resultados
        displayResults(result);
        
    } catch (error) {
        console.error('Erro na classificação:', error);
        // Extrair mensagem de erro de forma segura
        let errorMessage = 'Erro ao classificar email. Tente novamente.';
        
        if (typeof error === 'string') {
            errorMessage = error;
        } else if (error && error.message) {
            errorMessage = error.message;
        } else if (error && error.detail) {
            errorMessage = error.detail;
        }
        
        showError(errorMessage);
    } finally {
        state.isProcessing = false;
        hideLoading();
    }
}

// ==================== EXIBIR RESULTADOS ====================

function displayResults(result) {
    // Categoria
    const category = result.classification.toUpperCase();
    const isProductive = category === 'PRODUTIVO';
    
    elements.badgeText.textContent = category;
    elements.categoryBadge.className = `category-badge ${isProductive ? 'produtivo' : 'improdutivo'}`;
    
    // Confiança
    const confidence = Math.round(result.confidence * 100);
    elements.confidenceFill.style.width = `${confidence}%`;
    elements.confidenceValue.textContent = `${confidence}%`;
    
    // Justificativa
    elements.justificationText.textContent = result.justification || '-';
    
    // Resposta sugerida
    elements.responseText.textContent = result.suggested_response || 'Nenhuma resposta sugerida';
    
    // Tempo de processamento
    elements.processingTime.textContent = result.processing_time_ms || '-';
    
    // Mostrar seção de resultados
    showResults();
    
    // Scroll suave para resultados
    setTimeout(() => {
        elements.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 300);
}

// ==================== AÇÕES DOS RESULTADOS ====================

function initializeResultActions() {
    // Nova classificação
    elements.newClassificationBtn.addEventListener('click', () => {
        hideResults();
        resetUploadState();
    });
    
    // Copiar resposta
    elements.copyBtn.addEventListener('click', async () => {
        try {
            await navigator.clipboard.writeText(elements.responseText.textContent);
            
            // Feedback visual
            const originalText = elements.copyBtn.innerHTML;
            elements.copyBtn.innerHTML = 'Copiado!';
            elements.copyBtn.style.background = '#DCFCE7';
            
            setTimeout(() => {
                elements.copyBtn.innerHTML = originalText;
                elements.copyBtn.style.background = '';
            }, 2000);
            
        } catch (error) {
            showError('Erro ao copiar texto');
        }
    });
}

// ==================== UI HELPERS ====================

function showLoading() {
    elements.loadingOverlay.style.display = 'flex';
}

function hideLoading() {
    elements.loadingOverlay.style.display = 'none';
}

function showResults() {
    elements.resultsSection.style.display = 'block';
}

function hideResults() {
    elements.resultsSection.style.display = 'none';
}

function showError(message) {
    elements.errorText.textContent = message;
    elements.errorMessage.style.display = 'flex';
    
    // Auto-hide após 5 segundos
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    elements.errorMessage.style.display = 'none';
}

// Close error button
elements.closeErrorBtn.addEventListener('click', hideError);

// ==================== API HEALTH CHECK ====================

async function checkAPIHealth() {
    try {
        const health = await window.apiClient.healthCheck();
        console.log('API Health:', health);
    } catch (error) {
        console.warn('API não está respondendo. Verifique se o backend está rodando.');
        // Não mostrar erro para não alarmar o usuário na primeira carga
    }
}
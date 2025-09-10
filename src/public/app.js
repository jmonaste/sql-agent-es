class SQLAgent {
    constructor() {
        this.apiUrl = '/api';
        this.pythonUrl = 'http://localhost:5000';
        this.init();
    }

    init() {
        this.bindEvents();
        this.checkHealth();
    }

    bindEvents() {
        // Eventos principales
        const translateBtn = document.getElementById('translateBtn');
        const executeBtn = document.getElementById('executeBtn');
        const clearAllBtn = document.getElementById('clearAllBtn');
        const clearSqlBtn = document.getElementById('clearSqlBtn');
        const tablesBtn = document.getElementById('tablesBtn');
        const naturalQuery = document.getElementById('naturalQuery');
        const sqlQuery = document.getElementById('sqlQuery');

        if (translateBtn) translateBtn.addEventListener('click', () => this.translateToSQL());
        if (executeBtn) executeBtn.addEventListener('click', () => this.executeQuery());
        if (clearAllBtn) clearAllBtn.addEventListener('click', () => this.clearAll());
        if (clearSqlBtn) clearSqlBtn.addEventListener('click', () => this.clearSQL());
        if (tablesBtn) tablesBtn.addEventListener('click', () => this.showTables());
        
        // Atajos de teclado
        if (naturalQuery) {
            naturalQuery.addEventListener('keydown', (e) => {
                if (e.ctrlKey && e.key === 'Enter') {
                    this.translateToSQL();
                }
            });
        }
        
        if (sqlQuery) {
            sqlQuery.addEventListener('keydown', (e) => {
                if (e.ctrlKey && e.key === 'Enter') {
                    this.executeQuery();
                }
            });
        }
    }

    async checkHealth() {
        try {
            const response = await fetch(`${this.apiUrl}/health`);
            const data = await response.json();
            
            const statusElement = document.getElementById('status');
            const statusText = document.getElementById('status-text');
            
            if (data.status === 'ok' && data.database === 'connected') {
                statusElement.className = 'status-indicator connected';
                statusText.textContent = '✅ Conectado a SAKILA';
            } else {
                statusElement.className = 'status-indicator disconnected';
                statusText.textContent = '❌ Sin conexión a base de datos';
            }
        } catch (error) {
            const statusElement = document.getElementById('status');
            const statusText = document.getElementById('status-text');
            statusElement.className = 'status-indicator disconnected';
            statusText.textContent = '❌ Error de conexión';
        }
    }

    async executeQuery() {
        const query = document.getElementById('sqlQuery').value.trim();
        
        if (!query) {
            this.showError('Por favor, escriba una consulta SQL');
            return;
        }

        this.showLoading(true);
        this.clearResults();

        try {
            const response = await fetch(`${this.apiUrl}/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query })
            });

            const data = await response.json();

            if (data.success) {
                this.displayResults(data.data, data.rowCount);
            } else {
                this.showError(data.error || 'Error desconocido');
            }
        } catch (error) {
            this.showError('Error de conexión: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    async showTables() {
        this.showLoading(true);
        this.clearResults();

        try {
            const response = await fetch(`${this.apiUrl}/tables`);
            const data = await response.json();

            if (data.success) {
                const tables = data.tables.map(table => ({ Tabla: table }));
                this.displayResults(tables, tables.length);
            } else {
                this.showError(data.error || 'Error al obtener tablas');
            }
        } catch (error) {
            this.showError('Error de conexión: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    displayResults(data, rowCount) {
        const resultsContainer = document.getElementById('results');
        
        if (!data || data.length === 0) {
            resultsContainer.innerHTML = '<p class="no-results">No se encontraron resultados</p>';
            return;
        }

        const table = this.createTable(data);
        resultsContainer.innerHTML = `
            <div class="results-info">
                <span>📊 ${rowCount} filas encontradas</span>
            </div>
            ${table}
        `;
    }

    createTable(data) {
        if (!data || data.length === 0) return '';

        const headers = Object.keys(data[0]);
        
        const headerRow = headers.map(header => `<th>${header}</th>`).join('');
        
        const dataRows = data.map(row => {
            const cells = headers.map(header => {
                const value = row[header];
                const displayValue = value === null ? '<em>NULL</em>' : String(value);
                return `<td>${displayValue}</td>`;
            }).join('');
            return `<tr>${cells}</tr>`;
        }).join('');

        return `
            <div class="table-container">
                <table class="results-table">
                    <thead>
                        <tr>${headerRow}</tr>
                    </thead>
                    <tbody>
                        ${dataRows}
                    </tbody>
                </table>
            </div>
        `;
    }

    clearQuery() {
        this.clearSQL();
        this.clearResults();
    }

    clearResults() {
        document.getElementById('results').innerHTML = '';
        document.getElementById('error').className = 'error-message hidden';
    }

    showError(message, type = 'error') {
        const errorElement = document.getElementById('error');
        const icon = type === 'warning' ? '⚠️' : '❌';
        errorElement.textContent = icon + ' ' + message;
        errorElement.className = `error-message ${type}`;
    }

    showLoading(show, message = 'Ejecutando consulta...') {
        const loading = document.getElementById('loading');
        const loadingText = loading.querySelector('span');
        
        if (loadingText) {
            loadingText.textContent = message;
        }
        
        loading.className = show ? 'loading' : 'loading hidden';
    }

    async translateToSQL() {
        const naturalQuery = document.getElementById('naturalQuery').value.trim();
        
        if (!naturalQuery) {
            this.showError('Por favor, escriba una consulta en lenguaje natural');
            return;
        }

        this.showLoading(true, 'Traduciendo a SQL...');
        this.clearResults();
        
        try {
            const response = await this.callPythonService('/generate-sql', {
                query: naturalQuery
            });

            if (response.success) {
                this.displayGeneratedSQL(response);
            } else {
                this.showError(response.error || 'Error al traducir la consulta');
            }
        } catch (error) {
            this.showError('Error de conexión con el servicio Python: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    displayGeneratedSQL(response) {
        const sqlTextarea = document.getElementById('sqlQuery');
        const modelInfo = document.getElementById('modelInfo');
        const sqlInfoPanel = document.getElementById('sqlInfoPanel');
        const explanationText = document.getElementById('explanationText');
        const considerationsText = document.getElementById('considerationsText');
        const alternativesText = document.getElementById('alternativesText');
        
        // Colocar el SQL generado en el textarea principal
        sqlTextarea.value = response.sql_query;
        
        // Mostrar información del modelo
        if (response.llm_info) {
            modelInfo.textContent = `🤖 Generado por ${response.llm_info.model} (${response.llm_info.provider})`;
            modelInfo.classList.remove('hidden');
        }
        
        // Mostrar panel lateral con información adicional
        if (response.explanation || response.considerations || response.alternatives) {
            explanationText.textContent = response.explanation || 'No disponible';
            considerationsText.textContent = response.considerations || 'No disponible';
            alternativesText.textContent = response.alternatives || 'No disponible';
            sqlInfoPanel.classList.remove('hidden');
        }
        
        // Mostrar información de validación si hay advertencias
        if (response.validation && response.validation.warnings && response.validation.warnings.length > 0) {
            const warnings = response.validation.warnings.join(', ');
            this.showError('⚠️ Advertencia: ' + warnings, 'warning');
        }
    }

    clearAll() {
        document.getElementById('naturalQuery').value = '';
        document.getElementById('sqlQuery').value = '';
        document.getElementById('modelInfo').classList.add('hidden');
        document.getElementById('sqlInfoPanel').classList.add('hidden');
        this.clearResults();
    }

    clearSQL() {
        document.getElementById('sqlQuery').value = '';
        document.getElementById('modelInfo').classList.add('hidden');
        document.getElementById('sqlInfoPanel').classList.add('hidden');
    }

    async callPythonService(endpoint, data = {}) {
        try {
            const response = await fetch(`${this.pythonUrl}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.log('Servicio Python no disponible:', error.message);
            throw new Error('Servicio Python no disponible en puerto 5000');
        }
    }
}


document.addEventListener('DOMContentLoaded', () => {
    new SQLAgent();
});
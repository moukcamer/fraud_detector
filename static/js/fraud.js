// FRAUD DETECTOR CM - JavaScript Principal
let transactions = [];
let alerts = [];

// Dashboard Admin - Mise à jour automatique
async function loadDashboardData() {
    try {
        const response = await fetch('/api/dashboard/');
        const data = await response.json();
        
        // Met à jour les stats
        document.getElementById('total-transactions').textContent = data.total_transactions.toLocaleString();
        document.getElementById('frauds-detected').textContent = data.frauds_detected.toLocaleString();
        document.getElementById('detection-rate').textContent = data.detection_rate + '%';
        document.getElementById('avg-score').textContent = data.avg_score.toFixed(3);
        
        // Met à jour le tableau
        updateTransactionsTable(data.recent_transactions);
        
        // Met à jour les alertes
        updateAlertsList(data.active_alerts);
        
        // Met à jour le graphique
        updateChart(data.fraud_distribution);
        
        console.log('✅ Dashboard mis à jour');
    } catch (error) {
        console.error('Erreur dashboard:', error);
    }
}

// Met à jour le tableau des transactions
function updateTransactionsTable(transactions) {
    const tbody = document.getElementById('transactions-table');
    tbody.innerHTML = '';
    
    transactions.forEach(tx => {
        const row = document.createElement('tr');
        const statusClass = tx.is_flagged ? 'fraud' : 'legit';
        const statusIcon = tx.is_flagged ? '🚨' : '✅';
        
        row.innerHTML = `
            <td><strong>${tx.transaction_id}</strong></td>
            <td>${formatCurrency(tx.amount)} FCFA</td>
            <td>**** ${tx.card_last4}</td>
            <td>${tx.merchant}</td>
            <td>
                <div class="score-badge ${statusClass}">
                    ${tx.fraud_score.toFixed(3)}
                </div>
            </td>
            <td>
                <span class="status ${statusClass}">
                    ${statusIcon} ${tx.is_flagged ? 'FRAUDE' : 'Légitime'}
                </span>
            </td>
            <td>${formatDate(tx.created_at)}</td>
        `;
        tbody.appendChild(row);
    });
}

// Met à jour les alertes
function updateAlertsList(alerts) {
    const container = document.getElementById('alerts-list');
    container.innerHTML = '';
    
    alerts.forEach(alert => {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert-item fraud';
        alertDiv.innerHTML = `
            <div class="alert-header">
                <i class="fas fa-exclamation-triangle"></i>
                <strong>${alert.transaction_id}</strong>
            </div>
            <div class="alert-body">
                <p>${formatCurrency(alert.amount)} FCFA</p>
                <p>Score: ${alert.fraud_score.toFixed(3)}</p>
                <small>${formatDate(alert.created_at)}</small>
            </div>
        `;
        container.appendChild(alertDiv);
    });
    
    if (alerts.length === 0) {
        container.innerHTML = '<p class="text-muted">✅ Aucune alerte active</p>';
    }
}

// Graphique des fraudes
let fraudChart;
function updateChart(distribution) {
    const ctx = document.getElementById('fraudChart').getContext('2d');
    
    if (fraudChart) fraudChart.destroy();
    
    fraudChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Légitimes', 'Fraudes'],
            datasets: [{
                data: [distribution.legit, distribution.fraud],
                backgroundColor: ['#28a745', '#dc3545'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Test transaction rapide
async function testTransaction(amount, isFraud = false) {
    const testData = {
        transaction_id: `TEST_${Date.now()}`,
        amount: amount,
        card_last4: '1234',
        merchant: isFraud ? 'Site suspect' : 'Super Marche',
        Time: 0
    };
    
    // Ajoute les features V1-V28 (simplifiées)
    for (let i = 1; i <= 28; i++) {
        testData[`V${i}`] = isFraud ? -5 + Math.random() * 10 : Math.random() * 2 - 1;
    }
    
    try {
        const response = await fetch('/api/check/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(testData)
        });
        
        const result = await response.json();
        showResult(testData, result);
        return result;
    } catch (error) {
        console.error('Erreur test:', error);
    }
}

// Utilitaires
function formatCurrency(amount) {
    return new Intl.NumberFormat('fr-FR').format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleString('fr-FR');
}

// Animation des scores
function animateScore(element, target) {
    let start = 0;
    const duration = 1000;
    const startTime = performance.now();
    
    function step(currentTime) {
        const progress = Math.min((currentTime - startTime) / duration, 1);
        const current = start + (target - start) * progress;
        
        element.textContent = current.toFixed(3);
        
        if (progress < 1) {
            requestAnimationFrame(step);
        }
    }
    
    requestAnimationFrame(step);
}

// Tests automatiques (démarre toutes les 10s)
setInterval(() => {
    if (Math.random() > 0.8) {
        testTransaction(2500000, true); // Fraude
    } else {
        testTransaction(45000, false); // Légitime
    }
}, 10000);

// Export pour autres fichiers
window.FraudDetector = {
    testTransaction,
    loadDashboardData,
    animateScore
};
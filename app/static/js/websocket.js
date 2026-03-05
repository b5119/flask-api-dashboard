/**
 * WebSocket client for real-time updates
 */

// Initialize Socket.IO connection
const socket = io('/crypto');

// Connection events
socket.on('connect', () => {
    console.log('✅ Connected to crypto WebSocket');
    Toast.success('Connected to live price feed');
    
    // Subscribe to coins
    const coins = ['bitcoin', 'ethereum', 'cardano'];
    socket.emit('subscribe', { coins: coins });
});

socket.on('disconnect', () => {
    console.log('❌ Disconnected from crypto WebSocket');
    Toast.warning('Disconnected from live price feed');
});

// Price update events
socket.on('crypto_update', (prices) => {
    console.log('📊 Received price update:', prices);
    updateCryptoPrices(prices);
});

// Subscription confirmation
socket.on('subscribed', (data) => {
    console.log('✅ Subscribed to:', data.coins);
});

/**
 * Update cryptocurrency prices in UI
 */
function updateCryptoPrices(prices) {
    Object.keys(prices).forEach(coin => {
        const element = document.getElementById(`price-${coin}`);
        
        if (element) {
            const oldPrice = parseFloat(element.textContent.replace('$', '').replace(',', ''));
            const newPrice = prices[coin].usd;
            
            // Update price
            element.textContent = `$${newPrice.toLocaleString()}`;
            
            // Add animation class
            if (newPrice > oldPrice) {
                element.classList.add('price-up');
                setTimeout(() => element.classList.remove('price-up'), 1000);
            } else if (newPrice < oldPrice) {
                element.classList.add('price-down');
                setTimeout(() => element.classList.remove('price-down'), 1000);
            }
            
            // Check price alerts
            checkPriceAlerts(coin, newPrice);
        }
    });
}

/**
 * Check if any price alerts should be triggered
 */
function checkPriceAlerts(coinId, currentPrice) {
    const alerts = JSON.parse(localStorage.getItem('crypto_alerts') || '[]');
    
    alerts.forEach((alert, index) => {
        if (alert.coinId === coinId && !alert.triggered) {
            let shouldTrigger = false;
            
            if (alert.condition === 'above' && currentPrice >= alert.targetPrice) {
                shouldTrigger = true;
            } else if (alert.condition === 'below' && currentPrice <= alert.targetPrice) {
                shouldTrigger = true;
            }
            
            if (shouldTrigger) {
                // Mark as triggered
                alerts[index].triggered = true;
                localStorage.setItem('crypto_alerts', JSON.stringify(alerts));
                
                // Show notification
                Toast.warning(
                    `${coinId.toUpperCase()} ${alert.condition} $${alert.targetPrice}!`,
                    5000
                );
                
                // Browser notification
                if ('Notification' in window && Notification.permission === 'granted') {
                    new Notification(`Price Alert: ${coinId.toUpperCase()}`, {
                        body: `Current price: $${currentPrice.toLocaleString()}`,
                        icon: '/static/img/crypto-icon.png'
                    });
                }
            }
        }
    });
}

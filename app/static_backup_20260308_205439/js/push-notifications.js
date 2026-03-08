/**
 * Browser Push Notifications
 */

const PushNotifications = {
    permission: null,
    
    /**
     * Request notification permission
     */
    async requestPermission() {
        if (!('Notification' in window)) {
            console.warn('This browser does not support notifications');
            return false;
        }
        
        this.permission = await Notification.requestPermission();
        
        if (this.permission === 'granted') {
            Toast.success('Notifications enabled!');
            return true;
        } else if (this.permission === 'denied') {
            Toast.error('Notifications blocked');
            return false;
        }
        
        return false;
    },
    
    /**
     * Send browser notification
     */
    send(title, options = {}) {
        if (Notification.permission !== 'granted') {
            return;
        }
        
        const defaultOptions = {
            icon: '/static/img/logo.png',
            badge: '/static/img/badge.png',
            vibrate: [200, 100, 200],
            requireInteraction: false
        };
        
        const notification = new Notification(title, {
            ...defaultOptions,
            ...options
        });
        
        // Auto-close after 5 seconds
        setTimeout(() => notification.close(), 5000);
        
        // Click handler
        notification.onclick = () => {
            window.focus();
            notification.close();
            if (options.url) {
                window.location.href = options.url;
            }
        };
        
        return notification;
    },
    
    /**
     * Send price alert notification
     */
    sendPriceAlert(coin, price, condition) {
        const emoji = condition === 'above' ? '🚀' : '📉';
        
        this.send(`${emoji} ${coin.toUpperCase()} Price Alert!`, {
            body: `${coin} has ${condition} $${price.toLocaleString()}`,
            tag: `price-alert-${coin}`,
            renotify: true
        });
    },
    
    /**
     * Send news notification
     */
    sendNewsAlert(article) {
        this.send('📰 Breaking News', {
            body: article.title,
            tag: 'news-alert',
            url: article.url
        });
    }
};

// Make available globally
window.PushNotifications = PushNotifications;

// Request permission on page load (optional)
document.addEventListener('DOMContentLoaded', () => {
    // Show notification permission button
    const notifButton = document.getElementById('enable-notifications');
    
    if (notifButton && Notification.permission === 'default') {
        notifButton.addEventListener('click', () => {
            PushNotifications.requestPermission();
        });
    }
});

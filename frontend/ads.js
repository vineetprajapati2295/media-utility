// Ad Management Script
// Handles loading and displaying ads from various networks

class AdManager {
    constructor() {
        this.adNetworks = {
            propellerads: {
                enabled: false,
                scriptUrl: 'https://propellerads.com/popunder.js',
                siteId: 'YOUR_SITE_ID' // Replace with your actual site ID
            },
            adsterra: {
                enabled: false,
                scriptUrl: 'https://ads.adsterra.net/render.js',
                siteId: 'YOUR_SITE_ID' // Replace with your actual site ID
            },
            custom: {
                enabled: true, // Enable custom/self-hosted ads
                ads: []
            }
        };
    }

    init() {
        // Load ads after page load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.loadAds());
        } else {
            this.loadAds();
        }
    }

    loadAds() {
        // Load custom ads first
        if (this.adNetworks.custom.enabled) {
            this.loadCustomAds();
        }

        // Load third-party ad networks (uncomment and configure)
        // if (this.adNetworks.propellerads.enabled) {
        //     this.loadPropellerAds();
        // }
        // if (this.adNetworks.adsterra.enabled) {
        //     this.loadAdsterra();
        // }
    }

    loadCustomAds() {
        // Example: Load custom banner ads
        const adContainers = document.querySelectorAll('.ad-container[data-ad-type="custom"]');
        
        adContainers.forEach((container, index) => {
            // You can replace this with your actual ad content
            // For now, showing placeholder that you can replace with real ads
            container.innerHTML = this.getCustomAdHTML(index);
        });
    }

    getCustomAdHTML(adIndex) {
        // Replace these with your actual ad HTML
        const ads = [
            // Ad 1 - Banner
            `
            <div class="ad-banner">
                <a href="https://example.com/affiliate-link" target="_blank" rel="nofollow sponsored">
                    <img src="https://via.placeholder.com/728x90/1a1f3a/00d4ff?text=Your+Ad+Here" alt="Advertisement" style="width: 100%; height: auto; border-radius: 8px;">
                </a>
                <span class="ad-label">Advertisement</span>
            </div>
            `,
            // Ad 2 - Square
            `
            <div class="ad-square">
                <a href="https://example.com/affiliate-link" target="_blank" rel="nofollow sponsored">
                    <div class="ad-content">
                        <h4>Recommended Tool</h4>
                        <p>Get the best video editing software</p>
                        <span class="ad-cta">Learn More →</span>
                    </div>
                </a>
                <span class="ad-label">Advertisement</span>
            </div>
            `,
            // Ad 3 - Text Link
            `
            <div class="ad-text-links">
                <p class="ad-label">Sponsored Links</p>
                <ul>
                    <li><a href="https://example.com/link1" target="_blank" rel="nofollow sponsored">Video Converter Pro</a></li>
                    <li><a href="https://example.com/link2" target="_blank" rel="nofollow sponsored">Media Storage Solution</a></li>
                    <li><a href="https://example.com/link3" target="_blank" rel="nofollow sponsored">Cloud Backup Service</a></li>
                </ul>
            </div>
            `
        ];

        return ads[adIndex % ads.length] || ads[0];
    }

    loadPropellerAds() {
        // PropellerAds integration
        if (typeof window.PropellerAds === 'undefined') {
            const script = document.createElement('script');
            script.src = this.adNetworks.propellerads.scriptUrl;
            script.async = true;
            script.setAttribute('data-site-id', this.adNetworks.propellerads.siteId);
            document.head.appendChild(script);
        }
    }

    loadAdsterra() {
        // Adsterra integration
        if (typeof window.adsterra === 'undefined') {
            const script = document.createElement('script');
            script.src = this.adNetworks.adsterra.scriptUrl;
            script.async = true;
            script.setAttribute('data-site-id', this.adNetworks.adsterra.siteId);
            document.head.appendChild(script);
        }
    }

    // Method to refresh ads
    refreshAds() {
        const adContainers = document.querySelectorAll('.ad-container');
        adContainers.forEach(container => {
            if (container.dataset.adType === 'custom') {
                const index = parseInt(container.dataset.adIndex || '0');
                container.innerHTML = this.getCustomAdHTML(index);
            }
        });
    }
}

// Initialize ad manager
const adManager = new AdManager();
adManager.init();

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdManager;
}


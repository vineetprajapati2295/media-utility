# Ad Integration Guide

## Quick Setup

### Option 1: Custom/Self-Hosted Ads (Recommended to Start)

1. **Edit `frontend/ads.js`**:
   - Replace placeholder ad HTML with your actual ad content
   - Update affiliate links
   - Add your banner images

2. **Ad HTML Structure**:
   ```html
   <div class="ad-banner">
       <a href="YOUR_AFFILIATE_LINK" target="_blank" rel="nofollow sponsored">
           <img src="YOUR_BANNER_IMAGE_URL" alt="Advertisement">
       </a>
       <span class="ad-label">Advertisement</span>
   </div>
   ```

3. **Ad Placement**:
   - Top banner: Above main card
   - Bottom banner: Below legal notice
   - Sidebar: Can be enabled for larger screens

### Option 2: PropellerAds (CPA Network)

1. **Sign up**: https://propellerads.com
2. **Get Site ID**: From your PropellerAds dashboard
3. **Edit `frontend/ads.js`**:
   ```javascript
   propellerads: {
       enabled: true,  // Change to true
       siteId: 'YOUR_ACTUAL_SITE_ID'  // Replace with your ID
   }
   ```
4. **Uncomment in `loadAds()` method**:
   ```javascript
   if (this.adNetworks.propellerads.enabled) {
       this.loadPropellerAds();
   }
   ```

### Option 3: Adsterra (CPA Network)

1. **Sign up**: https://adsterra.com
2. **Get Site ID**: From your Adsterra dashboard
3. **Edit `frontend/ads.js`**:
   ```javascript
   adsterra: {
       enabled: true,  // Change to true
       siteId: 'YOUR_ACTUAL_SITE_ID'  // Replace with your ID
   }
   ```
4. **Uncomment in `loadAds()` method**:
   ```javascript
   if (this.adNetworks.adsterra.enabled) {
       this.loadAdsterra();
   }
   ```

### Option 4: Direct Banner Sales

1. **Create ad zones** in your HTML (already done)
2. **Sell ad space** directly to advertisers
3. **Replace ad content** in `ads.js` with advertiser's HTML
4. **Track impressions/clicks** manually or with analytics

## Ad Networks Comparison

| Network | Type | Payout | Best For |
|---------|------|--------|----------|
| **PropellerAds** | CPA/CPM | High | Pop-unders, native ads |
| **Adsterra** | CPA/CPM | Medium-High | Banners, pop-unders |
| **Custom/Self-hosted** | Direct | Variable | Full control, affiliate links |
| **AdMaven** | CPA | High | Various formats |
| **RevenueHits** | CPA | Medium | Multiple ad types |

## Implementation Steps

### Step 1: Choose Your Ad Network

For beginners, start with **custom/self-hosted ads**:
- No approval process
- Full control
- Use affiliate links
- Easy to implement

### Step 2: Configure Ads

**For Custom Ads:**
1. Open `frontend/ads.js`
2. Find `getCustomAdHTML()` method
3. Replace placeholder HTML with your ads:
   ```javascript
   const ads = [
       `
       <div class="ad-banner">
           <a href="https://your-affiliate-link.com" target="_blank" rel="nofollow sponsored">
               <img src="https://your-banner-image.com/banner.jpg" alt="Ad">
           </a>
           <span class="ad-label">Advertisement</span>
       </div>
       `,
       // Add more ads...
   ];
   ```

**For CPA Networks:**
1. Sign up for network
2. Get your site ID
3. Enable in `ads.js`
4. Uncomment loading code

### Step 3: Test Ads

1. Open browser console (F12)
2. Check for errors
3. Verify ads load correctly
4. Test on mobile and desktop

### Step 4: Monitor Performance

- **Custom ads**: Use UTM parameters
  ```
  https://affiliate-link.com?utm_source=media-utility&utm_medium=banner
  ```
- **CPA networks**: Check dashboard for stats
- **Analytics**: Add Google Analytics events

## Ad Placement Best Practices

1. **Above the fold**: Top banner gets most views
2. **Below content**: Bottom banner for users who scroll
3. **Sidebar**: Good for desktop, hide on mobile
4. **Between sections**: Can be effective but don't overdo it

## Legal Requirements

1. **Disclosure**: Always label ads as "Advertisement" or "Sponsored"
2. **Rel attribute**: Use `rel="nofollow sponsored"` on ad links
3. **Privacy**: If using tracking, add privacy policy
4. **GDPR**: For EU users, may need consent for some ad networks

## Revenue Optimization Tips

1. **A/B Testing**: Test different ad placements
2. **Mobile Optimization**: Ensure ads work on mobile
3. **Loading Speed**: Don't let ads slow down your site
4. **User Experience**: Balance ads with UX
5. **Multiple Networks**: Rotate between networks for best rates

## Example: Adding Amazon Affiliate Banner

```javascript
getCustomAdHTML(adIndex) {
    const ads = [
        `
        <div class="ad-banner">
            <a href="https://amazon.com/dp/PRODUCT_ID?tag=YOUR_TAG" 
               target="_blank" 
               rel="nofollow sponsored">
                <img src="https://your-banner-host.com/amazon-banner.jpg" 
                     alt="Amazon Product">
            </a>
            <span class="ad-label">Advertisement</span>
        </div>
        `,
        // More ads...
    ];
    return ads[adIndex % ads.length];
}
```

## Troubleshooting

**Ads not showing?**
- Check browser console for errors
- Verify ad network script loaded
- Check ad container exists in HTML
- Ensure `ads.js` is loaded before `app.js`

**Low revenue?**
- Try different ad placements
- Test different ad networks
- Optimize for your audience
- Consider direct ad sales

**Ad blocking?**
- Many users have ad blockers
- Consider native/content ads
- Offer ad-free premium option
- Focus on affiliate links

## Next Steps

1. ✅ Choose ad method (start with custom)
2. ✅ Configure `ads.js`
3. ✅ Test ads locally
4. ✅ Deploy and monitor
5. ✅ Optimize based on performance

For more details, see `MONETIZATION.md`


# Website Integration Guide

## Overview

This guide explains how the luxor9app.com website integrates with the LUXORANOVA platform and how to deploy it.

## Website Structure

The website is a static single-page application (SPA) that serves as the public-facing landing page for the LUXORANOVA Enterprise AI Platform.

### Directory Structure

```
website/
├── index.html          # Main landing page
├── css/
│   └── style.css      # Comprehensive styling
├── js/
│   └── main.js        # Interactive functionality
├── images/            # Image assets (empty, add as needed)
├── assets/            # Additional assets (empty, add as needed)
├── README.md          # Documentation
├── DEPLOYMENT.md      # Deployment guide
├── Dockerfile         # Container deployment
├── nginx.conf         # Web server configuration
├── netlify.toml       # Netlify configuration
├── robots.txt         # SEO crawling rules
├── sitemap.xml        # SEO sitemap
├── start.sh           # Quick start script
└── .gitignore         # Git ignore rules
```

## Integration with Main Platform

### Option 1: Separate Deployment (Recommended)

Deploy the website separately from the main platform:

1. **Different Domain/Subdomain**
   - Main Platform: `app.luxor9app.com` or `api.luxor9app.com`
   - Website: `luxor9app.com` or `www.luxor9app.com`

2. **Benefits**
   - Independent scaling
   - Faster static site delivery
   - Simplified CDN integration
   - Lower hosting costs for static content

### Option 2: Integrated Deployment

Serve the website from the main platform:

1. **Add to Backend**
   ```python
   # In backend/main.py, add:
   from fastapi.staticfiles import StaticFiles
   
   app.mount("/", StaticFiles(directory="../website", html=True), name="website")
   ```

2. **Update Docker Compose**
   ```yaml
   # In docker-compose.yml, add volume:
   volumes:
     - ./website:/app/website
   ```

## Deployment Options

### 1. Netlify (Easiest)

Perfect for static sites with automatic SSL and CDN.

```bash
cd website
netlify deploy --prod
```

Configuration is already set in `netlify.toml`.

### 2. Vercel

Similar to Netlify, excellent for static sites.

```bash
cd website
vercel --prod
```

### 3. Docker + Cloud (AWS/GCP/Azure)

For more control and integration with existing infrastructure.

```bash
# Build image
docker build -t luxoranova-website:latest website/

# Push to registry
docker tag luxoranova-website:latest your-registry/luxoranova-website:latest
docker push your-registry/luxoranova-website:latest

# Deploy to cloud
# (Use cloud-specific commands)
```

### 4. Kubernetes

Add to existing Kubernetes deployment:

```yaml
# Create deployment file: infra/kubernetes/website-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: luxoranova-website
spec:
  replicas: 2
  selector:
    matchLabels:
      app: luxoranova-website
  template:
    metadata:
      labels:
        app: luxoranova-website
    spec:
      containers:
      - name: website
        image: your-registry/luxoranova-website:latest
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: luxoranova-website-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: luxoranova-website
```

## DNS Configuration

### Primary Domain (luxor9app.com)

```
Type    Name    Value                           TTL
A       @       <hosting-ip-or-cdn-address>     300
CNAME   www     luxor9app.com                   300
```

### Subdomain for API (if needed)

```
Type    Name    Value                           TTL
CNAME   api     backend-service.provider.com    300
CNAME   app     frontend-service.provider.com   300
```

## SSL/TLS Certificate

### Automatic (Recommended)
- Netlify/Vercel: Automatic Let's Encrypt
- Cloudflare: Free Universal SSL

### Manual (Self-hosted)
```bash
# Using Certbot
certbot --nginx -d luxor9app.com -d www.luxor9app.com
```

## Performance Optimization

### CDN Setup
1. Use Netlify/Vercel built-in CDN
2. Or configure CloudFlare for existing setup
3. Or use AWS CloudFront

### Caching Strategy
```nginx
# Already configured in nginx.conf
location ~* \.(css|js|jpg|png|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

## Monitoring & Analytics

### Add Google Analytics
1. Create GA4 property
2. Add tracking code to `index.html`:

```html
<!-- Add before </head> -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Uptime Monitoring
- UptimeRobot: Free tier available
- Pingdom: More detailed monitoring
- StatusCake: Alternative option

## Contact Form Backend

Currently, the form is frontend-only. To make it functional:

### Option 1: Netlify Forms
```html
<!-- Update form in index.html -->
<form name="contact" method="POST" data-netlify="true">
  <!-- existing form fields -->
</form>
```

### Option 2: Custom API Endpoint
```javascript
// Update in js/main.js
const response = await fetch('https://api.luxor9app.com/contact', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
});
```

### Option 3: Third-party Service
- Formspree
- SendGrid
- EmailJS

## Security Considerations

### Headers
Already configured in `nginx.conf`:
- X-Frame-Options
- X-Content-Type-Options
- X-XSS-Protection
- Content-Security-Policy

### HTTPS
- Always use HTTPS in production
- Redirect HTTP to HTTPS
- Use HSTS header

## Testing

### Local Testing
```bash
# Run local server
cd website
./start.sh
# Select option 1 or 2
```

### Automated Testing
```bash
# Validate files
cd website
./start.sh
# Select option 7
```

## Maintenance

### Regular Updates
- Update content in `index.html`
- Refresh styles in `css/style.css`
- Update features and platform info as needed

### Version Control
- Keep website in sync with platform releases
- Tag releases for rollback capability

## Troubleshooting

### Issue: Website not loading
- Check DNS propagation: `nslookup luxor9app.com`
- Verify deployment status in hosting dashboard
- Check browser console for errors

### Issue: Styles not loading
- Clear browser cache
- Check network tab for 404s
- Verify file paths are correct

### Issue: Contact form not working
- Check console for JavaScript errors
- Verify form submission endpoint
- Check CORS settings if using custom API

## Support

For deployment issues or questions, refer to:
- `README.md` - General information
- `DEPLOYMENT.md` - Detailed deployment guide
- Platform documentation in `/docs`

## Next Steps

1. Choose deployment method
2. Configure DNS settings
3. Set up SSL certificate
4. Deploy website
5. Configure monitoring
6. Test all functionality
7. Announce launch!

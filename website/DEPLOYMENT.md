# LUXORANOVA Website Deployment Guide

## Quick Deployment Options

### Option 1: Netlify (Recommended for Quick Setup)

#### Using Netlify UI
1. Go to [Netlify](https://www.netlify.com/)
2. Click "Add new site" → "Import an existing project"
3. Connect your GitHub repository
4. Configure build settings:
   - Base directory: `website`
   - Build command: (leave empty)
   - Publish directory: `.`
5. Click "Deploy site"
6. Add custom domain: `luxor9app.com` in Site settings → Domain management

#### Using Netlify CLI
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy from website directory
cd website
netlify deploy --prod --dir .
```

### Option 2: Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd website
vercel --prod
```

### Option 3: GitHub Pages

1. Ensure the website directory is in your repository
2. Go to repository Settings → Pages
3. Select source: Deploy from a branch
4. Choose branch (e.g., `main`) and folder `/website`
5. Save

### Option 4: AWS S3 + CloudFront

#### Step 1: Create S3 Bucket
```bash
# Create bucket
aws s3 mb s3://luxor9app.com

# Enable static website hosting
aws s3 website s3://luxor9app.com --index-document index.html --error-document index.html

# Upload files
cd website
aws s3 sync . s3://luxor9app.com --delete --acl public-read
```

#### Step 2: Setup CloudFront
```bash
# Create CloudFront distribution (use AWS Console or CLI)
# Point origin to S3 bucket
# Configure SSL certificate from AWS Certificate Manager
```

### Option 5: Docker + VPS/Cloud

#### Build Docker Image
```bash
cd website
docker build -t luxoranova-website:latest .
```

#### Run Locally
```bash
docker run -d -p 80:80 --name luxoranova-web luxoranova-website:latest
```

#### Deploy to Container Registry
```bash
# Tag image
docker tag luxoranova-website:latest your-registry/luxoranova-website:latest

# Push to registry
docker push your-registry/luxoranova-website:latest
```

#### Deploy to Cloud (Example: DigitalOcean)
```bash
# SSH into your droplet
ssh root@your-droplet-ip

# Pull and run container
docker pull your-registry/luxoranova-website:latest
docker run -d -p 80:80 --name luxoranova-web your-registry/luxoranova-website:latest
```

## Custom Domain Configuration

### DNS Settings for luxor9app.com

#### For Netlify/Vercel:
```
Type    Name    Value
A       @       (provided by hosting)
CNAME   www     (provided by hosting)
```

#### For AWS CloudFront:
```
Type    Name    Value
A       @       (CloudFront distribution domain)
CNAME   www     luxor9app.com
```

### SSL Certificate

#### Automatic SSL (Netlify/Vercel)
- SSL is automatically provisioned and renewed

#### Let's Encrypt (Self-hosted)
```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d luxor9app.com -d www.luxor9app.com

# Auto-renewal is configured automatically
```

#### AWS Certificate Manager
1. Go to ACM console
2. Request a certificate for `luxor9app.com` and `*.luxor9app.com`
3. Verify domain ownership via DNS or email
4. Attach certificate to CloudFront distribution

## Environment-Specific Configuration

### Production
- Ensure all API endpoints point to production URLs
- Enable analytics (Google Analytics, etc.)
- Configure error tracking (Sentry, etc.)
- Enable CDN caching

### Staging
- Use staging API endpoints
- Disable analytics
- Enable debug logging

## Performance Optimization

### Before Deployment
```bash
# Minify CSS
npx cssnano css/style.css css/style.min.css

# Minify JavaScript
npx terser js/main.js -o js/main.min.js

# Update references in index.html
```

### Image Optimization
```bash
# Install imagemin
npm install -g imagemin-cli

# Optimize images
imagemin images/* --out-dir=images
```

## Monitoring & Analytics

### Add Google Analytics
Add to `<head>` in index.html:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Uptime Monitoring
- Use services like UptimeRobot, Pingdom, or StatusCake
- Monitor `https://luxor9app.com`

## Troubleshooting

### Issue: Site not loading
- Check DNS propagation: `nslookup luxor9app.com`
- Verify SSL certificate is valid
- Check server/hosting logs

### Issue: Styles not loading
- Clear browser cache
- Check console for CORS errors
- Verify CSS file paths are correct

### Issue: Form not working
- Check console for JavaScript errors
- Verify API endpoint is configured
- Test form submission in developer tools

## Rollback Procedure

### Netlify/Vercel
- Go to Deployments
- Click on previous successful deployment
- Click "Publish deploy"

### Docker
```bash
# Stop current container
docker stop luxoranova-web

# Run previous version
docker run -d -p 80:80 --name luxoranova-web your-registry/luxoranova-website:previous-tag
```

## Support

For deployment issues, contact the DevOps team or refer to the hosting provider's documentation.

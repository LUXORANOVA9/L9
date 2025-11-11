# LUXORANOVA Website

Official landing page for luxor9app.com - Enterprise AI Platform

## Overview

This is a modern, responsive website showcasing the LUXORANOVA Enterprise AI Platform with its key features, technology stack, and capabilities.

## Features

- **Responsive Design**: Fully responsive layout that works on all devices
- **Modern UI**: Clean, professional design with gradient effects and animations
- **Smooth Scrolling**: Seamless navigation between sections
- **Contact Form**: Interactive contact form for inquiries
- **Performance Optimized**: Minimal dependencies, fast loading times
- **SEO Ready**: Proper meta tags and semantic HTML structure

## Structure

```
website/
├── index.html          # Main HTML file
├── css/
│   └── style.css      # Main stylesheet
├── js/
│   └── main.js        # JavaScript functionality
├── images/            # Image assets (add as needed)
├── assets/            # Additional assets
└── README.md          # This file
```

## Technologies Used

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS Grid and Flexbox
- **Vanilla JavaScript**: No framework dependencies for maximum performance
- **Google Fonts**: Inter font family

## Deployment

### Static Hosting

This website can be deployed to any static hosting service:

#### Netlify
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd website
netlify deploy --prod
```

#### Vercel
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd website
vercel --prod
```

#### GitHub Pages
1. Push the `website` directory to your repository
2. Go to Settings → Pages
3. Select the branch and `/website` folder
4. Save and your site will be live at `https://yourusername.github.io/repo-name`

#### AWS S3 + CloudFront
```bash
# Sync to S3 bucket
aws s3 sync . s3://your-bucket-name --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

### Docker Deployment

A simple Nginx-based Docker setup:

```dockerfile
FROM nginx:alpine
COPY . /usr/share/nginx/html
EXPOSE 80
```

Build and run:
```bash
docker build -t luxoranova-website .
docker run -d -p 80:80 luxoranova-website
```

### Custom Domain Setup

1. **DNS Configuration**: Point your domain to your hosting provider
   - A Record: `@` → `your-server-ip`
   - CNAME: `www` → `your-domain.com`

2. **SSL Certificate**: Use Let's Encrypt or your hosting provider's SSL
   ```bash
   # Using Certbot
   certbot --nginx -d luxor9app.com -d www.luxor9app.com
   ```

## Customization

### Colors

Edit CSS variables in `css/style.css`:

```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --accent-color: #ec4899;
    /* ... other colors */
}
```

### Content

- **Hero Section**: Edit text in `index.html` under `<section class="hero">`
- **Features**: Modify feature cards in the features section
- **Contact Form**: Update form action endpoint in `js/main.js`

### Contact Form Backend

To make the contact form functional, you need to:

1. Create an API endpoint to receive form submissions
2. Update the form handler in `js/main.js`:

```javascript
// Replace the simulated API call with actual endpoint
const response = await fetch('https://api.luxor9app.com/contact', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
});
```

Popular form backend services:
- [Formspree](https://formspree.io/)
- [Netlify Forms](https://www.netlify.com/products/forms/)
- [SendGrid](https://sendgrid.com/)
- Custom API endpoint

## Performance Optimization

- **Minify CSS/JS**: Use tools like `cssnano` and `terser`
- **Image Optimization**: Compress images with `imagemin`
- **CDN**: Serve static assets through a CDN
- **Caching**: Configure proper cache headers

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## Development

To work on the website locally:

```bash
# Simple HTTP server with Python
cd website
python -m http.server 8080

# Or with Node.js
npx http-server -p 8080

# Or with PHP
php -S localhost:8080
```

Then open `http://localhost:8080` in your browser.

## License

Copyright © 2025 LUXORANOVA. All rights reserved.

## Support

For questions or issues, contact the LUXORANOVA team.

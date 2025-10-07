# Deployment Guide

This guide covers deploying the AI-Powered Personal Tutor platform to production.

## Prerequisites

- Python 3.10+
- Node.js 18+
- MongoDB 6.0+
- Redis 7.0+
- Docker & Docker Compose (optional)

## Environment Setup

### 1. Clone and Configure

```bash
git clone <repository-url>
cd "ai powered tutor"
cp .env.example .env
```

### 2. Update Environment Variables

Edit `.env` and set:
- `SECRET_KEY`: Django secret key
- `GEMINI_API_KEY`: Your Google Gemini API key
- `MONGODB_*`: MongoDB connection details
- `REDIS_URL`: Redis connection URL
- `ALLOWED_HOSTS`: Your domain names
- `CORS_ALLOWED_ORIGINS`: Frontend URLs

## Deployment Options

### Option 1: Docker Deployment (Recommended)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Admin Panel: http://localhost:8000/admin

### Option 2: Manual Deployment

#### Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Start Gunicorn
gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Build for production
npm run build

# Serve with nginx or any static server
```

#### Celery Worker

```bash
celery -A backend worker -l info
```

## Production Checklist

### Security

- [ ] Set `DEBUG=False` in production
- [ ] Use strong `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Configure HTTPS/SSL
- [ ] Set proper `ALLOWED_HOSTS`
- [ ] Configure CORS properly
- [ ] Use environment variables for sensitive data
- [ ] Enable Django security middleware
- [ ] Set up firewall rules

### Database

- [ ] MongoDB authentication enabled
- [ ] Regular backups configured
- [ ] Indexes created for performance
- [ ] Connection pooling configured

### Performance

- [ ] Static files served via CDN or nginx
- [ ] Media files stored in object storage (S3, etc.)
- [ ] Redis caching configured
- [ ] Database query optimization
- [ ] Gunicorn workers tuned
- [ ] Frontend build optimized

### Monitoring

- [ ] Sentry error tracking configured
- [ ] Application logs configured
- [ ] Server monitoring (CPU, memory, disk)
- [ ] Database monitoring
- [ ] API endpoint monitoring

### Backup

- [ ] Database backup strategy
- [ ] Media files backup
- [ ] ML models backup
- [ ] Configuration backup

## Cloud Deployment

### AWS Deployment

1. **EC2 Instance**
   - Launch Ubuntu 22.04 instance
   - Install Docker and Docker Compose
   - Clone repository and run docker-compose

2. **RDS/DocumentDB**
   - Use AWS DocumentDB for MongoDB
   - Update connection string in .env

3. **ElastiCache**
   - Use ElastiCache for Redis
   - Update Redis URL in .env

4. **S3**
   - Store media files in S3
   - Configure Django storage backend

5. **CloudFront**
   - Serve static files via CloudFront CDN

### Heroku Deployment

```bash
# Install Heroku CLI
heroku login

# Create app
heroku create ai-tutor-app

# Add MongoDB addon
heroku addons:create mongolab

# Add Redis addon
heroku addons:create heroku-redis

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set GEMINI_API_KEY=your-api-key

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

### DigitalOcean Deployment

1. Create Droplet (Ubuntu 22.04)
2. Install Docker and Docker Compose
3. Clone repository
4. Configure .env
5. Run `docker-compose up -d`

## Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/staticfiles;
    }

    location /media {
        alias /path/to/media;
    }
}
```

## SSL/HTTPS Setup

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

## Scaling

### Horizontal Scaling

- Use load balancer (nginx, AWS ELB)
- Multiple backend instances
- Shared Redis and MongoDB
- Shared media storage (S3)

### Vertical Scaling

- Increase server resources
- Optimize database queries
- Add database indexes
- Use caching aggressively

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check MongoDB is running
   - Verify connection string
   - Check firewall rules

2. **Static Files Not Loading**
   - Run `collectstatic`
   - Check nginx configuration
   - Verify file permissions

3. **Celery Tasks Not Running**
   - Check Redis connection
   - Verify Celery worker is running
   - Check task logs

4. **API Errors**
   - Check Django logs
   - Verify environment variables
   - Check database migrations

## Maintenance

### Regular Tasks

- Monitor error logs
- Check disk space
- Review performance metrics
- Update dependencies
- Backup databases
- Test disaster recovery

### Updates

```bash
# Pull latest code
git pull origin main

# Update dependencies
pip install -r requirements.txt
cd frontend && npm install

# Run migrations
python manage.py migrate

# Restart services
docker-compose restart
```

## Support

For issues and questions:
- GitHub Issues: <repository-url>/issues
- Email: support@aitutor.com
- Documentation: <docs-url>
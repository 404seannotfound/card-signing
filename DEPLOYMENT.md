# Deployment Guide for Render.com

## Prerequisites
- GitHub account with this repository
- Render.com account (free tier available)

## Step-by-Step Deployment

### 1. Prepare Your Repository
```bash
git add .
git commit -m "Initial commit - Ranger Signature Manager"
git push origin main
```

### 2. Create PostgreSQL Database on Render.com

1. Log in to [Render.com](https://render.com)
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name**: `ranger-signatures-db` (or your choice)
   - **Database**: `ranger_signatures`
   - **User**: (auto-generated)
   - **Region**: Choose closest to your users
   - **Plan**: Free (or paid for production)
4. Click "Create Database"
5. **Save the Internal Database URL** - you'll need this

### 3. Create Web Service on Render.com

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `ranger-signature-manager` (or your choice)
   - **Region**: Same as database
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free (or paid for production)

### 4. Set Environment Variables

In the Web Service settings, add these environment variables:

1. **SECRET_KEY**
   - Generate a secure random string (32+ characters)
   - Example: Use Python to generate one:
     ```python
     import secrets
     print(secrets.token_hex(32))
     ```

2. **DATABASE_URL**
   - Copy the "Internal Database URL" from your PostgreSQL database
   - Should look like: `postgresql://user:password@host/database`
   - Render automatically converts `postgres://` to `postgresql://`

### 5. Deploy

1. Click "Create Web Service"
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Start the application
   - Create database tables on first run

### 6. Access Your Application

- Your app will be available at: `https://your-service-name.onrender.com`
- First deployment takes 2-5 minutes
- Subsequent deployments are automatic on git push

## Post-Deployment

### Test the Application
1. Visit your app URL
2. Click "Ranger Login"
3. Enter a test Ranger ID (e.g., "RANGER001")
4. Upload a test signature image
5. Check "View All Signatures" page
6. Test PDF generation

### Monitor Your Application
- View logs in Render dashboard
- Check database connections
- Monitor resource usage

## Troubleshooting

### Database Connection Issues
- Verify DATABASE_URL is set correctly
- Check database is in same region as web service
- Ensure database is running (not suspended)

### Application Won't Start
- Check logs in Render dashboard
- Verify all dependencies in requirements.txt
- Ensure Procfile is correct: `web: gunicorn app:app`

### Images Not Uploading
- Check file size limits (5MB default)
- Verify image format is supported
- Check application logs for errors

### PDF Generation Fails
- Ensure reportlab and Pillow are installed
- Check that signatures exist in database
- Verify at least one signature is selected

## Scaling Considerations

### Free Tier Limitations
- Web service spins down after 15 minutes of inactivity
- Database limited to 1GB storage
- 750 hours/month of runtime

### Upgrading for Production
- **Paid Web Service**: Always-on, more resources
- **Paid Database**: More storage, better performance
- **Custom Domain**: Add your own domain name
- **SSL Certificate**: Automatic with custom domain

## Backup and Maintenance

### Database Backups
- Render automatically backs up paid databases
- For free tier, manually export data periodically
- Use PostgreSQL dump tools for backups

### Updates and Maintenance
- Push updates to GitHub main branch
- Render automatically redeploys
- Test in development before pushing to production

## Security Best Practices

1. **Never commit .env file** - use environment variables
2. **Use strong SECRET_KEY** - 32+ random characters
3. **Keep dependencies updated** - regularly update requirements.txt
4. **Monitor access logs** - check for suspicious activity
5. **Implement rate limiting** - for production use
6. **Add admin authentication** - protect report page in production

## Support

- Render Documentation: https://render.com/docs
- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/

## Cost Estimate

### Free Tier (Development/Testing)
- Web Service: Free (with limitations)
- PostgreSQL: Free (1GB limit)
- Total: $0/month

### Production Tier (Recommended)
- Web Service: $7/month (Starter)
- PostgreSQL: $7/month (Starter)
- Total: $14/month

### High-Traffic Production
- Web Service: $25+/month (Standard+)
- PostgreSQL: $25+/month (Standard+)
- Total: $50+/month

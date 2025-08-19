# Deployment Configuration

## Files in this directory

- **Procfile**: Heroku deployment configuration
- **fly.toml**: Fly.io deployment configuration
- **runtime.txt**: Python runtime version specification

## Deployment Options

### Fly.io
Use `fly.toml` configuration:
```bash
fly deploy
```

### Heroku
Use `Procfile` and `runtime.txt`:
```bash
git push heroku main
```

## Configuration Notes
- Port 8080 is configured for both platforms
- Health check endpoint: `/info`
- Data persistence configured via Fly.io volumes
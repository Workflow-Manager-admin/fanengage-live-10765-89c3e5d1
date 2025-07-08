# Dockerfile for football_engagement_database
FROM postgres:15-alpine

# Set environment variables for default DB config (production overrides with .env)
ENV POSTGRES_DB=fanengage
ENV POSTGRES_USER=fanengage
ENV POSTGRES_PASSWORD=fanengagepwd

# Copy init SQL scripts
COPY initdb/ /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432

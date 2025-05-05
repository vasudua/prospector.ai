FROM postgres:latest

# Environment variables for PostgreSQL
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=postgres
ENV PGDATA=/var/lib/postgresql/data/pgdata

# Create directory for persistent data
RUN mkdir -p $PGDATA && chown -R postgres:postgres $PGDATA

# Expose PostgreSQL port
EXPOSE 5432

# Health check to verify the database is ready
HEALTHCHECK --interval=5s --timeout=5s --retries=5 \
  CMD pg_isready -U $POSTGRES_USER -d $POSTGRES_DB || exit 1

# Set the volumes
VOLUME ["$PGDATA"]

# The default command starts the PostgreSQL server
CMD ["postgres"] 
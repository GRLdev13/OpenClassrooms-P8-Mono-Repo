FROM postgres:13

# PostgreSQL executes these scripts alphabetically when it initializes an
# empty data directory for the first time.
COPY *.sql /docker-entrypoint-initdb.d/

# The dump was created from a database owned by "postgres". Objects should
# instead remain owned by the POSTGRES_USER supplied through Compose.
RUN sed -i '/OWNER TO postgres;/d' /docker-entrypoint-initdb.d/*.sql

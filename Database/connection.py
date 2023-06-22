import psycopg2
from psycopg2 import pool
import os
import dotenv
dotenv.load_dotenv(dotenv.find_dotenv())


postgreSQL_pool_geral = psycopg2.pool.SimpleConnectionPool(1, 10, user=os.getenv('login_db'),password=os.getenv('senha_db'),host=os.getenv('host_db'),port=os.getenv('port_db'),database=os.getenv('database_db'))



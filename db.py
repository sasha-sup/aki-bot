import config
import asyncpg
import logging

async def create_db_connection():
    db_config = {
        "host": config.DB_HOST,
        "port": config.DB_PORT,
        "database": config.DB_NAME,
        "user": config.DB_USER,
        "password": config.DB_PASS,
    }
    try:
        # Connect db
        connection = await asyncpg.connect(**db_config)
        logging.info("Connected to DB")
        return connection
    except asyncpg.PostgresError as e:
        logging.error(f"Error connecting to DB: {e}")
        raise e

async def close_db_connection(connection):
    await connection.close()

async def create_tables_if_exists():
    connection = await create_db_connection()
    try:
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                user_id BIGINT UNIQUE NOT NULL,
                send_notifications BOOLEAN DEFAULT TRUE);
            """)
    except Exception as e:
        logging.error(f"Error creating table: {e}")
    finally:
        await close_db_connection(connection)

import asyncpg

import config
from config import logger


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
        return connection
    except asyncpg.PostgresError as e:
        logger.error(f"Error connecting to DB: {e}")
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
                send_notifications BOOLEAN DEFAULT TRUE,
                pet_clicks INT DEFAULT 0,
                total_pet_clicks INT DEFAULT 0,
                last_pet_time timestamp);
            """)
    except asyncpg.PostgresError as e:
        logger.error(f"Error creating table: {e}")
    finally:
        await connection.close()

async def ensure_user_exists(user_id):
    connection = await create_db_connection()
    try:
        select_query = "SELECT * FROM users WHERE user_id = $1"
        user = await connection.fetchrow(select_query, user_id)
        if user is None:
            insert_query = "INSERT INTO users (user_id, send_notifications) VALUES ($1, TRUE) ON CONFLICT (user_id) DO NOTHING"
            await connection.execute(insert_query, user_id)
            logger.info(f"Added new user with user_id {user_id}")
    except asyncpg.UniqueViolationError:
        logger.warning(f"User with user_id {user_id} already exists.")
    except asyncpg.PostgresError as e:
        logger.error(f"Error adding user: {e}")
    finally:
        await connection.close()

async def get_user(user_id):
    try:
        connection = await create_db_connection()
        query = "SELECT * FROM users WHERE user_id = $1"
        result = await connection.fetchrow(query, user_id)
        return result
    except asyncpg.PostgresError as e:
        logger.error(f"Error get user: {e}")
    finally:
        await connection.close()

async def get_all_user_ids():
    try:
        connection = await create_db_connection()
        query = "SELECT user_id FROM users WHERE send_notifications = TRUE"
        result = await connection.fetch(query)
        user_ids = [record['user_id'] for record in result]
        return user_ids
    except asyncpg.PostgresError as e:
        logger.error(f"Error get all user: {e}")
    finally:
        await connection.close()

async def update_notification_settings(user_id, send_notifications):
    connection = await create_db_connection()
    try:
        query = "UPDATE users SET send_notifications = $2 WHERE user_id = $1"
        await connection.execute(query, user_id, send_notifications)
    except asyncpg.PostgresError as e:
        logger.error(f"Error updating notification settings: {e}")
    finally:
        await connection.close()

async def increment_click_count(user_id):
    connection = await create_db_connection()
    try:
        update_query = "UPDATE users SET total_pet_clicks = total_pet_clicks + 1 WHERE user_id = $1"
        await connection.execute(update_query, user_id)
    except asyncpg.PostgresError as e:
        logger.error(f"Error incrementing click count: {e}")
    finally:
        await connection.close()

async def set_last_pet_time(user_id, current_time):
    connection = await create_db_connection()
    try:
        update_query = "UPDATE users SET last_pet_time = $2 WHERE user_id = $1"
        await connection.execute(update_query, user_id, current_time)
    except asyncpg.PostgresError as e:
        logger.error(f"Error setting last pet time: {e}")
    finally:
        await connection.close()

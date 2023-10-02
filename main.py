import os
import db
import random
import config
import asyncio
import logging
from bot import dp
from aiogram import executor

# Logger
log_dir = os.path.join(os.path.dirname(__file__), 'log')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO,
    filename = os.path.join(config.BASE_DIR, "log", "main.log"))
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# LoggingMiddleware
logging_middleware = LoggingMiddleware(
    logger_name='aiogram',
    log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    log_level=logging.INFO)

# Create required directories
async def create_content_dirs():
    try:
        for dir_path in [config.PIC_PATH, config.VIDEO_PATH]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                logging.info(f"Created directory: {dir_path}")
            else:
                logging.info(f"Directory already exists: {dir_path}")
    except Exception as e:
        logging.error(f"Error creating directories: {e}")
        raise e




async def main():
    await create_content_dirs()
    await db.create_tables_if_exists()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


























# Get random content
def get_random_content():
    try:
        picture = [f for f in os.listdir(PIC_PATH) if os.path.isfile(os.path.join(PIC_PATH, f))]
        video = [f for f in os.listdir(VIDEO_PATH) if os.path.isfile(os.path.join(VIDEO_PATH, f))]
        random_number = random.randint(1, 100)
        if random_number == 1:
            send_choice = 'video'
            random_file = random.choice(video)
        else:
            send_choice = 'picture'
            random_file = random.choice(picture)
        random_path = os.path.join(VIDEO_PATH if send_choice == 'video' else PIC_PATH, random_file)
        return send_choice, random_path
    except Exception as e:
        logger.error(f"Error in get_random_content: {str(e)}")

# DB connection
# def connect_to_db():
#     conn = asyncpg.connect(
#         host=os.getenv('DB_HOST'),
#         database=os.getenv('DB_NAME'),
#         user=os.getenv('DB_USER'),
#         password=os.getenv('DB_PASS')
#     )
#     return conn

async def connect_to_db():
    conn = asyncpg.connect(
        host    =DB_HOST,
        database=DB_NAME,
        user    =DB_USER,
        password=DB_PASS
    )
    return conn

# Check or create db table
def create_users_table(conn):
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            user_id BIGINT UNIQUE NOT NULL,
            send_notifications BOOLEAN DEFAULT TRUE
        );
        """
        conn.execute(create_table_query)
        logger.info("Created 'users' table in the database.")
    except Exception as e:
        logger.error(f"Error creating 'users' table: {str(e)}")

# DB connection check and init
def initialize_db():
    try:
        conn = connect_to_db()
        if not conn:
            logger.error("Failed to connect to the database.")
            return
        else:
            create_users_table(conn)
            conn.close()
    except Exception as e:
        logger.error(f"Error in initialize_db: {str(e)}")

async def start(update: Update, context):
    try:
        user = update.effective_user
        user_id = user.id
        conn = connect_to_db()
        logging.info(f"User ID: {user_id} started bot at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        try:
            insert_user_query = """
            INSERT INTO users (user_id) VALUES ($1)
            ON CONFLICT (user_id) DO NOTHING;
            """
            await conn.execute(insert_user_query, user_id)
            chat_id = update.message.chat_id
            await update.message.reply_text(
                text=WELCOME_MESSAGE,
                parse_mode=constants.ParseMode.MARKDOWN_V2,
                disable_web_page_preview=True,
                reply_markup=ReplyKeyboardMarkup([
                    [KeyboardButton("🐕 Pet me")]
                ])
            )
            await send_random_content(update, context, user_id)
        finally:
            conn.close()
    except Exception as e:
        logger.error(f"Error in start: {str(e)}")

async def stop(update: Update):
    try:
        user = update.effective_user
        user_id = user.id
        conn = await connect_to_db()
        logging.info(f"User ID: {user_id} stopped bot at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        try:
            update_notifications_query = """
            UPDATE users SET send_notifications = FALSE WHERE user_id = $1;
            """
            conn.execute(update_notifications_query, user_id)
            update.message.reply_text("You have successfully stopped receiving notifications.")
        finally:
            conn.close()
    except Exception as e:
        logger.error(f"Error in stop: {str(e)}")

async def handle_keyboard_buttons(update, context):
    try:
        user = update.effective_user
        user_id = user.id
        chat_id = update.message.chat_id
        await send_random_content(update, context, user_id)
        logger.info(f"User ID: {user_id} requested content at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        logger.error(f"Error in handle_keyboard_buttons: {str(e)}")

async def send_messages_to_all_users(bot, conn):
    try:
        users = await get_all_users(conn)
        for user in users:
            user_id = user['user_id']
            wait_time = random.randint(MIN_TIME, MAX_TIME)
            scheduled_time = datetime.now() + timedelta(seconds=wait_time)
            logger.info(f"Starting message scheduling for user {user_id} at {scheduled_time}")
            await asyncio.sleep(wait_time)
            await send_random_content(update, context, user_id)
            logger.info(f"Finished message scheduling for user {user_id} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        logger.error(f"Error in send_messages_to_all_users: {str(e)}")

async def send_random_content(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id):
    try:
        send_choice, content_path = get_random_content()
        chat_id = user_id
        if send_choice == 'video':
            await context.bot.send_video(chat_id=chat_id, video=open(content_path, 'rb'))
        else:
            await context.bot.send_photo(chat_id=chat_id, photo=open(content_path, 'rb'))
    except Exception as e:
        logger.error(f"Error in send_random_content: {str(e)}")

async def main():
    try:
        check_directories_exist()
        initialize_db()
        logger.info("Starting the application...")
        bot = Application.builder().token(TOKEN).build()

        bot.add_handler(CommandHandler(["start", "help"], start))
        bot.add_handler(CommandHandler("stop", stop))
        bot.add_handler(MessageHandler(filters.Text("🐕 Pet me"), handle_keyboard_buttons))
        bot.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())

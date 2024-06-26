import discord
import json
from discord.ext import commands, tasks
from src.constants.config import Config
from src.logging.logger import LOGGER
from src.utils.init_operations import get_extensions, get_routines

CONFIG = Config.get_instance()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.AutoShardedBot(command_prefix=CONFIG.PREFIX, intents=intents, enable_debug_events=True)

LOGGER.info("Bot initialized")

@bot.event
async def on_ready():
    # Load extensions
    extensions = get_extensions()
    for extension in extensions:
        await bot.load_extension(extension)
    LOGGER.info("Extensions initialized")

    interval_and_routines = get_routines(bot=bot)
    for interval, routine in interval_and_routines:
        loop = tasks.loop(seconds=interval)(routine)
        loop.start()
    LOGGER.info("Routines initialized")

    # Set activity
    await bot.change_presence(activity=discord.Game(name="Chess 2"))

    LOGGER.info("Bot ready")

# Connection events
@bot.event
async def on_connect():
    LOGGER.info("Bot connected")

@bot.event
async def on_disconnect():
    LOGGER.warn("Bot disconnected")

@bot.event
async def on_resumed():
    LOGGER.info("Bot reconnected")

@bot.event
async def on_socket_raw_receive(msg):
    try:
        data = json.loads(msg)
    except Exception:
        return
    if not isinstance(data, dict):
        return
    opcode = data.get('op', None)
    match opcode:
        case 7:
            LOGGER.info('Received opcode 7: Reconnect requested by Discord')
        case 9:
            LOGGER.error('Received opcode 9: Session has been invalidated')

bot.run(CONFIG.BOT_TOKEN)

from discord.ext import commands
import discord
import os

intents = discord.Intents.default()
intents.members = True # メンバー管理の権限
intents.message_content = True # メッセージの内容を取得する権限


# Botをインスタンス化
bot = commands.Bot(
    command_prefix="$", # $コマンド名　でコマンドを実行できるようになる
    case_insensitive=True, # コマンドの大文字小文字を区別しない ($hello も $Hello も同じ!)
    intents=intents # 権限を設定
)

@bot.event
async def on_ready():
    """Botが起動したときに呼び出されるイベント"""
    print(f"Bot is ready. Logged in as {bot.user}")

@bot.event
async def on_message(message: discord.Message):
    """メッセージをおうむ返しにする処理"""
    if message.author.bot: # ボットのメッセージは無視
        return
    
    # メッセージが /pin で始まるリプライの場合、そのメッセージをピン留め/ピン留め解除する
    if message.content.startswith("/pin") and message.type == discord.MessageType.reply:
        reply = message.reference.resolved
        if reply.pinned:
            await reply.unpin()
            await message.reply("ピン留めを解除しました")
        else:
            await reply.pin()
        await bot.process_commands(message)  # コマンド処理を続行するための呼び出し

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
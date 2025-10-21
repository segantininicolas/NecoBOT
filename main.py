import disnake
from entidades.necoBOT import necoBOT
from cogs.comandos import Comandos
from cogs.adm import Adm
from cogs.perfil import Perfil
from dotenv import load_dotenv
import os
from save_and_load import *

load_dotenv()

MEU_TOKEN = os.getenv('DISCORD_TOKEN')

intents = disnake.Intents.all()
bot = necoBOT(intents=intents)

@bot.event
async def on_ready():
    print(f"Bot {bot.user} está online!")
            
@bot.before_slash_command_invoke
async def before_slash_command_invoke(inter : disnake.ApplicationCommandInteraction):
    bot.usuario_servico.registrar(inter.user)


bot.add_cog(Comandos(bot))
bot.add_cog(Adm(bot))
bot.add_cog(Perfil(bot))


bot.run(MEU_TOKEN)




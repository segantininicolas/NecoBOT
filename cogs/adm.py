import json
import disnake
from disnake.ext import commands
import requests
from entidades.necoBOTType import necoBOTType
import json

# Comandos de Admin do bot.

class Adm(commands.Cog):
    def __init__(self, bot : necoBOTType):
        self.bot = bot
        self.usuario_servico = bot.usuario_servico



    @commands.slash_command(name="msg", description="Comando para fazer a NecoBOT falar.")
    async def msg(self, inter : disnake.ApplicationCommandInteraction, mensagem : str, contem_variavel : bool = False):
        if inter.author.id not in [self.bot.owner_id, inter.guild.owner.id]:
            await inter.response.send_message("Você não tem permissão para usar esse comando.")
            return
        
        if contem_variavel:
            mensagem = eval(f"f'{mensagem}'")
            
        await inter.channel.send(mensagem)
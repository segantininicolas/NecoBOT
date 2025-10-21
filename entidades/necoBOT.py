import codecs
from datetime import datetime, timezone
from random import randint
import re
import disnake
from disnake.ext import commands, tasks
from entidades.necoBOTType import necoBOTType
from save_and_load import carregar
from servicos.UsuarioServico import UsuarioServico

class necoBOT(necoBOTType):
    def __init__(self, intents : disnake.Intents):
        super().__init__(intents=intents)
        self.usuario_servico = UsuarioServico(self)
        self.configs = carregar("configs")

    async def on_slash_command_error(self, interaction : disnake.ApplicationCommandInteraction, 
                                    exception : commands.CommandError):
        try:
            await interaction.response.defer()
        except:
            pass
        
        await self.owner.send(f"## Ocorreu um erro: " +
                                f"\n- Servidor: **{interaction.guild.name}**" +
                                f"\n- Canal: **{interaction.channel.name}** às **{datetime.now().strftime('%H:%M:%S, %Y/%m/%d')}**" + 
                                f"\n- Usuário: **{interaction.user.name}**" + 
                                f"\n- Comando: **{interaction.application_command.name}**" +
                                f"\n- Exceção: \n```{exception}```")
        
        await interaction.edit_original_message("Ocorreu um erro :(")


    async def on_member_join(self, usuario: disnake.User):
        self.usuario_servico.registrar(usuario)



        
        

        
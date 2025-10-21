from enum import Enum
import disnake
from disnake.ext import commands
from re import match
from entidades.necoBOTType import necoBOTType

# Variavel para verificar se um link é válido.

def validar_link(link : str) -> bool:
    regex = r'[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
    return match(regex, link) is not None

# Classe perfil

class Perfil(commands.Cog):
    def __init__(self, bot : necoBOTType):
        self.bot = bot
        self.usuario_servico = bot.usuario_servico


    # Comando para adicionar o nome no perfil.
    
    @commands.slash_command(name="nome", description="Registra seu nome")
    async def nome(self, inter : disnake.ApplicationCommandInteraction, nome : str):
        await inter.response.defer()
        
        usuario = self.usuario_servico.pegar_usuario(inter.user)
        usuario.nome = nome.strip().capitalize()
        self.usuario_servico.salvar_usuario(usuario)
        
        await inter.edit_original_message("Nome adicionado com sucesso!")

    # Comando para mostrar o perfil.

    @commands.slash_command(name="perfil", description="Mostra seu perfil")
    async def perfil(self, inter : disnake.ApplicationCommandInteraction, usuario : disnake.User = None):
        await inter.response.defer()

        usuario = self.usuario_servico.pegar_usuario_valido(inter.user, usuario)

        embed_perfil = disnake.Embed(
            title = f"Perfil de {usuario.name}",
            colour=disnake.Colour.blue()
        )
        embed_perfil.set_thumbnail(usuario.avatar)
        embed_perfil.add_field(
            name="Nick",
            value=usuario.global_name
        )
        
        for key, value in self.usuario_servico.usuario_info_para_dict(usuario).items():
            if value != None and key not in ["xp"]:
                if key == "twitch":
                    value = f"https://www.twitch.tv/{value}"

                embed_perfil.add_field(
                    name= key.replace("_", " ").title(),
                    value= f"[Clique aqui]({value})" if validar_link(str(value)) else str(value),
                )

        await inter.edit_original_message(embed=embed_perfil)
        
    @commands.slash_command(name="anv", description="Registra a data do seu aniversário no perfil")
    async def anv(self, inter : disnake.ApplicationCommandInteraction, dia : int, mes : int):
        await inter.response.defer()

        if mes < 0 > dia or mes > 12 or dia > 31:
            await inter.edit_original_message("Insira uma data válida")
            return
        
        usuario = self.usuario_servico.pegar_usuario(inter.user)
        usuario.aniversario = f"{dia:02}/{mes:02}"
        self.usuario_servico.salvar_usuario(usuario)

        await inter.edit_original_message("Aniversário registrado com sucesso!")

    # Comando para adicionar o estado no perfil.

    @commands.slash_command(name="estado", description="Registra seu Estado no perfil.")
    async def estado(self, inter : disnake.ApplicationCommandInteraction, estado : str):
        await inter.response.defer()
        
        usuario = self.usuario_servico.pegar_usuario(inter.user)
        usuario.estado = estado.strip()
        self.usuario_servico.salvar_usuario(usuario)
        
        await inter.edit_original_message("Estado registrado com sucesso!")

    @commands.slash_command(name="twitter", description="Registra sua twitter no perfil.")
    async def nome(self, inter : disnake.ApplicationCommandInteraction, 
                   twitter : str, tipo = commands.Param(choices=["Link", "Usuário"])):
        await inter.response.defer()
        
        twitter = twitter.strip()
        
        if tipo == "Link" and not validar_link(twitter):
            await inter.edit_original_message("Coloque um link válido.")
            return

        usuario = self.usuario_servico.pegar_usuario(inter.user)
        usuario.twitter = twitter.strip()
        self.usuario_servico.salvar_usuario(usuario)

        await inter.edit_original_message("Twitter registrado com sucesso!")

    # Comando para adicionar a Steam no perfil.

    @commands.slash_command(name="steam", description="Registra sua conta da Steam no perfil.")
    async def steam(self, inter : disnake.ApplicationCommandInteraction, 
                    steam : str, tipo = commands.Param(choices=["Link", "Usuário"])):
        await inter.response.defer()
        
        steam = steam.strip()

        if tipo == "Link" and not validar_link(steam):
            await inter.edit_original_message("Coloque um link válido.")
            return

        usuario = self.usuario_servico.pegar_usuario(inter.user)
        usuario.steam = steam
        self.usuario_servico.salvar_usuario(usuario)

        await inter.edit_original_message("Steam registrada com sucesso!")

    # Comando para adicionar o Instagram no perfil.

    @commands.slash_command(name="insta", description="Registra sua conta do Instagram no perfil.")
    async def insta(self, inter : disnake.ApplicationCommandInteraction, 
                    instagram : str, tipo = commands.Param(choices=["Link", "Usuário"])):
        await inter.response.defer()
        
        instagram = instagram.strip()

        if tipo == "Link" and not validar_link(instagram):
            await inter.edit_original_message("Coloque um link válido.")
            return

        usuario = self.usuario_servico.pegar_usuario(inter.user)
        usuario.instagram = instagram
        self.usuario_servico.salvar_usuario(usuario)

        await inter.edit_original_message("Instagram registrado com sucesso!")

    # Comando para adicionar a conta do Osu no Perfil.

    @commands.slash_command(name="osu", description="Registra sua conta do Osu! no perfil")
    async def osu(self, inter : disnake.ApplicationCommandInteraction, 
                  osu : str, tipo = commands.Param(choices=["Link", "Usuário"])):
        await inter.response.defer()

        osu = osu.strip()
        if tipo == "Link" and not validar_link(osu):
            await inter.edit_original_message("Coloque um link válido.")
            return

        usuario = self.usuario_servico.pegar_usuario(inter.user)
        usuario.osu = osu
        self.usuario_servico.salvar_usuario(usuario)

        await inter.edit_original_message("Osu! registrado com sucesso!")

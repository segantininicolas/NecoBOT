import asyncio
from random import randint
from card.gerador_card import criar_imagem_base
import io
import re
import os
import disnake
from disnake.ext import commands
import requests
from cogs.dicionario import SAUDACOES
from cogs.dicionario import CORES_COMUNS
from entidades.necoBOTType import necoBOTType
from save_and_load import carregar
import hashlib
from cogs.osu_api import profile


def string_to_hex(s):
    hashed = hashlib.md5(s.encode()).hexdigest().upper()
    return hashed[:6]

class Comandos(commands.Cog):
    def __init__(self, bot : necoBOTType):
        self.bot = bot
        self.usuario_servico = bot.usuario_servico
        
    async def remove_colors(self, member):
        removed = 0
        for role in member.roles:
            if role.name.startswith("#") and re.match(r"^#[0-9A-F]{6}$", role.name.upper()):
                await member.remove_roles(role)
                removed += 1
        return removed
    
    # Comando para roletar um número aleatório.
        
    @commands.slash_command(name="roll", description="Roleta um número aleatório",)
    async def roll(self, inter : disnake.ApplicationCommandInteraction, max : int = 100):
        await inter.response.send_message(f"{inter.user.display_name} roletou o número {randint(0, max)}")

    # Comando que lista todos os comandos do bot.

    @commands.slash_command(name="help", description="Lista de comandos")
    async def help(self, inter : disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        
        embed = disnake.Embed(
            title="Lista de comandos",
            colour=disnake.Colour.blue()
        )
        
        comandos = list(self.bot.slash_commands)
        comandos.sort(key=lambda x: x.name)
        for comando in comandos:
            embed.add_field(
                name=f"/{comando.name}",
                value=comando.description,
                inline=False
            )
        
        await inter.edit_original_message(embed=embed)

    # Comando para abrir a lista de aniversariantes.

    @commands.slash_command(name="ans", description="Mostra a lista de aniversariantes, podendo escolher o mês")
    async def ans(self, inter : disnake.ApplicationCommandInteraction, mes : int = None):
        await inter.response.defer()

        usuarios = sorted(
            filter(
                lambda usuario: usuario.aniversario != None,
                self.usuario_servico.pegar_todos_usuarios()
                ),
            key=lambda usuario: (usuario.aniversario[3:], usuario.aniversario[:2])
            )
        
        embed = disnake.Embed(
            title="Aniversariantes", 
            description="",
            colour=disnake.Color.blue(),
            )
        
        if mes != None:
            if 0 > mes or mes > 12:
                await inter.edit_original_message(f"{mes} não é um mês válido.")
                return
            
            meses = [
                "Janeiro", "Fevereiro", "Março", "Abril", 
                "Maio", "Junho", "Julho", "Agosto", 
                "Setembro", "Outubro", "Novembro", "Dezembro"]
            
            embed.title += f" do mês {meses[mes - 1]}"
        
        for usuario in usuarios:
            embed.description += f"\n<@{usuario.id}>: {usuario.aniversario}"

        await inter.edit_original_message(embed=embed)

    async def sleep_check_and_delete_role(self, role):
        await asyncio.sleep(10)
        return await self.check_and_delete_role(role)

    async def check_and_delete_role(self, role):
        if len(role.members) == 0:
            await role.delete()
            return True
        return False

    async def remove_colors(self, author):
        color_roles = []
        re_color = re.compile(r'^\#[0-9A-F]{6}$')
        for role in author.roles:
            if re_color.match(role.name.upper()):
                color_roles.append(role)

        for role in color_roles:
            await author.remove_roles(role)
            asyncio.create_task(self.sleep_check_and_delete_role(role))

        return len(color_roles)

    # Comando para alterar a cor do nome.

    @commands.slash_command(name="cor", description="Muda a cor do seu nick no servidor")
    async def cor(self, inter: disnake.ApplicationCommandInteraction, cor: str):
        await inter.response.defer()

        author = inter.author
        guild = inter.guild
        cor = cor.strip().upper()

        if cor in CORES_COMUNS:
            cor = CORES_COMUNS[cor]

        if cor == "REMOVER":
            removed = await self.remove_colors(author)
            if removed > 0:
                await inter.send("Cor removida!")
            else:
                await inter.send("Nenhuma cor para remover.")
            return


        if re.fullmatch(r"[0-9A-F]{6}", cor):
            cor = "#" + cor
        elif not re.fullmatch(r"#[0-9A-F]{6}", cor):
            cor = "#" + string_to_hex(cor)

        await self.remove_colors(author)

        assigned_role = None
        for role in guild.roles:
            if role.name.upper() == cor:
                assigned_role = role
                break

        if assigned_role is None:
            red = int(cor[1:3], 16)
            green = int(cor[3:5], 16)
            blue = int(cor[5:7], 16)

            assigned_role = await guild.create_role(
                name=cor,
                colour=disnake.Color.from_rgb(red, green, blue)
            )

        await author.add_roles(assigned_role)
        await inter.edit_original_message(f"Cor `{cor}` aplicada com sucesso!")

    # Comando para mostrar a imagem de perfil de um usuário

    @commands.slash_command(name="avatar", description="Mostra a imagem de perfil do usuário.")
    async def avatar(self, inter : disnake.ApplicationCommandInteraction, usuario : disnake.User = None):
        await inter.response.defer()

        if usuario == None:
            usuario = inter.author

        embed = disnake.Embed(
            colour=disnake.Colour.blue(),
            title="Imagem de perfil de " + usuario.name
        )
        embed.set_image(url=usuario.display_avatar)

        await inter.edit_original_message(embed=embed)

    @commands.slash_command(name="profile", description="Gera uma imagem com as informações do perfil do usuário")
    async def profile(self, inter : disnake.ApplicationCommandInteraction, usuario : str):
        await inter.response.defer()

        arquivo_osu = await profile(usuario)

        if arquivo_osu is None:
            await inter.followup.send("Nome de usuário inválido ou erro ao buscar os dados.")
            return # <-- sasa beta tester

        else:
            os.remove("./card/data.json"),
            os.rename(os.path.basename(arquivo_osu), os.path.join("./card", arquivo_osu))

        gerar_imagem = criar_imagem_base()
        
        if gerar_imagem is None:
            await inter.followup.send("Erro ao gerar imagem.")
            return
        
        with io.BytesIO() as image_binary:
            gerar_imagem.save(image_binary, 'PNG')
            image_binary.seek(0)
        
            imagem_gerada = disnake.File(fp=image_binary, filename='card_gerado.png')
            await inter.followup.send("Aqui está o card!", file=imagem_gerada)

        # Sistema de troca automático de links para que o embed funcione corretamente no Discord.

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        matches_twitter = re.match(r"(https://twitter.com/.*?/status/\w*)", message.content)
        matches_x = re.match(r"(https://x.com/.*?/status/\w*)", message.content)
        matches_tiktok = re.match(r"(https://www.tiktok.com/@.*?/video/\d+)", message.content)
        matches_tiktok2 = re.match(r"(https://vm\.tiktok\.com/[\w/]+)", message.content)
       # matches_instagram1 = re.match(r"https?:\/\/(\w+\.)?instagram\.com\/[^\s]+", message.content)
       # matches_instagram2 = re.match(r"(\w+\.)?(instagram\.com\/)", message.content)

        if matches_twitter:
            await message.channel.send(f'<@{message.author.id}>:\n{matches_twitter.groups()[0].replace("twitter", "vxtwitter")}')
            await message.delete()
        
        elif matches_x:
            await message.channel.send(f'<@{message.author.id}>:\n{matches_x.groups()[0].replace("x.com", "fixupx.com")}')
            await message.delete()

        elif matches_tiktok:
            await message.channel.send(f'<@{message.author.id}>:\n{matches_tiktok.groups()[0].replace("tiktok", "tnktok")}')
            await message.delete()

        elif matches_tiktok2:
            await message.channel.send(f'<@{message.author.id}>:\n{matches_tiktok2.groups()[0].replace("vm.tiktok", "vm.tnktok")}')
            await message.delete()

      #  elif matches_instagram1:
        #    await message.channel.send(f'<@{message.author.id}>:{matches_instagram1.group().replace("instagram.com", "vxinstagram.com")}')
        #    await message.delete()

      #  elif matches_instagram2:
        #    await message.channel.send(f'<@{message.author.id}>:{matches_instagram2.group().replace("instagram.com", "vxinstagram.com")}')
        #   await message.delete()
            
        if message.content.startswith('!'):
            await self.process_commands(message)
            return
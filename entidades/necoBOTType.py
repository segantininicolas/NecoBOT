from disnake.ext import commands
from servicos.UsuarioServico import UsuarioServico


class necoBOTType(commands.InteractionBot):
    usuario_servico : UsuarioServico
    configs : dict
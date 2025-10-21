from disnake import User
from disnake.ext import commands
from entidades.Usuario import Usuario
from repositorios.UsuarioRepositorio import UsuarioRepositorio


class UsuarioServico():
    def __init__(self, bot : commands.Bot) -> None:
        self.bot = bot
        self.usuario_repositorio = UsuarioRepositorio()
    
    def pegar_usuario(self, usuario : User) -> Usuario:
        usuario_info = self.usuario_repositorio.pegar_usuario(str(usuario.id))
        if usuario_info == None:
            self.registrar(usuario)
        
        usuario = Usuario(usuario)
        
        return self.disnake_user_para_usuario(
            usuario_info,
            usuario
            )
        
    def pegar_usuario_valido(self, usuario1 : User, usuario2 : User | None) -> Usuario:
        if usuario2 != None:
            usuario1 = usuario2
        
        return self.pegar_usuario(usuario1)
    
    def pegar_todos_usuarios(self) -> list[Usuario]:
        usuarios_dict = self.usuario_repositorio.pegar_todos_usuarios()
        usuarios = []
        
        for id, usuario_info in usuarios_dict.items():
            disnake_user = next((x for x in list(self.bot.get_all_members()) if str(x.id) == id), None)
            if disnake_user != None:
                usuarios.append(
                    self.disnake_user_para_usuario(usuario_info, disnake_user)
                    )
        
        return usuarios

    def salvar_todos_usuarios(self, usuarios : list[Usuario]):
        usuarios_dict = {}
        
        for usuario in usuarios:
            usuarios_dict[str(usuario.id)] = self.usuario_info_para_dict(usuario)
        
        self.usuario_repositorio.salvar_todos(
            usuarios_dict
        )
        
    def salvar_usuario(self, usuario : Usuario) -> None:
        self.usuario_repositorio.salvar_usuario(
            str(usuario.id),
            self.usuario_info_para_dict(usuario)
            )

    def registrar(self, usuario : User) -> None:
        if self.usuario_repositorio.pegar_usuario(str(usuario.id)) != None:
            return
        
        usuario = Usuario(usuario)
        self.usuario_repositorio.salvar_usuario(
            str(usuario.id),
            self.usuario_info_para_dict(usuario)
        )
    
    def usuario_info_para_dict(self, usuario : Usuario) -> dict[str, str | int | None]:
        return {
            "nome": usuario.nome,
            "aniversario": usuario.aniversario,
            "estado": usuario.estado,
            "twitter": usuario.twitter,
            "twitch": usuario.twitch,
            "steam": usuario.steam,
            "instagram": usuario.instagram,
            "osu": usuario.osu,
        }
        
    def disnake_user_para_usuario(self, usuario_info : dict, disnake_user : User) -> Usuario:
        user = Usuario(disnake_user)
        
        user.nome = usuario_info["nome"]
        user.aniversario = usuario_info["aniversario"]
        user.estado = usuario_info["estado"]
        user.twitter = usuario_info["twitter"]
        user.twitch = usuario_info["twitch"]
        user.steam = usuario_info["steam"]
        user.instagram = usuario_info["instagram"]
        user.osu = usuario_info["osu"]
        
        return user

    def apagar_usuario(self, id : int | str):
        self.usuario_repositorio.apagar_usuario(str(id))

from sqlalchemy.orm import Session
from models.usuarios_models import Usuarios


# Classe responsavel por gerenciar o CRUD de usuarios
class UsuariosService:
    # Função para iniciar a sessão:
    def __init__(self, session: Session):
        self.session = session

    # Função para buscar todos usuarios
    def get_usuarios(self):
        usuarios = self.session.query(Usuarios).all()
        usuarios_lista = []
        for usuario in usuarios:
            usuarios_lista.append(usuario.as_dict())
        return usuarios_lista

    # Funcao para buscar usuario pelo CPF
    def get_usuario_por_cpf(self, cpf):
        usuario = self.session.query(Usuarios).filter_by(cpf=cpf).first()
        usuario_json = usuario.as_dict()
        return usuario_json

    def post_usuarios(self, cpf: str, nome: str, telefone: str, endereco: str):
        novo_usuario = Usuarios(cpf=cpf, nome=nome, telefone=telefone, endereco=endereco)
        self.session.add(novo_usuario)
        self.session.commit()
        return novo_usuario.as_dict()

    def put_usuario(self, cpf, nome=None, telefone=None, endereco=None):
        usuario = self.session.query(Usuarios).filter_by(cpf=cpf).first()
        if not usuario:
            return f'Erro ao encontrar usuario'

        if nome:
            usuario.nome = nome
        if telefone:
            usuario.telefone = telefone
        if endereco:
            usuario.endereco = endereco

        try:
            self.session.commit()
            return usuario.as_dict()
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Erro ao atualizar usuario {str(e)}')

    def delete_usuario(self, cpf):
        usuario = self.session.query(Usuarios).filter_by(cpf=cpf).first()
        if not usuario:
            return f'Erro ao encontrar usuario'
        try:
            self.session.delete(usuario)
            self.session.commit()
            return f'Usuario {usuario.nome} deletado com sucesso'
        except Exception as e:
            return f'Erro {e} ao deletar usuario'


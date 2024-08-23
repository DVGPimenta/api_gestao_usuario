from flask import Blueprint, jsonify, request
from services.usuarios_services import UsuariosService
from sqlalchemy.orm import sessionmaker
from config.conexao import engine

# Criando Blueprint para rota 'usuarios'
usuarios_page = Blueprint('usuarios_page', __name__)
Session_local = sessionmaker(bind=engine)


# Criando Rotas para 'usuarios'

# Rota para mostrar todos usuarios
@usuarios_page.route('/usuarios', methods=['GET'])
def rota_get_usuarios():
    session = Session_local()
    try:
        usuarios_service = UsuariosService(session)
        usuarios = usuarios_service.get_usuarios()
        return jsonify(usuarios)
    except ValueError as e:
        return jsonify(f'Erro {e}')
    finally:
        session.close()


# Rota para mostrar um usuario atraves do CPF
@usuarios_page.route('/usuarios/<cpf>', methods=['GET'])
def rota_get_usuario_por_cpf(cpf):
    session = Session_local()
    try:
        usuario_service = UsuariosService(session)
        usuario = usuario_service.get_usuario_por_cpf(cpf)
        return jsonify(usuario)
    except Exception as e:
        return jsonify(f'Erro {e}')
    finally:
        session.close()


# Rota de cadastro de clientes
@usuarios_page.route('/usuarios/add', methods=['POST'])
def rota_post_usuarios():
    data = request.get_json()
    cpf = data.get('cpf')
    nome = data.get('nome')
    telefone = data.get('telefone')
    endereco = data.get('endereco')

    if not cpf or not nome or not telefone or not endereco:
        return jsonify(f'Dados insuficientes para o cadastro')

    session = Session_local()
    try:
        service_usuarios = UsuariosService(session)
        usuario = service_usuarios.post_usuarios(cpf, nome, telefone, endereco)
        return jsonify(usuario)
    except ValueError as e:
        return f'Erro {e} ao cadastrar usuario'
    finally:
        session.close()


@usuarios_page.route('/usuarios/edit/<cpf>', methods=['PUT'])
def rota_put_usuarios(cpf):
    data = request.get_json()
    nome = data.get('nome')
    telefone = data.get('telefone')
    endereco = data.get('endereco')

    if not any([nome, telefone, endereco]):
        return jsonify({'erro': 'Nenhum dado a ser atualizado'})

    session = Session_local()
    try:
        services_usuario = UsuariosService(session)
        usuario = services_usuario.put_usuario(
            cpf,
            nome=nome,
            telefone=telefone,
            endereco=endereco
        )
        return jsonify(usuario)
    finally:
        session.close()


@usuarios_page.route('/usuarios/delete/<cpf>', methods=['DELETE'])
def rota_deletar_usuario(cpf):
    session = Session_local()
    try:
        usuario_service = UsuariosService(session)
        usuario = usuario_service.delete_usuario(cpf)
        return jsonify(usuario)
    except Exception as e:
        return f'Erro {e} ao deletar usuario'

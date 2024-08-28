from sqlalchemy.exc import IntegrityError
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
        return jsonify(usuarios), 200
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    finally:
        session.close()


# Rota para mostrar um usuario atraves do CPF
@usuarios_page.route('/usuarios/<cpf>', methods=['GET'])
def rota_get_usuario_por_cpf(cpf):
    session = Session_local()
    try:
        usuario_service = UsuariosService(session)
        usuario = usuario_service.get_usuario_por_cpf(cpf)
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({'erro': 'Usuario não encontrado em nosso bando de dados'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        session.close()


# Rota de cadastro de usuarios
@usuarios_page.route('/usuarios/add', methods=['POST'])
def rota_post_usuarios():
    data = request.get_json()
    cpf = data.get('cpf')
    nome = data.get('nome')
    telefone = data.get('telefone')
    endereco = data.get('endereco')

    if not cpf or not nome or not telefone or not endereco:
        return jsonify({'erro': 'Dados insuficientes para o cadastro'}), 400

    session = Session_local()
    try:
        service_usuarios = UsuariosService(session)
        usuario = service_usuarios.post_usuarios(cpf, nome, telefone, endereco)
        return jsonify({'mensagem': f'Usuario {usuario.nome} cadastrado com susseco'})
    except ValueError as ve:
        return jsonify({'erro': str(ve)}), 400
    except IntegrityError:
        return jsonify({'erro': 'CPF ja existente no banco de dados'}), 409
    finally:
        session.close()


# Rota Edição De Usuarios
@usuarios_page.route('/usuarios/edit/<cpf>', methods=['PUT'])
def rota_put_usuarios(cpf):
    data = request.get_json()
    nome = data.get('nome')
    telefone = data.get('telefone')
    endereco = data.get('endereco')

    if not any([nome, telefone, endereco]):
        return jsonify({'erro': 'Nenhum dado a ser atualizado'}), 400

    session = Session_local()
    try:
        services_usuario = UsuariosService(session)
        usuario = services_usuario.put_usuario(
            cpf,
            nome=nome,
            telefone=telefone,
            endereco=endereco
        )
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({'erro': 'Usuario não encontrado'}), 404
    finally:
        session.close()


# Rota para deletar usuarios
@usuarios_page.route('/usuarios/delete/<cpf>', methods=['DELETE'])
def rota_deletar_usuario(cpf):
    session = Session_local()
    try:
        usuario_service = UsuariosService(session)
        usuario = usuario_service.delete_usuario(cpf)
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({'erro': 'Usuario não encontrado em nosso bando de dados'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        session.close()



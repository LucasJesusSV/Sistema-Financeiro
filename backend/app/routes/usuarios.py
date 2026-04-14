from flask import Blueprint, request, jsonify
from app import db
from app.models import Usuario

usuarios_bp = Blueprint("usuarios", __name__)


# CREATE - Cadastrar usuário
@usuarios_bp.route("/", methods=["POST"])
def criar_usuario():
    data = request.get_json()

    if not data or not data.get("nome") or not data.get("email"):
        return jsonify({"erro": "Nome e email são obrigatórios"}), 400

    if Usuario.query.filter_by(email=data["email"]).first():
        return jsonify({"erro": "Email já cadastrado"}), 409

    usuario = Usuario(nome=data["nome"], email=data["email"])
    db.session.add(usuario)
    db.session.commit()

    return jsonify(usuario.to_dict()), 201


# READ - Listar todos os usuários
@usuarios_bp.route("/", methods=["GET"])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([u.to_dict() for u in usuarios]), 200


# READ - Buscar usuário por ID
@usuarios_bp.route("/<int:id>", methods=["GET"])
def buscar_usuario(id):
    usuario = Usuario.query.get_or_404(id, description="Usuário não encontrado")
    return jsonify(usuario.to_dict()), 200


# UPDATE - Atualizar usuário
@usuarios_bp.route("/<int:id>", methods=["PUT"])
def atualizar_usuario(id):
    usuario = Usuario.query.get_or_404(id, description="Usuário não encontrado")
    data = request.get_json()

    if "nome" in data:
        usuario.nome = data["nome"]
    if "email" in data:
        if Usuario.query.filter_by(email=data["email"]).first():
            return jsonify({"erro": "Email já em uso"}), 409
        usuario.email = data["email"]

    db.session.commit()
    return jsonify(usuario.to_dict()), 200


# DELETE - Remover usuário
@usuarios_bp.route("/<int:id>", methods=["DELETE"])
def deletar_usuario(id):
    usuario = Usuario.query.get_or_404(id, description="Usuário não encontrado")
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"mensagem": "Usuário removido com sucesso"}), 200

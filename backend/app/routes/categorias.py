from flask import Blueprint, request, jsonify
from app import db
from app.models import Categoria

categorias_bp = Blueprint("categorias", __name__)


# CREATE - Criar categoria
@categorias_bp.route("/", methods=["POST"])
def criar_categoria():
    data = request.get_json()

    if not data or not data.get("nome"):
        return jsonify({"erro": "Nome da categoria é obrigatório"}), 400

    categoria = Categoria(
        nome=data["nome"],
        descricao=data.get("descricao", "")
    )
    db.session.add(categoria)
    db.session.commit()

    return jsonify(categoria.to_dict()), 201


# READ - Listar categorias
@categorias_bp.route("/", methods=["GET"])
def listar_categorias():
    categorias = Categoria.query.all()
    return jsonify([c.to_dict() for c in categorias]), 200


# READ - Buscar categoria por ID
@categorias_bp.route("/<int:id>", methods=["GET"])
def buscar_categoria(id):
    categoria = Categoria.query.get_or_404(id, description="Categoria não encontrada")
    return jsonify(categoria.to_dict()), 200


# UPDATE - Atualizar categoria
@categorias_bp.route("/<int:id>", methods=["PUT"])
def atualizar_categoria(id):
    categoria = Categoria.query.get_or_404(id, description="Categoria não encontrada")
    data = request.get_json()

    if "nome" in data:
        categoria.nome = data["nome"]
    if "descricao" in data:
        categoria.descricao = data["descricao"]

    db.session.commit()
    return jsonify(categoria.to_dict()), 200


# DELETE - Remover categoria
@categorias_bp.route("/<int:id>", methods=["DELETE"])
def deletar_categoria(id):
    categoria = Categoria.query.get_or_404(id, description="Categoria não encontrada")
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({"mensagem": "Categoria removida com sucesso"}), 200

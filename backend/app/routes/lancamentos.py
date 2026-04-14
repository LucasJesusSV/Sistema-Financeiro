from flask import Blueprint, request, jsonify
from app import db
from app.models import Lancamento, Usuario, Categoria

lancamentos_bp = Blueprint("lancamentos", __name__)

TIPOS_VALIDOS = ["entrada", "saida"]


# CREATE - Criar lançamento
@lancamentos_bp.route("/", methods=["POST"])
def criar_lancamento():
    data = request.get_json()

    # Validação dos campos obrigatórios
    campos = ["descricao", "valor", "tipo", "usuario_id", "categoria_id"]
    for campo in campos:
        if campo not in data:
            return jsonify({"erro": f"Campo '{campo}' é obrigatório"}), 400

    # Regra de negócio 1: valor deve ser positivo
    if data["valor"] <= 0:
        return jsonify({"erro": "O valor do lançamento deve ser positivo"}), 422

    # Regra de negócio 2: tipo deve ser "entrada" ou "saida"
    if data["tipo"] not in TIPOS_VALIDOS:
        return jsonify({"erro": "O tipo deve ser 'entrada' ou 'saida'"}), 422

    # Regra de negócio 3: usuário deve existir
    usuario = Usuario.query.get(data["usuario_id"])
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    # Regra de negócio 3: categoria deve existir (lançamento obrigatoriamente associado)
    categoria = Categoria.query.get(data["categoria_id"])
    if not categoria:
        return jsonify({"erro": "Categoria não encontrada"}), 404

    lancamento = Lancamento(
        descricao=data["descricao"],
        valor=data["valor"],
        tipo=data["tipo"],
        usuario_id=data["usuario_id"],
        categoria_id=data["categoria_id"]
    )
    db.session.add(lancamento)
    db.session.commit()

    return jsonify(lancamento.to_dict()), 201


# READ - Listar lançamentos (com filtros opcionais)
@lancamentos_bp.route("/", methods=["GET"])
def listar_lancamentos():
    usuario_id = request.args.get("usuario_id")
    tipo = request.args.get("tipo")
    categoria_id = request.args.get("categoria_id")

    query = Lancamento.query

    if usuario_id:
        query = query.filter_by(usuario_id=usuario_id)
    if tipo:
        if tipo not in TIPOS_VALIDOS:
            return jsonify({"erro": "Tipo inválido. Use 'entrada' ou 'saida'"}), 400
        query = query.filter_by(tipo=tipo)
    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)

    lancamentos = query.all()
    return jsonify([l.to_dict() for l in lancamentos]), 200


# READ - Buscar lançamento por ID
@lancamentos_bp.route("/<int:id>", methods=["GET"])
def buscar_lancamento(id):
    lancamento = Lancamento.query.get_or_404(id, description="Lançamento não encontrado")
    return jsonify(lancamento.to_dict()), 200


# READ - Resumo financeiro de um usuário
@lancamentos_bp.route("/resumo/<int:usuario_id>", methods=["GET"])
def resumo_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id, description="Usuário não encontrado")

    entradas = db.session.query(db.func.sum(Lancamento.valor)).filter_by(
        usuario_id=usuario_id, tipo="entrada"
    ).scalar() or 0

    saidas = db.session.query(db.func.sum(Lancamento.valor)).filter_by(
        usuario_id=usuario_id, tipo="saida"
    ).scalar() or 0

    return jsonify({
        "usuario": usuario.nome,
        "total_entradas": entradas,
        "total_saidas": saidas,
        "saldo": entradas - saidas
    }), 200


# UPDATE - Atualizar lançamento
@lancamentos_bp.route("/<int:id>", methods=["PUT"])
def atualizar_lancamento(id):
    lancamento = Lancamento.query.get_or_404(id, description="Lançamento não encontrado")
    data = request.get_json()

    if "valor" in data:
        if data["valor"] <= 0:
            return jsonify({"erro": "O valor deve ser positivo"}), 422
        lancamento.valor = data["valor"]

    if "tipo" in data:
        if data["tipo"] not in TIPOS_VALIDOS:
            return jsonify({"erro": "O tipo deve ser 'entrada' ou 'saida'"}), 422
        lancamento.tipo = data["tipo"]

    if "descricao" in data:
        lancamento.descricao = data["descricao"]

    if "categoria_id" in data:
        categoria = Categoria.query.get(data["categoria_id"])
        if not categoria:
            return jsonify({"erro": "Categoria não encontrada"}), 404
        lancamento.categoria_id = data["categoria_id"]

    db.session.commit()
    return jsonify(lancamento.to_dict()), 200


# DELETE - Remover lançamento
@lancamentos_bp.route("/<int:id>", methods=["DELETE"])
def deletar_lancamento(id):
    lancamento = Lancamento.query.get_or_404(id, description="Lançamento não encontrado")
    db.session.delete(lancamento)
    db.session.commit()
    return jsonify({"mensagem": "Lançamento removido com sucesso"}), 200

-- ============================================================
-- SISTEMA FINANCEIRO SIMPLIFICADO
-- Script de criação do banco de dados
-- ============================================================
 
-- ============================================================
-- TABELA: usuarios
-- Armazena os usuários do sistema
-- ============================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id          INTEGER      PRIMARY KEY AUTOINCREMENT,
    nome        VARCHAR(100) NOT NULL,
    email       VARCHAR(150) NOT NULL UNIQUE,
    criado_em   DATETIME     DEFAULT CURRENT_TIMESTAMP
);
 
-- ============================================================
-- TABELA: categorias
-- Armazena as categorias dos lançamentos financeiros
-- ============================================================
CREATE TABLE IF NOT EXISTS categorias (
    id          INTEGER      PRIMARY KEY AUTOINCREMENT,
    nome        VARCHAR(100) NOT NULL,
    descricao   VARCHAR(255)
);
 
-- ============================================================
-- TABELA: lancamentos
-- Armazena os lançamentos financeiros (entradas e saídas)
-- Regras de negócio:
--   1. valor deve ser positivo (> 0)
--   2. tipo deve ser 'entrada' ou 'saida'
--   3. categoria_id é obrigatório (NOT NULL)
-- ============================================================
CREATE TABLE IF NOT EXISTS lancamentos (
    id            INTEGER      PRIMARY KEY AUTOINCREMENT,
    descricao     VARCHAR(255) NOT NULL,
    valor         FLOAT        NOT NULL CHECK (valor > 0),
    tipo          VARCHAR(10)  NOT NULL CHECK (tipo IN ('entrada', 'saida')),
    data          DATETIME     DEFAULT CURRENT_TIMESTAMP,
    usuario_id    INTEGER      NOT NULL,
    categoria_id  INTEGER      NOT NULL,
    FOREIGN KEY (usuario_id)   REFERENCES usuarios(id)   ON DELETE CASCADE,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE RESTRICT
);
 
-- ============================================================
-- ÍNDICES para melhorar performance nas consultas
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_lancamentos_usuario   ON lancamentos(usuario_id);
CREATE INDEX IF NOT EXISTS idx_lancamentos_categoria ON lancamentos(categoria_id);
CREATE INDEX IF NOT EXISTS idx_lancamentos_tipo      ON lancamentos(tipo);
CREATE INDEX IF NOT EXISTS idx_usuarios_email        ON usuarios(email);
 
-- ============================================================
-- DADOS DE EXEMPLO
-- ============================================================
 
-- Usuários
INSERT INTO usuarios (nome, email) VALUES
    ('João Silva',   'joao@email.com'),
    ('Maria Souza',  'maria@email.com'),
    ('Carlos Lima',  'carlos@email.com');
 
-- Categorias
INSERT INTO categorias (nome, descricao) VALUES
    ('Alimentação',   'Gastos com supermercado, restaurantes e delivery'),
    ('Transporte',    'Gastos com combustível, uber e transporte público'),
    ('Saúde',         'Gastos com farmácia, consultas e plano de saúde'),
    ('Educação',      'Gastos com cursos, livros e materiais'),
    ('Salário',       'Receita mensal de salário'),
    ('Freelance',     'Receitas de trabalhos extras'),
    ('Lazer',         'Gastos com entretenimento e hobbies');
 
-- Lançamentos (entradas e saídas)
INSERT INTO lancamentos (descricao, valor, tipo, usuario_id, categoria_id) VALUES
    ('Salário mensal',          3500.00, 'entrada', 1, 5),
    ('Freelance site',           800.00, 'entrada', 1, 6),
    ('Supermercado',             250.00, 'saida',   1, 1),
    ('Uber para o trabalho',      45.00, 'saida',   1, 2),
    ('Farmácia',                  80.00, 'saida',   1, 3),
    ('Curso de Python',          199.00, 'saida',   1, 4),
    ('Cinema',                    60.00, 'saida',   1, 7),
    ('Salário mensal',          2800.00, 'entrada', 2, 5),
    ('Restaurante almoço',        35.00, 'saida',   2, 1),
    ('Combustível',              150.00, 'saida',   2, 2);
 
-- ============================================================
-- CONSULTAS ÚTEIS PARA VERIFICAÇÃO
-- ============================================================
 
-- Ver todos os usuários
-- SELECT * FROM usuarios;
 
-- Ver todos os lançamentos com nome do usuário e categoria
-- SELECT
--     l.id,
--     u.nome AS usuario,
--     c.nome AS categoria,
--     l.descricao,
--     l.valor,
--     l.tipo,
--     l.data
-- FROM lancamentos l
-- JOIN usuarios u ON l.usuario_id = u.id
-- JOIN categorias c ON l.categoria_id = c.id
-- ORDER BY l.data DESC;
 
-- Resumo financeiro por usuário
-- SELECT
--     u.nome,
--     SUM(CASE WHEN l.tipo = 'entrada' THEN l.valor ELSE 0 END) AS total_entradas,
--     SUM(CASE WHEN l.tipo = 'saida'   THEN l.valor ELSE 0 END) AS total_saidas,
--     SUM(CASE WHEN l.tipo = 'entrada' THEN l.valor ELSE -l.valor END) AS saldo
-- FROM usuarios u
-- LEFT JOIN lancamentos l ON u.id = l.usuario_id
-- GROUP BY u.id, u.nome;
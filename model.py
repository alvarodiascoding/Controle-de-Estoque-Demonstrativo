# model.py

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    Boolean
)
from datetime import datetime
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    relationship
)

# Conexão com o banco SQLite
engine = create_engine("sqlite:///Controle_de_Estoque_&_DRE.db")

Base = declarative_base()


class produtos(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True)
    produto = Column(String, nullable=False, unique=True)

    preco_venda = Column(Float, default=0.0)
    preco_compra = Column(Float, default=0.0)
    ativo = Column(Boolean, default=True)

    # Relacionamentos
    estoque = relationship(
        "Estoque",
        back_populates="produto_rel",
        cascade="all, delete"
    )

    historico = relationship(
        "Historico",
        back_populates="produto_rel",
        cascade="all, delete"
    )

class Estoque(Base):
    __tablename__ = "estoque"

    id = Column(Integer, primary_key=True)

    # Referência ao produto
    id_produto = Column(
        Integer,
        ForeignKey("produtos.id"),
        unique=True
    )

    quantidade = Column(Integer, nullable=False, default=0)

    produto_rel = relationship(
        "produtos",
        back_populates="estoque"
    )

class Historico(Base):
    __tablename__ = "historico"

    id = Column(Integer, primary_key=True)

    data_criacao = Column(
        DateTime,
        default=datetime.now
    )

    id_produto = Column(
        Integer,
        ForeignKey("produtos.id")
    )

    tipo = Column(String, nullable=False)

    quantidade = Column(Integer, nullable=False)

    movimentacao = Column(String, nullable=False)

    produto_rel = relationship(
        "produtos",
        back_populates="historico"
    )

class Resultado(Base):
    __tablename__ = "resultado"

    id = Column(Integer, primary_key=True)

    receita_bruta = Column(Float, default=0)

    custo_produtos = Column(Float, default=0)

    lucro_bruto = Column(Float, default=0)

#custo fixo

class custofixo(Base):
    __tablename__ = "custofixo"

    id = Column(Integer, primary_key=True)
    nomecf = Column(String, nullable=False, unique=True)

    valorcf = Column(Float, default=0.0)

# Sessão do banco
Session = sessionmaker(bind=engine)
session = Session()

# Criação das tabelas
Base.metadata.create_all(engine)


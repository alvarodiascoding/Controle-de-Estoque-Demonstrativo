# Sistema.py

from model import produtos, Estoque, Historico, Resultado, custofixo, session
from Dao import CatalogoDao, EstoqueDao, HistoricoDao, CustofixoDao, ResultadoDao
import re

# Instâncias dos DAOs
CatalogoDao1 = CatalogoDao(session, produtos)
EstoqueDao1 = EstoqueDao(session, Estoque)
HistoricoDao1 = HistoricoDao(session, Historico)
CustofixoDao1 = CustofixoDao(session, custofixo)
ResultadoDao1 = ResultadoDao(session, Resultado)


class SistemaBase:
    def __init__(self, session, ObjectsDao):
        self.session = session
        self.ObjectsDao = ObjectsDao

    def ver_tabela(self):
        return self.ObjectsDao.listar()

    def ver_itens_porID(self, id_produto1):
        produto = self.ObjectsDao.buscar_produtoID(id_produto1)

        if not produto:
            raise ValueError("O item não existe")

        return produto

    def ver_itens_porNome(self, nome1):
        produto = self.ObjectsDao.buscar_produtoNome(nome1)

        if not produto:
            raise ValueError("O item não existe")

        return produto

    def remover_produto(self, id_produto1):
        if not self.ObjectsDao.buscar_produtoID(id_produto1):
            raise ValueError("Esse produto não existe")

        self.ObjectsDao.remover_geral(id_produto1)

    def remover_custofixo(self, id1):
        if not self.ObjectsDao.buscar_cfID(id1):
            raise ValueError("Esse custo não existe")

        self.ObjectsDao.remover_custofixoDAO(id1)

    def atualizar_nome(self, novo_nome, id_produto1):
        produto = self.ObjectsDao.buscar_produtoID(id_produto1)

        if produto:
            produto.produto = novo_nome
            self.ObjectsDao.atualizar()

    def atualizar_preco_venda(self, novo_preco_venda, id_produto1):
        produto = self.ObjectsDao.buscar_produtoID(id_produto1)

        if produto:
            produto.preco_venda = novo_preco_venda
            self.ObjectsDao.atualizar()

    def atualizar_preco_compra(self, novo_preco_compra, id_produto1):
        produto = self.ObjectsDao.buscar_produtoID(id_produto1)

        if produto:
            produto.preco_compra = novo_preco_compra
            self.ObjectsDao.atualizar()

    def atualizar_quantidade(self, nova_quantidade, id_produto1):
        produto = self.ObjectsDao.buscar_produtoID(id_produto1)

        if produto:
            produto.quantidade = nova_quantidade
            self.ObjectsDao.atualizar()

class CustofixoController(SistemaBase):

    def adicionar_custofixo(self, nomecf1, valorcf1):

        nomecf1 = nomecf1.strip()
        valorcf1 = valorcf1.strip()
 
        if not nomecf1 or not valorcf1:
            raise ValueError("Nada pode estar vazio")

        if self.ObjectsDao.buscar_custoNome(nomecf1):
            raise ValueError("O custo já existe")

        if not re.fullmatch(r"[0-9.,]+", valorcf1):
           raise ValueError("Preço inválido")   
        else:    
            try:
                if isinstance(valorcf1, str):
                    valorcf1 = valorcf1.replace(",",".").strip()
                if isinstance(valorcf1, str):
                    valorcf1 = valorcf1.replace(",",".").strip()
            except ValueError:
                raise ValueError("Preço inválido")

        self.ObjectsDao.adicionar_custofixo(
            nomecf1,
            valorcf1,
        )

class CatalogoController(SistemaBase):

    def adicionar_produto_catalogo(self, nome1, preco_venda1, preco_compra1):

        nome1 = nome1.strip()
        preco_venda1 = preco_venda1.strip()
        preco_compra1 = preco_compra1.strip()

        if not preco_venda1.replace(",", ".").replace(".", "", 1).isdigit():
            raise ValueError("O preço de venda deve conter apenas números.")

        if not preco_compra1.replace(",", ".").replace(".", "", 1).isdigit():
            raise ValueError("O preço de compra deve conter apenas números.")
 
        if not nome1 or not preco_venda1 or not preco_compra1:
            raise ValueError("Nada pode estar vazio")

        if self.ObjectsDao.buscar_produtoNome(nome1):
            raise ValueError("O produto já existe")

        if not re.fullmatch(r"[0-9.,]+", preco_venda1):
           raise ValueError("Preço inválido")   
        else:    
            try:
                if isinstance(preco_venda1, str):
                    preco_venda1 = preco_venda1.replace(",",".").strip()
                if isinstance(preco_compra1, str):
                    preco_compra1 = preco_compra1.replace(",",".").strip()
            except ValueError:
                raise ValueError("Preço inválido")

        self.ObjectsDao.adicionar_catalogo(
            nome1,
            preco_venda1,
            preco_compra1,
        )


class EstoqueController(SistemaBase):

    def adicionar_produto_estoque(self, nome1):
        """
        Cadastro simplificado:
        - quantidade inicial = 0
        """

        nome1 = nome1.strip()

        if nome1 == "":
            raise ValueError("O nome não pode ser vazio")

        if nome1.isdigit():
            raise ValueError("Apenas letras são permitidas")

        if self.ObjectsDao.buscar_produtoNome(nome1):
            raise ValueError("O produto já existe")

        self.ObjectsDao.adicionar_estoque(
            nome1,
            0
        )

    def somar_produto_estoque(self, id_produto1, quantidade1):

        if not self.ObjectsDao.buscar_produtoID(id_produto1):
            raise ValueError("Esse produto não existe")

        if quantidade1 <= 0:
            raise ValueError(
                "Não são aceitos números negativos ou 0"
            )

        self.ObjectsDao.somar_estoque(
            id_produto1,
            quantidade1
        )

    def diminuir_produto_estoque(self, id_produto1, quantidade1):

        if not self.ObjectsDao.buscar_produtoID(id_produto1):
            raise ValueError("Esse produto não existe")

        if quantidade1 <= 0:
            raise ValueError(
                "Não são aceitos números negativos ou 0"
            )

        estoque = self.ObjectsDao.buscar_produtoID(id_produto1)

        if estoque.quantidade < quantidade1:
            raise ValueError(
                "Não é possível remover além da quantidade existente"
            )

        self.ObjectsDao.diminuir_estoque(
            id_produto1,
            quantidade1
        )

class HistoricoController(SistemaBase):

    def ver_conjunto_de_itens_porID(self, id_produto1):
        return self.ObjectsDao.ver_conjunto_itensID(
            id_produto1
        )

    def ver_conjunto_de_itens_porNome(self, nome1):
        return self.ObjectsDao.ver_conjunto_itensNome(
            nome1
        )

    def remover_do_historico(self, id_produto1):
        self.ObjectsDao.remover_historico(
            id_produto1
        )

class ResultadoController(SistemaBase):

    def calcular_resultado(
        self,
        mes=None,
        ano=None,
        aliquota=4.0
    ):

        receita_bruta = 0
        custo_produtos = 0

        movimentacoes = self.ObjectsDao.buscar_movimentacoes()

        for mov in movimentacoes:

            if mov.tipo != "-":
                continue

            if mes is not None and mov.data_criacao.month != mes:
                continue

            if ano is not None and mov.data_criacao.year != ano:
                continue

            produto = CatalogoDao1.buscar_produtoID(
                mov.id_produto
            )

            receita_bruta += (
                produto.preco_venda *
                mov.quantidade
            )

            custo_produtos += (
                produto.preco_compra *
                mov.quantidade
            )

        # Simples Nacional (4%)
        simples_nacional = receita_bruta * (aliquota / 100)

        # Receita líquida
        receita_liquida = (
            receita_bruta -
            simples_nacional
        )

        # Lucro bruto (sem impostos)
        lucro_bruto = (
            receita_bruta -
            custo_produtos
        )

        # Lucro líquido (com impostos)
        lucro_liquido = (
            receita_liquida -
            custo_produtos
        )

        return {

            "receita_bruta": receita_bruta,

            "custo_produtos": custo_produtos,

            "lucro_bruto": lucro_bruto,

            "simples_nacional": simples_nacional,

            "receita_liquida": receita_liquida,

            "lucro_liquido": lucro_liquido

        }

# Instâncias dos Controllers
CatalogoController1 = CatalogoController(
    session,
    CatalogoDao1
)

EstoqueController1 = EstoqueController(
    session,
    EstoqueDao1
)

HistoricoController1 = HistoricoController(
    session,
    HistoricoDao1
)

CustofixoController1 = CustofixoController(
    session,
    CustofixoDao1
)

ResultadoController1 = ResultadoController(
    session,
    ResultadoDao1
)
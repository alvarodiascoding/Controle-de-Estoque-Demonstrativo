# Dao.py

from model import produtos, Estoque, Historico, Resultado, custofixo 


class ObjectsDao:
    def __init__(self, session, tabela):
        self.session = session
        self.tabela = tabela

    def buscar_produtoID(self, id_produto1):
        return (
            self.session
            .query(self.tabela)
            .filter_by(id=id_produto1)
            .first()
        )

    def buscar_cfID(self, id1):
        return (
            self.session
            .query(self.tabela)
            .filter_by(id=id1)
            .first()
        )


    def buscar_produtoNome(self, nome1):
        """
        Busca pelo nome do produto.

        Funciona para:
        - produtos
        - Estoque
        - Historico
        """

        if self.tabela == produtos:

            return (
                self.session
                .query(produtos)
                .filter_by(produto=nome1)
                .first()
            )

        elif self.tabela == Estoque:

            return (
                self.session
                .query(Estoque)
                .join(produtos)
                .filter(produtos.produto == nome1)
                .first()
            )

        elif self.tabela == Historico:

            return (
                self.session
                .query(Historico)
                .join(produtos)
                .filter(produtos.produto == nome1)
                .first()
            )

    def buscar_custoNome(self, nomecf1):

        if self.tabela == custofixo:

            return (
                self.session
                .query(custofixo)
                .filter_by(nomecf=nomecf1)
                .first()
            )
        
    def listar(self):

        if self.tabela == produtos:

            return (
                self.session
                .query(produtos)
                .filter_by(ativo=True)
                .all()
            )

        return self.session.query(self.tabela).all()

    def remover_custofixoDAO(self, id1):

        cf = (
            self.session
            .query(custofixo)
            .filter_by(id=id1)
            .first()
        )

        if cf:
            self.session.delete(cf)

        self.atualizar()

    def remover_geral(self, id_produto1):

        produto = (
            self.session
            .query(produtos)
            .filter_by(id=id_produto1)
            .first()
        )

        if produto:

            produto.ativo = False

            self.atualizar()

    def remover(self, objeto):

        if objeto:
            self.session.delete(objeto)
            self.atualizar()

    def atualizar(self):
        self.session.commit()

    def adicionar(self, objeto):
        self.session.add(objeto)
        self.atualizar()


class CatalogoDao(ObjectsDao):

    def adicionar_catalogo(
        self,
        nome1,
        preco_venda1,
        preco_compra1
    ):

        novo_produto = produtos(
            produto=nome1,
            preco_venda=preco_venda1,
            preco_compra=preco_compra1
        )

        self.adicionar(novo_produto)

class ResultadoDao(ObjectsDao):

    def buscar_movimentacoes(self):

        return (
            self.session
            .query(Historico)
            .all()
        )

    def adicionar_custo(self, valor):

        resultado = self.session.query(Resultado).first()

        if resultado is None:
            resultado = Resultado(
                receita_bruta=0,
                custo_produtos=0,
                lucro_bruto=0
            )
            self.session.add(resultado)

        resultado.custo_produtos += valor
        resultado.lucro_bruto = (
            resultado.receita_bruta -
            resultado.custo_produtos
        )

        self.atualizar()

    def buscar_resultado(self):
        return self.session.query(Resultado).first()

class CustofixoDao(ObjectsDao):

    def adicionar_custofixo(
        self,
        nomecf1,
        valorcf1
    ):

        novo_custo = custofixo(
            nomecf=nomecf1,
            valorcf=valorcf1
        )

        self.adicionar(novo_custo)

    def total_custos(self):

        custos = (
            self.session
            .query(custofixo)
            .all()
        )

        return sum(c.valorcf for c in custos)

class EstoqueDao(ObjectsDao):

    def adicionar_estoque(
        self,
        nome1,
        quantidade1
    ):
        """
        Cria o estoque associado ao produto recém criado.
        """

        produto = (
            self.session
            .query(produtos)
            .filter_by(produto=nome1)
            .first()
        )

        novo_estoque = Estoque(
            id_produto=produto.id,
            quantidade=quantidade1
        )

        self.adicionar(novo_estoque)

    def somar_estoque(
        self,
        id_produto1,
        quantidade1
    ):

        estoque = (
            self.session
            .query(Estoque)
            .filter_by(id_produto=id_produto1)
            .first()
        )

        estoque.quantidade += quantidade1

        novo_historico = Historico(
                id_produto=id_produto1,
                tipo="+",
                quantidade=quantidade1,
                movimentacao=(
                    f'+{quantidade1}, '
                    f'{estoque.quantidade} restantes'
                )
            )

        self.session.add(novo_historico)

        self.atualizar()

    def diminuir_estoque(
        self,
        id_produto1,
        quantidade1
    ):

        estoque = (
            self.session
            .query(Estoque)
            .filter_by(id_produto=id_produto1)
            .first()
        )

        estoque.quantidade -= quantidade1

        novo_historico = Historico(
                id_produto=id_produto1,
                tipo="-",
                quantidade=quantidade1,
                movimentacao=(
                    f'-{quantidade1}, '
                    f'{estoque.quantidade} restantes'
                )
            )

        self.session.add(novo_historico)

        self.atualizar()

    def buscar_produtoID(self, id_produto1):
        """
        No estoque buscamos pelo id do produto,
        e não pelo id interno do estoque.
        """

        return (
            self.session
            .query(Estoque)
            .filter_by(id_produto=id_produto1)
            .first()
        )


class HistoricoDao(ObjectsDao):

    def ver_conjunto_itensID(self, data1):

        return (
            self.session
            .query(Historico)
            .filter_by(data=data1)
            .all()
        )

    def ver_conjunto_itensNome(self, nome1):

        return (
            self.session
            .query(Historico)
            .join(produtos)
            .filter(produtos.produto == nome1)
            .all()
        )

    def remover_historico(self, id_historico):

        historico = (
            self.session
            .query(Historico)
            .filter_by(id=id_historico)
            .first()
        )

        self.remover(historico)
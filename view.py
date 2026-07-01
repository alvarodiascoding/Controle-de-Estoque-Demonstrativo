# view.py

from datetime import datetime
import PySimpleGUI as sg
from Sistema import (
    CatalogoController1,
    EstoqueController1,
    HistoricoController1,
    CustofixoController1,
    ResultadoController1
)

def atualizar_tabela_produtos(window):
    dados = []

    for produto in CatalogoController1.ver_tabela():

        estoque = EstoqueController1.ver_itens_porID(produto.id)

        quantidade = estoque.quantidade if estoque else 0

        dados.append([
            produto.id,
            produto.produto,
            f"R$ {produto.preco_venda:.2f}".replace(".", ","),
            f"R$ {produto.preco_compra:.2f}".replace(".", ","),
            quantidade
        ])

    window["-TABELA_PRODUTOS-"].update(values=dados)


def atualizar_tabela_historico(window, mes=None):
    dados = []

    for item in HistoricoController1.ver_tabela():

        if mes is not None:
            if item.data_criacao.month != mes:
                continue

        dados.append([
            item.data_criacao.strftime("%d/%m/%Y às %H:%M"),
            item.produto_rel.produto,
            item.movimentacao
        ])

    window["-TABELA_HISTORICO-"].update(values=dados)

# custo fixo

def atualizar_tabela_custofixo(window):
    dados = []

    for custofixo in CustofixoController1.ver_tabela():

        dados.append([
            custofixo.id,
            custofixo.nomecf,
            f"R$ {custofixo.valorcf:.2f}".replace(".", ","),
        ])

    window["-TABELA_CUSTO_FIXO-"].update(values=dados)

def layout_custo_fixo():
    return [
        [
            sg.Text(
                "Adicione seus custos mensáis:",
                font=("Arial", 14, "bold")
            )
        ],
        [
            sg.Text("Custo:"),

            sg.Input(
                key="-NOMECF-",
                size=(15, 1)
            ),

            sg.Text("Valor:"),

            sg.Input(
                key="-VALORCF-",
                size=(5, 1)
            ),

            sg.Button(
                " Submit ",
                key="-ADICIONARCF-"
            ),
        ],
        [
            sg.Table(
                values=[],
                headings=[
                    "ID",
                    "Custo",
                    "Valor",
                ],

                background_color="#DEE7ED",
                text_color="#000000",

                header_background_color="#FFFFFF",
                header_text_color="#000000",

                alternating_row_color="#C9D2D8",

                key="-TABELA_CUSTO_FIXO-",
                auto_size_columns=False,
                col_widths=[15, 20, 30],
                justification="center",
                num_rows=15,
                expand_x=True,
                expand_y=True
            )
        ],
        [
            sg.Text("ID:"),

            sg.Input(
                key="-CF_REMOVER_ID-",
                size=(3, 1)
            ),

            sg.Button(
                " Execute ",
                key="-CF_REMOVER-"
            )
        ],
    ]

# resultados

aliquotas = {
    " Comércio": 4.0,
    " Indústria": 4.5,
    " Serviços III": 6.0,
    " Serviços IV": 4.5,
    " Serviços V": 15.5
}

def layout_resultados():
    ano_atual = datetime.now().year

    anos = [
        str(ano)
        for ano in range(ano_atual - 10, ano_atual + 1)
    ]

    return [
        [
            sg.Text(
                "Resultados",
                font=("Arial", 14, "bold")
            ),

            sg.Push(),

            sg.Text(
                "Aliquota:",
            ),

            sg.Combo(
                values=list(aliquotas.keys()),
                default_value=" Comércio",
                readonly=True,
                key="-ALIQUOTA-",
                size=(10,1),
                enable_events=True
            )
        ],

        [
            sg.Text("Mês:"),

            sg.Combo(
                values=[
                    "1", "2", "3", "4", "5", "6",
                    "7", "8", "9", "10", "11", "12"
                ],
                readonly=True,
                key="-MES_RESULTADO-",
                size=(3,1)
            ),

            sg.Text("Ano:"),

            sg.Combo(
                values=anos,
                readonly=True,
                key="-ANO_RESULTADO-",
                size=(6,1)
            ),

            sg.Push(),

            sg.Button(
                "Pesquisar",
                key="-PESQUISAR_RESULTADO-"
            ),

            sg.Button(
                "Limpar",
                key="-LIMPAR_RESULTADO-"
            )
        ],

        [sg.HorizontalSeparator()],

        [
            sg.Text(
                "Impostos:",
                font=("Arial", 12, "bold")
            ),

            sg.Push(),

            sg.Text(
                "Simples Nacional"
            ),
        ],

        [sg.HorizontalSeparator()],

        [
            sg.Text(
                "Faturamento (+)"
            ),

            sg.Push(),

            sg.Text(
                "R$ 0,00",
                key="-RECEITA_BRUTA-"
            )
        ],

        [
            sg.Text(
                "Simples Nacional 2026 (-)"
            ),

            sg.Push(),

            sg.Text(
                "R$ 0,00",
                key="-SIMPLES-NACIONAL-",
            ),
        ],

        [
            sg.Text(
                "Receita Líquida ="
            ),

            sg.Push(),

            sg.Text(
                "R$ 0,00",
                key="-RECEITA_LIQUIDA-",
            ),
        ],

        [sg.HorizontalSeparator()],

        [
            sg.Text(
                "CMV/CPV (-)"
            ),

            sg.Push(),

            sg.Text(
                "R$ 0,00",
                key="-CPV-"
            )
        ],

        [
            sg.Text(
                "Lucro Bruto ="
            ),

            sg.Push(),

            sg.Text(
                "R$ 0,00",
                key="-LUCRO_BRUTO-"
            )
        ],

        [sg.HorizontalSeparator()],

        [
            sg.Text(
                "Custos Fixos (-)"
            ),

            sg.Push(),

            sg.Text(
                "R$ 0,00",
                key="-CUSTO_FIXO_TOTAL-"
            )
        ],


        [
            sg.Text(
                "Lucro Líquido ="
            ),

            sg.Push(),

            sg.Text(
                "R$ 0,00",
                key="-LUCRO_LIQUIDO-",
            ),
        ],

    ]

def executar():
    coluna_esquerda = [
        [
            sg.Text(
                "Cadastro",
                font=("Arial", 14, "bold")
            )
        ],

        [
            sg.Text("Nome:"),

            sg.Input(
                key="-NOME-",
                size=(15, 1)
            ),

            sg.Text("Venda / Compra:"),

            sg.Input(
                key="-VENDA-",
                size=(5, 0)
            ),

            sg.Input(
                key="-COMPRA-",
                size=(5, 1)
            ),

            sg.Button(
                " Submit ",
                key="-CADASTRAR-"
            )
        ],

        [sg.HorizontalSeparator()],

        [
            sg.Text(
                "Remoção",
                font=("Arial", 14, "bold")
            )
        ],

        [
            sg.Text("ID:"),

            sg.Input(
                key="-REMOVER_ID-",
                size=(3, 1)
            ),

            sg.Button(
                " Execute ",
                key="-REMOVER-"
            )
        ],

        [
            sg.Text(
                "Produtos",
                font=("Arial", 14, "bold")
            )
        ],

        [
            sg.Table(
                values=[],
                headings=["ID", "Produto", "Venda", "Compra", "Qnt."],
                key="-TABELA_PRODUTOS-",
                auto_size_columns=False,
                col_widths=[8, 25, 12],
                justification="center",
                num_rows=15,
                expand_x=True,
                expand_y=True,

                background_color="#DEE7ED",
                text_color="#000000",

                header_background_color="#FFFFFF",
                header_text_color="#000000",

                alternating_row_color="#C9D2D8"
            )
        ]
    ]

    coluna_direita = [
        [
            sg.Text(
                "Movimentações",
                font=("Arial", 14, "bold"),
                pad = ((0,0), (40, 0))
            ),
            sg.Column(
                [[
                    sg.Push(),
                    sg.Button(
                        " Adicionar Custo Fixo ",
                        key="-ADCUSTOFIXO-"
                    ),
                    sg.Button(
                        " Resultados ",
                        key="-RESULTADOS-"
                    )
                ]],
                expand_x=True,
                pad=((0,0),(0,20))
            )
        ],

        [
            sg.Text("ID:"),

            sg.Input(
                key="-MOV_ID-",
                size=(3, 1)
            ),

            sg.Combo(
                values=[" +", " -"],
                default_value=" +",
                readonly=True,
                key="-OPERACAO-",
                size=(3, 1)
            ),

            sg.Text("Qtd:"),

            sg.Input(
                key="-QUANTIDADE-",
                size=(6, 1)
            ),

            sg.Button(
                " Submit ",
                key="-MOVIMENTAR-"
            )
        ],

        [
            sg.Column(
                [[
                    sg.Text(
                        "Histórico",
                        font=("Arial", 14, "bold")
                    ),

                    sg.Push(),

                    sg.Text("Mês:"),

                    sg.Combo(
                        values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
                        readonly=True,
                        key="-MES-",
                        size=(3, 1)
                        ),
                    sg.Button(
                        " Filtrar ",
                        key="-FILTRAR-"
                    ),
                    sg.Button(
                        " Limpar ",
                        key="-LIMPAR-"
                    )
                ]],
                expand_x=True,
                pad=((0,0),(40,0))
            )
        ],

        [
            sg.Table(
                values=[],
                headings=[
                    "Data",
                    "Produto",
                    "Movimentação"
                ],

                background_color="#DEE7ED",
                text_color="#000000",

                header_background_color="#FFFFFF",
                header_text_color="#000000",

                alternating_row_color="#C9D2D8",

                key="-TABELA_HISTORICO-",
                auto_size_columns=False,
                col_widths=[15, 20, 30],
                justification="center",
                num_rows=15,
                expand_x=True,
                expand_y=True
            )
        ]
    ]

    layout = [
        [
            sg.Column(coluna_esquerda),

            sg.VSeparator(),

            sg.Column(coluna_direita)
        ]
    ]

    window = sg.Window(
        "Controle de Estoque & Demonstrativo",
        layout,
        resizable=True,
        finalize=True
    )

    atualizar_tabela_produtos(window)
    atualizar_tabela_historico(window)

    while True:

        evento, valores = window.read()

        if evento == sg.WINDOW_CLOSED:
            break

        try:

            if evento == "-CADASTRAR-":

                nome = valores["-NOME-"].strip()
                preco_venda = valores["-VENDA-"].strip()
                preco_compra = valores["-COMPRA-"].strip()

                CatalogoController1.adicionar_produto_catalogo(
                    nome,
                    preco_venda,
                    preco_compra
                )

                EstoqueController1.adicionar_produto_estoque(
                    nome
                )

                atualizar_tabela_produtos(window)

                window["-NOME-"].update("")
                window["-VENDA-"].update("")
                window["-COMPRA-"].update("")

                sg.popup(
                    "Produto cadastrado com sucesso!"
                )

            elif evento == "-REMOVER-":

                if not valores["-REMOVER_ID-"].isdigit():
                    raise ValueError("O ID deve conter apenas números.")

                id_produto = int(
                    valores["-REMOVER_ID-"]
                )

                CatalogoController1.remover_produto(
                    id_produto
                )

                atualizar_tabela_produtos(window)

                window["-REMOVER_ID-"].update("")

                sg.popup(
                    "Produto removido com sucesso!"
                )

            elif evento == "-MOVIMENTAR-":

                if not valores["-MOV_ID-"].isdigit():
                    raise ValueError("O ID deve conter apenas números.")

                if not valores["-QUANTIDADE-"].isdigit():
                    raise ValueError("A quantidade deve conter apenas números.")

                id_produto = int(
                    valores["-MOV_ID-"]
                )

                quantidade = int(
                    valores["-QUANTIDADE-"]
                )

                operacao = valores["-OPERACAO-"]

                if operacao == " +":

                    EstoqueController1.somar_produto_estoque(
                        id_produto,
                        quantidade
                    )

                elif operacao == " -":

                    EstoqueController1.diminuir_produto_estoque(
                        id_produto,
                        quantidade
                    )

                atualizar_tabela_produtos(window)
                atualizar_tabela_historico(window)

                window["-MOV_ID-"].update("")
                window["-QUANTIDADE-"].update("")

                sg.popup(
                    "Movimentação registrada!"
                )

            elif evento == "-FILTRAR-":

                mes = int(
                    valores["-MES-"]
                )

                atualizar_tabela_historico(
                    window,
                    mes
                )

            elif evento == "-LIMPAR-":

                window["-MES-"].update(value="")

                atualizar_tabela_historico(
                    window
                )

            elif evento == "-ADCUSTOFIXO-":

                janela_cf = sg.Window(
                    "Custos Fixos",
                    layout_custo_fixo(),
                    modal=True,
                    finalize=True
                )

                atualizar_tabela_custofixo(
                    janela_cf
                )

                while True:

                    ev_cf, val_cf = janela_cf.read()

                    if ev_cf == sg.WINDOW_CLOSED:
                        break

                    if ev_cf == "-ADICIONARCF-":

                        nome = val_cf["-NOMECF-"].strip()
                        valor = val_cf["-VALORCF-"].strip()

                        CustofixoController1.adicionar_custofixo(
                            nome,
                            valor
                        )

                        janela_cf["-NOMECF-"].update("")
                        janela_cf["-VALORCF-"].update("")

                        atualizar_tabela_custofixo(
                            janela_cf
                        )

                        sg.popup(
                            f"Custo adicionado: {nome} - R$ {valor}"
                        )

                    elif ev_cf == "-CF_REMOVER-":

                        id = int(
                            val_cf["-CF_REMOVER_ID-"]
                        )

                        CustofixoController1.remover_custofixo(
                            id
                        )

                        janela_cf["-CF_REMOVER_ID-"].update("")

                        atualizar_tabela_custofixo(
                            janela_cf
                        )

                        sg.popup(
                            "Custo-fixo removido com sucesso!"
                        )

                janela_cf.close()

            elif evento == "-RESULTADOS-":

                janela_rs = sg.Window(
                    "Resultados",
                    layout_resultados(),
                    modal=True,
                    finalize=True
                )

                # Primeira atualização da tela
                aliquota = aliquotas[
                    janela_rs["-ALIQUOTA-"].get()
                ]

                resultado = ResultadoController1.calcular_resultado(
                    aliquota=aliquota
                )

                janela_rs["-RECEITA_BRUTA-"].update(
                    f'R$ {resultado["receita_bruta"]:.2f}'.replace(".", ",")
                )

                janela_rs["-RECEITA_LIQUIDA-"].update(
                    f'R$ {resultado["receita_liquida"]:.2f}'.replace(".", ",")
                )

                janela_rs["-CUSTO_FIXO_TOTAL-"].update(
                    f"R$ {resultado['custo_fixo_total']:.2f}".replace(".", ",")
                )

                janela_rs["-CPV-"].update(
                    f'R$ {resultado["custo_produtos"]:.2f}'.replace(".", ",")
                )

                janela_rs["-LUCRO_BRUTO-"].update(
                    f'R$ {resultado["lucro_bruto"]:.2f}'.replace(".", ",")
                )

                janela_rs["-SIMPLES-NACIONAL-"].update(
                    f'R$ {resultado["simples_nacional"]:.2f}'.replace(".", ",")
                )

                janela_rs["-LUCRO_LIQUIDO-"].update(
                    f'R$ {resultado["lucro_liquido"]:.2f}'.replace(".", ",")
                )

                while True:

                    ev_rs, val_rs = janela_rs.read()

                    if ev_rs == sg.WINDOW_CLOSED:
                        break

                    elif ev_rs == "-ALIQUOTA-" or ev_rs == "-PESQUISAR_RESULTADO-":

                        mes = None
                        ano = None

                        if val_rs["-MES_RESULTADO-"] != "":
                            mes = int(
                                val_rs["-MES_RESULTADO-"]
                            )

                        if val_rs["-ANO_RESULTADO-"] != "":
                            ano = int(
                                val_rs["-ANO_RESULTADO-"]
                            )

                        aliquota = aliquotas[
                            val_rs["-ALIQUOTA-"]
                        ]

                        resultado = ResultadoController1.calcular_resultado(
                            mes=mes,
                            ano=ano,
                            aliquota=aliquota
                        )

                        janela_rs["-RECEITA_BRUTA-"].update(
                            f'R$ {resultado["receita_bruta"]:.2f}'.replace(".", ",")
                        )

                        janela_rs["-RECEITA_LIQUIDA-"].update(
                            f'R$ {resultado["receita_liquida"]:.2f}'.replace(".", ",")
                        )

                        janela_rs["-CPV-"].update(
                            f'R$ {resultado["custo_produtos"]:.2f}'.replace(".", ",")
                        )

                        janela_rs["-LUCRO_BRUTO-"].update(
                            f'R$ {resultado["lucro_bruto"]:.2f}'.replace(".", ",")
                        )

                        janela_rs["-SIMPLES-NACIONAL-"].update(
                            f'R$ {resultado["simples_nacional"]:.2f}'.replace(".", ",")
                        )

                        janela_rs["-LUCRO_LIQUIDO-"].update(
                            f'R$ {resultado["lucro_liquido"]:.2f}'.replace(".", ",")
                        )

                    elif ev_rs == "-LIMPAR_RESULTADO-":

                        janela_rs["-MES_RESULTADO-"].update("")
                        janela_rs["-ANO_RESULTADO-"].update("")

                        aliquota = aliquotas[
                            val_rs["-ALIQUOTA-"]
                        ]

                        resultado = ResultadoController1.calcular_resultado(
                            aliquota=aliquota
                        )

                        janela_rs["-RECEITA_BRUTA-"].update(
                            f'R$ {resultado["receita_bruta"]:.2f}'.replace(".", ",")
                        )

                        janela_rs["-RECEITA_LIQUIDA-"].update(
                            f'R$ {resultado["receita_liquida"]:.2f}'.replace(".", ",")
                        )

                        janela_rs["-CPV-"].update(
                            f'R$ {resultado["custo_produtos"]:.2f}'.replace(".", ",")
                        )

                        janela_rs["-LUCRO_BRUTO-"].update(
                            f'R$ {resultado["lucro_bruto"]:.2f}'.replace(".", ",")
                        )

                        janela_rs["-SIMPLES-NACIONAL-"].update(
                            f'R$ {resultado["simples_nacional"]:.2f}'.replace(".", ",")
                        )

                        janela_rs["-LUCRO_LIQUIDO-"].update(
                            f'R$ {resultado["lucro_liquido"]:.2f}'.replace(".", ",")
                        )

                janela_rs.close()

        except ValueError as erro:

            sg.popup_error(
                str(erro)
            )

        except Exception as erro:

            sg.popup_error(
                "Erro inesperado:",
                str(erro)
            )

    window.close()
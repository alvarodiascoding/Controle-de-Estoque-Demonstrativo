import hashlib
import PySimpleGUI as sg
import json
import os

ARQUIVO_LOGIN = "login.json"

def carregar_login():

    if not os.path.exists(ARQUIVO_LOGIN):

        usuario = "9cbca7897838293fb2a86c412124b55e08e5b05259b866b491308526eb8fd63c"
        senha = "1a128f7d536f1762aa430e310d8c41b41c147e445e6ac048da7ad178b8813e07"

        salvar_login(usuario, senha)

    with open(ARQUIVO_LOGIN, "r") as arquivo:
        dados = json.load(arquivo)

    return dados["usuario"], dados["senha"]


def salvar_login(usuario, hash_senha):

    with open(ARQUIVO_LOGIN, "w") as arquivo:
        json.dump(
            {
                "usuario": usuario,
                "senha": hash_senha
            },
            arquivo,
            indent=4
        )

HASH_USUARIO, HASH_SENHA = carregar_login()


def layout_cadastrar():

    return [
        [
            sg.Text(
                "Cadastro de Usuário",
                font=("Arial", 16, "bold")
            )
        ],

        [
            sg.Text("Novo Usuário:", size=(12, 1)),
            sg.Input(
                key="-NOVO_USUARIO-",
                size=(20, 1)
            )
        ],

        [
            sg.Text("Senha:", size=(12, 1)),
            sg.Input(
                password_char="*",
                key="-NOVA_SENHA-",
                size=(20, 1)
            )
        ],

        [
            sg.Push(),

            sg.Button(
                "Cadastrar",
                key="-NOVO_LOGIN-"
            ),

            sg.Button(
                "Cancelar",
                key="-CAD_CANCELAR-"
            )
        ]
    ]


def login():

    layout = [

        [
            sg.Text(
                "Login",
                font=("Arial", 16, "bold")
            ),

            sg.Push(),

            sg.Button(
                "Cadastrar",
                key="-CADASTRAR-"
            )
        ],

        [
            sg.Text(
                "Usuário:",
                size=(10, 1)
            ),

            sg.Input(
                key="-USUARIO-",
                size=(20, 1)
            )
        ],

        [
            sg.Text(
                "Senha:",
                size=(10, 1)
            ),

            sg.Input(
                password_char="*",
                key="-SENHA-",
                size=(20, 1)
            )
        ],

        [
            sg.Push(),

            sg.Button(
                "Entrar",
                key="-LOGIN-"
            ),

            sg.Button(
                "Cancelar",
                key="-CANCELAR-"
            )
        ]
    ]

    window = sg.Window(
        "Login",
        layout,
        finalize=True,
        modal=True
    )

    while True:

        evento, valores = window.read()

        if evento in (
            sg.WINDOW_CLOSED,
            "-CANCELAR-"
        ):

            window.close()
            return None

        if evento == "-LOGIN-":

            usuario_hash = hashlib.sha256(
                valores["-USUARIO-"].strip().encode()
            ).hexdigest()

            senha_hash = hashlib.sha256(
                valores["-SENHA-"].encode()
            ).hexdigest()

            if (
                usuario_hash == HASH_USUARIO
                and senha_hash == HASH_SENHA
            ):
                window.close()
                return "liberado"
            
            sg.popup_error(
                "Usuário ou senha incorretos."
            )

        elif evento == "-CADASTRAR-":

            usuario = valores["-USUARIO-"].strip()
            senha = valores["-SENHA-"]

            if (hashlib.sha256(usuario.encode()).hexdigest() == HASH_USUARIO and hashlib.sha256(senha.encode()).hexdigest() == HASH_SENHA):

                janela_cd = sg.Window(
                    "Cadastrar Usuário",
                    layout_cadastrar(),
                    modal=True,
                    finalize=True
                )

                while True:

                    ev_cd, val_cd = janela_cd.read()

                    if ev_cd in (
                        sg.WINDOW_CLOSED,
                        "-CAD_CANCELAR-"
                    ):
                        janela_cd.close()
                        break

                    elif ev_cd == "-NOVO_LOGIN-":

                        novo_usuario = val_cd["-NOVO_USUARIO-"].strip()
                        nova_senha = val_cd["-NOVA_SENHA-"]

                        if novo_usuario == "" or nova_senha == "":

                            sg.popup_error(
                                "Preencha todos os campos."
                            )

                            continue

                        hash_usuario = hashlib.sha256(
                            novo_usuario.encode()
                        ).hexdigest()

                        hash_senha = hashlib.sha256(
                            nova_senha.encode()
                        ).hexdigest()

                        salvar_login(
                            hash_usuario,
                            hash_senha
                        )

                        sg.popup(
                            "Novo usuário cadastrado com sucesso!"
                        )

                        janela_cd.close()
                        break

            elif usuario == "" and senha == "":

                sg.popup_error(
                    "Digite o usuário e a senha do administrador."
                )

            else:

                sg.popup_error(
                    "Usuário ou senha do administrador incorretos."
                )

    window.close()
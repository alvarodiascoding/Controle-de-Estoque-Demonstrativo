from view import executar
from login import login


def main():
    #executar()
    if login() == "liberado":
        executar()

if __name__ == "__main__":
    main()
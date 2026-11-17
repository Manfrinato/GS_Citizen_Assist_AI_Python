from base_conhecimento import BaseConhecimento
from assistente import Assistente


def main():
    base = BaseConhecimento("data/base_conhecimento.json")
    base.carregar()
    assistente = Assistente("Citizen Assist AI", base)

    while True:
        print("=" * 180)
        print("Citizen Assist_AI")
        print("="*180)
        print("Escolha uma dessa opção:")
        print("[1] Fazer pergunta")
        print("[2] Procurar por categorias")
        print("[3] consutar indicadores")
        print("[4] Exportar CSV")
        print("[0] sair")

        opcao = input()
        if opcao == "1":
            assistente.perguntar()
        elif opcao == "2":
            assistente.navegar()
        elif opcao == "3":
            assistente.indicadores()
        elif opcao == "4":
            assistente.exportar_csv()
        elif opcao == "0":
            break
        else:
            print("Erro")

if __name__ == "__main__":
    main()
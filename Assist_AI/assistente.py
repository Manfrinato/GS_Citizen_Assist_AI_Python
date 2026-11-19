from pathlib import Path
from datetime import datetime
import json
import csv
import time

class Assistente:
    def __init__(self, nome,base):
        self.nome = nome
        self.base = base
        self.historico = []
        self.data_dir = Path(__file__).resolve().parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.db_path = self.data_dir / "historico.json"
        self.csv_path = self.data_dir / "atendimentos.csv"

        if self.db_path.exists():
            try:
                self.historico = json.loads(self.db_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                self.historico = []
    def perguntar(self):
        inicio = time.time()
        tentativas = 0


        while True:
            print("Digite [0] para voltar:")
            pergunta = input("Digite sua duvida").strip()

            if pergunta == "0":
                return
            if not pergunta:
                continue
            numeros = 0

            for letra in pergunta:
                if letra.isdigit():
                    numeros +=1
            if numeros >= 11 or "@" in pergunta:
                print("Dados pessoais identificados! Não informe CPF, telefone ou e-mail.")
                continue

            tentativas += 1
            resultados = self.base.buscar(pergunta)

            if not resultados or resultados[0][0] < 3:
                print("Tenta outra palavra")
                ajudou = False
                orientacao = None
                encontrou = False
            else:
                pontos, orientacao = resultados[0]
                encontrou = True
                if pontos >= 6:
                    print(f"Confiança alta: {pontos} pontos")
                else:
                    print(f"Confiança média: {pontos} pontos")
                orientacao.exibir()
                print()
                print("Outras orientações:")

                for pontos_alt, alternativa in resultados[1:3]:
                    if pontos_alt >=3:
                        print(f"{alternativa.titulo}:{pontos_alt}")

                while True:
                    resposta = input("ajudou? (s/n):").lower()

                    if resposta == "s":
                        ajudou = True
                        break
                    elif resposta == "n":
                        ajudou = False
                        break
                    else:
                        print("erro")

            tempo = round(time.time() - inicio, 1)

            self.registrar("pergunta",pergunta,orientacao,encontrou,ajudou,tentativas,tempo)
            return

    def navegar(self):
        categorias = self.base.categorias()

        while True:
            print("categoria:")

            for i, categoria in enumerate(categorias, 1):
                print(f"{i}. {categoria}")

            print("Digite [0] para voltar")
            opcao = input("escolha uma categoria: ")

            if opcao == "0":
                return

            if not opcao.isdigit() or int(opcao) < 1 or int(opcao) > len(categorias):
                print("erro")
                continue

            categoria = categorias[int(opcao) - 1]
            orientacoes = self.base.por_categoria(categoria)

            while True:
                print(categoria)

                for i, orientacao in enumerate(orientacoes, 1):
                    print(f"[{i}] {orientacao.titulo}")

                print("Digite [0] para voltar")
                escolha = input("escolha uma orientação: ")

                if escolha == "0":
                    break

                if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(orientacoes):
                    print("erro")
                    continue

                inicio = time.time()
                orientacao = orientacoes[int(escolha) - 1]
                orientacao.exibir()

                while True:
                    resposta = input("ajudou? (s/n): ").lower()

                    if resposta == "s":
                        ajudou = True
                        break

                    elif resposta == "n":
                        ajudou = False
                        break

                    else:
                        print("erro")

                tempo = round(time.time() - inicio, 1)

                self.registrar("categoria", "", orientacao,True, ajudou, 1, tempo)


    def registrar(self, origem, pergunta, orientacao, encontrou, ajudou, tentativas, tempo):
        registro = {
            "data": datetime.now().isoformat(),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": orientacao.id if orientacao else None,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo
        }

        self.historico.append(registro)

        self.db_path.write_text(
            json.dumps(self.historico, ensure_ascii=False, indent=2),encoding="utf-8")

        print("registrado!")

    def indicadores(self):
        total = len(self.historico)

        if total == 0:
            print("Nenhum atendimento registrado")
            return

        encontrados = 0
        ajudaram = 0
        tempo_total = 0
        tentativas_total = 0

        print("\nDúvidas sem solução:")

        for registro in self.historico:
            if registro["encontrou"]:
                encontrados += 1

            if registro["ajudou"]:
                ajudaram += 1
            else:
                print(f'- {registro["pergunta"]}')

            tempo_total += registro["tempo_segundos"]
            tentativas_total += registro["tentativas"]

        print("\n=== INDICADORES ===")
        print(f"Total de atendimentos: {total}")
        print(f"Respostas encontradas: {encontrados / total * 100:.1f}%")
        print(f"Taxa de acerto: {ajudaram / total * 100:.1f}%")
        print(f"Tempo médio: {tempo_total / total:.1f} segundos")
        print(f"Tentativas por atendimento: {tentativas_total / total:.1f}")

    def exportar_csv(self):
        if not self.historico:
            print("Nenhum atendimento para exportar")
            return

        try:
            with self.csv_path.open("w", newline="", encoding="utf-8") as arquivo:
                writer = csv.DictWriter(arquivo, self.historico[0].keys())
                writer.writeheader()

                for registro in self.historico:
                    writer.writerow(registro)

            print(f"Atendimentos exportados para {self.csv_path}")

        except PermissionError:
            print("Erro")

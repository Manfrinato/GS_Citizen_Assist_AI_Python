from pathlib import Path
import json
from orientacao import Orientacao

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}


def normalizar(texto):
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "

class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = Path(__file__).resolve().parent / caminho
        self.orientacoes = []

    def carregar(self):
        if not self.caminho.exists():
            print("Caminho nao existe")
            return
        try:
            dados = json.loads(self.caminho.read_text(encoding="utf-8"))
            for item in dados:
                orientacao = Orientacao(**item)
                self.orientacoes.append(orientacao)
        except (json.decoder.JSONDecodeError, TypeError,KeyError, ValueError):
            print("erro ao carregar")
            self.orientacoes = []

    def categorias(self):
        categorias = []
        for orientacao in self.orientacoes:
            if orientacao.categoria not in categorias:
                categorias.append(orientacao.categoria)
        return categorias

    def por_categoria(self, categoria):
        resultado = []
        for orientacao in self.orientacoes:
            if orientacao.categoria == categoria:
                resultado.append(orientacao)
        return resultado

    def pontuar(self, pergunta, orientacao):
        pontos = 0
        pergunta = normalizar(pergunta)
        titulo = normalizar(orientacao.titulo)

        for chave in orientacao.palavras_chave:
            chave = normalizar(chave)
            if chave in pergunta:
                pontos += 3
        for palavras in pergunta.split():
            if len(palavras) >= 4:
                if f"{palavras} " in titulo:
                    pontos += 1
        return pontos

    def buscar(self, pergunta):
        resultado = []
        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta, orientacao)
            if pontos > 0:
                resultado.append((pontos, orientacao))
        resultado.sort(key=lambda item: item[0], reverse=True)

        return resultado

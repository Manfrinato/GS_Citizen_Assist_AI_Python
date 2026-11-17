class Orientacao:
    def __init__(self, id, categoria,titulo,palavras_chave,resposta,documentos,onde,fonte,verificado_em):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave
        self.resposta = resposta
        self.documentos = documentos
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em

    def exibir(self):
        print("id:", self.id)
        print("categoria:", self.categoria)
        print("titulo:", self.titulo)
        print("palavras_chave:", self.palavras_chave)
        print("resposta:", self.resposta)
        print("documentos:", self.documentos)
        print("onde:", self.onde)
        print("fonte:", self.fonte)
        print("verificado_em:", self.verificado_em)
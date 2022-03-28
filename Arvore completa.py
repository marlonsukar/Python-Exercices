class No():
    def __init__(self, valor):
        self.valor = valor
        self.direita = None
        self.esquerda = None
        self.pai = None

    def __str__(self):
        return str(self.valor)

    def is_folha(self):
        return self.direita is None and self.esquerda is None


class ArvoreBinariaBusca():
    def __init__(self):
        self.raiz = None
        self.total = 0

    def _min_max(self, valor, max=False):
        perc = self.buscar(valor)
        if perc is not None:
            atual = None
            while perc is not None:
                atual = perc
                if max:
                    perc = perc.direita
                else:
                    perc = perc.esquerda
            return atual

    def min(self, valor):
        return self._min_max(valor)

    def max(self, valor):
        return self._min_max(valor, True)

    def buscar(self, valor):
        perc = self.raiz
        while perc is not None:
            if valor == perc.valor:
                break
            elif valor > perc.valor:
                perc = perc.direita
            else:
                perc = perc.esquerda
        return perc

    # foi convertido para um pai no nó (duplamente encadeada)
    def _pai(self, no_perc):
        perc = self.raiz
        atual = None
        while perc != no_perc:
            atual = perc
            if no_perc.valor > perc.valor:
                perc = perc.direita
            else:
                perc = perc.esquerda
        return atual

    def add(self, valor):
        no = No(valor)
        if self.raiz is None:
            self.raiz = no
        else:
            perc = self.raiz
            atual = None
            while perc != None:
                atual = perc
                if perc.valor == valor:
                    raise ('O valor já existe na árvore')
                elif valor > perc.valor:
                    perc = perc.direita
                else:
                    perc = perc.esquerda
            if valor > atual.valor:
                atual.direita = no
            else:
                atual.esquerda = no
            no.pai = atual
        perc_pai = no.pai
        print('-->NO {}--'.format(no.valor), self.__fator(no))
        while perc_pai is not None:
            fator = self.__fator(perc_pai)
            print('-->', perc_pai.valor, self.__fator(perc_pai))
            if fator not in [-1, 0, 1]:
                self.rotacao(perc_pai)
            perc_pai = perc_pai.pai
        print('------------')
        self.total += 1

    def rotacionar_direita(self, raiz_atual, nova_raiz):
        print("rotacionar direita", raiz_atual, nova_raiz)
        if self.raiz.valor == raiz_atual.valor:
            self.raiz = nova_raiz
        raiz_atual.esquerda = nova_raiz.direita
        nova_raiz.direita = raiz_atual

    def rotacionar_esquerda(self, raiz_atual, nova_raiz):
        print("rotacionar_esquerda", raiz_atual, nova_raiz)
        if self.raiz.valor == raiz_atual.valor:
            self.raiz = nova_raiz
        raiz_atual.direita = nova_raiz.esquerda
        nova_raiz.esquerda = raiz_atual

    def rotacao(self, atual):
        print('VAMOS ROTACIONAR', atual)
        fator = self.__fator(atual)
        if fator < 0:
            print('verificar o filho da esquerda')
            fator_esqueda = self.__fator(atual.esquerda)
            if fator < 0 and fator_esqueda < 0: #pode remover essa primeira parte do and
               # print("Atual: " + str(atual.valor) + " Atual.esquerda: " + str(atual.esquerda.valor))
                self.rotacionar_direita(atual, atual.esquerda)
            if fator < 0 and fator_esqueda > 0:
                self.rotacionar_esquerda(atual.esquerda, atual.esquerda.direita)
                self.rotacionar_direita(atual, atual.esquerda)

        if fator > 0:
            print('verificar o filho da direita')
            fator_direita = self.__fator(atual.direita)
            if fator > 0 and fator_direita > 0:
                self.rotacionar_esquerda(atual, atual.direita)
            if fator > 0 and fator_direita < 0:
                self.rotacionar_direita(atual.esquerda, atual.esquerda.direita)
                self.rotacionar_esquerda(atual, atual.esquerda)
            # veriricar direita

    def sucessor(self, raiz):
        if raiz.direita is not None:
            return self.min(raiz.direita.valor)
        return None

    def predecessor(self, raiz):
        if raiz.esquerda is not None:
            return self.max(raiz.esquerda.valor)
        return None

    def _recortar(self, no):
        pai = no.pai
        if no.is_folha():
            if pai.valor > no.valor:
                pai.esquerda = None
            else:
                pai.direita = None
            self.total = self.total - 1
        else:
            sucessor = self.sucessor(no)
            predecessor = self.predecessor(no)
            if sucessor is not None:
                if self.raiz.valor == no.valor:
                    sucessor.esquerda = self.raiz.esquerda
                    sucessor.direita = self.raiz.direita
                    self.raiz = sucessor
                    if sucessor.pai.valor > sucessor.valor:
                        sucessor.pai.esquerda = None
                    else:
                        sucessor.pai.direita = None
                    self.total = self.total - 1
                else:
                    suc_pai = sucessor.pai
                    sucessor.esquerda = no.esquerda
                    if no.direita.valor != sucessor.valor:
                        sucessor.direita = no.direita
                    if suc_pai.valor > sucessor.valor:
                        suc_pai.esquerda = None
                    else:
                        suc_pai.direita = None
                    no.direita = None
                    no.esquerda = None
                    if no.valor < pai.valor:
                        pai.esquerda = sucessor
                    else:
                        pai.direita = sucessor
                    self.total = self.total - 1
            else:
                if self.raiz.valor == no.valor:
                    predecessor.esquerda = self.raiz.esquerda
                    predecessor.direita = self.raiz.direita
                    self.raiz = predecessor
                    if predecessor.pai.valor > predecessor.valor:
                        predecessor.pai.esquerda = None
                    else:
                        predecessor.pai.direita = None
                    self.total = self.total - 1
                else:
                    pre_pai = predecessor.pai
                    predecessor.direita = no.direita
                    if no.esquerda.valor != predecessor.valor:
                        predecessor.esquerda = no.esquerda
                    if pre_pai.valor > no.valor:
                        pre_pai.esquerda = None
                    else:
                        pre_pai.direita = None
                    no.direita = None
                    no.esquerda = None
                    if no.valor < pai.valor:
                        pai.esquerda = predecessor
                    else:
                        pai.direita = predecessor
                    self.total = self.total - 1

            # 1 - Encontrar o sucessor se não existir, pegar o predecessor
            # 2- Existe o sucessor
            # 2.1 - pegar a esquerda do sucessor
            # 2.2 - Apontar a esquerda do sucessor para a esquerda o que vai remover(no)
            # 2.3 - Apontar a direita do sucessor para a direta do no, verificar se a direita do no é diferente do suces
            # sor, se for diferente, aponta
            # 2.4 - pegar o pai do sucessor
            # 2.5 - apontar para None esquerda ou direita do pai (Verificar)
            # 2.6 - pegar a esquerda e difeira do no e aponta para NONE
            # 2.7 - Pega o pai do no e aponta para o sucessor (direita
            # 2.8 se o no for rais, self.raiz aponta para o sucessor

    def imprimir(self, order=None):
        lista = []

        def em_ordem(perc):
            if not perc:
                return
            # Visita filho da esquerda.
            em_ordem(perc.esquerda)
            # Visita nodo corrente.
            lista.append(perc.valor)
            # Visita filho da direita.
            em_ordem(perc.direita)

        def pre_ordem(perc):
            if not perc:
                return
            lista.append(perc.valor)
            em_ordem(perc.direita)
            em_ordem(perc.esquerda)

        def pos_ordem(perc):
            if not perc:
                return
            em_ordem(perc.esquerda)
            em_ordem(perc.direita)
            lista.append(perc.valor)

        if order == 'IN':
            em_ordem(self.raiz)
        elif order == 'PRE':
            pre_ordem(self.raiz)
        else:
            pos_ordem(self.raiz)
        return lista

    def remover(self, valor):
        # verificar se o no existe
        perc = self.buscar(valor)
        if perc is not None:
            # verificar se o no é uma folha
            self._recortar(perc)
            return True
        return False

    def altura(self, valor):
        perc = self.buscar(valor)
        return self.__altura(perc)

    def __altura(self, prox):
        if prox == None:
            return 0
        elif prox.esquerda == None and prox.direita == None:
            return 1
        else:
            if self.__altura(prox.esquerda) > self.__altura(prox.direita):
                return 1 + self.__altura(prox.esquerda)
            return 1 + self.__altura(prox.direita)

    def fator(self, valor):
        perc = self.buscar(valor)
        if perc:
            esq = self.__altura(perc.esquerda)
            direita = self.__altura(perc.direita)
            return direita - esq
        return None

    def __fator(self, atual):
        if atual:
            esq = self.__altura(atual.esquerda)
            direita = self.__altura(atual.direita)
            return direita - esq
        return None


arvore = ArvoreBinariaBusca()
arvore.add(10)
print('tamanho', arvore.total)
arvore.add(15)
arvore.add(20)
arvore.add(30)

print('***********')
# print(arvore.altura(17))
# print(arvore.altura(15))
# print(arvore.altura(25))
# print(arvore.fator(20))
print(arvore.fator(20))
print(arvore.fator(15))
print(arvore.fator(10))

# arvore.add(10)
# arvore.add(5)
# arvore.add(20)
# arvore.add(18)
# print('tamanho', arvore.total)
# print('altura', arvore.altura(20))
# print('Fator', arvore.fator_rotacao(20))

# print(arvore.buscar(15))
# print(arvore.min(23))
# print(arvore.max(23))
# arvore.remover(15)
# arvore.remover(23)

print('tamanho', arvore.total)

print(arvore.imprimir())
import random #importa a biblioteca de criação de números aleatorios

class Tabuleiro: #Classe do tabuleiro
  def __init__(self):
    palavras = [] #lista de palavras possiveis
    f = open("palavras.txt", "r")
    for linha in f: #For para ler linha por linha o arquivo
      palavras.append(linha.upper()[0:5]) #Le cada palavra no arquivo, menos o \n
    f.close()
    self.total = tuple(palavras) #transforma a lista em tupla
    i = random.randint(0, len(palavras)) #escolha uma palavra aleatoria
    self.atual = str(palavras[i])
    print(self.atual)
  
  def verifica(self, palavra): #função para verificar se o usuario acertou ou não a palavra
    if palavra == self.atual: #Verifica primeiro se a palavra é a que devia ser descoberta
      return tuple((3, 3, 3, 3, 3)), False #Retorna a tupla inteira como sucesso
    if palavra in self.total : #caso não for, procura a palavra na tupla de palavras possiveis
      #Variaveis para verificar os acertos
      aux = [True, True, True, True, True] #Essa lista é para que quando tenha letras repetidas, saiba se tem ou não na palavra secreta
      #Exemplo: Palavra = Linda, Usuario = Gamar. O segundo A de gamar vai aparecer como errado, pois a posição de A em aux ja foi usada, que no caso é a 2
      acertos = [0, 0, 0, 0, 0] #Os acertos começam com 0, ou seja, nenhum
      i = 0
      while i < len(palavra): #While que percorre uma letra por vez da palavra
        if palavra[i] == self.atual[i]: #Caso a posição seja correta o valor do acerto é 3
          acertos[i] = 3
          aux[i] = False
        else:
          for y, _ in enumerate(self.atual): #for que percorre cada letra da palavra secreta
            if palavra[i] == self.atual[y] and aux[y] == True: #Se a letra existir na palavra e nenhuma outra letra igual tenha aparecido antes
              acertos[i] = 2
              aux[y] = False #Tendo uma letra alocada, a posição vira false
              break #Para o loop do for, pois a letra ja foi encontrada na palavra
        i += 1
      return tuple(acertos), False #Retorna a quantidade de acertos
    return tuple((1, 1, 1, 1, 1)), True #Logo a flag é acionada e o jogador escreve outra palavra
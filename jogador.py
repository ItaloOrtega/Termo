from tkinter import *
class Jogador: #classe jogador
  def __init__(self, dic): #Criação da classe
    self.letras = dic #Recebe o dicionario enviado e aloca no objeto
    self.tentativas = 1 #Número de tentativas possiveis do usuario
  
  def att(self, palavra, resultado): #Função para atualizar as letras usadas e as tentativas
    i = 0
    while i < 5: #Percorre as ultimas letras utilizadas
       #Se a letra que foi utilizadas agora, não ter sido ainda usada, ou ja ter sido mas não na posição correta
      if self.letras["btt_"+str(palavra[i])].cget('bg') == "#CCCCCC" or self.letras["btt_"+str(palavra[i])].cget('bg') == "#FFFF00":
        if resultado[i] == 3: #Se a letra ja foi usada mas na posição errada...
          self.letras["btt_"+str(palavra[i])].config(bg="#66CC00") #Ela é atualizada para verde, ou seja, o usuario colocou em sua posição devida
        else: #Senão ela vai ser um erro ou um acerto na posição errada
          if self.letras["btt_"+str(palavra[i])].cget('bg') == "#CCCCCC" and resultado[i] == 2: #posição errada
            self.letras["btt_"+str(palavra[i])].config(bg="#FFFF00")
          elif resultado[i] == 0 and self.letras["btt_"+str(palavra[i])].cget('bg') == "#CCCCCC": #Erro
            self.letras["btt_"+str(palavra[i])].config(bg="#000000", fg="#FFFFFF")
      i += 1
    self.tentativas += 1 #Aumenta as tentativas em 1
    return self.letras
#Importa o Tkinter, que faz a GUI, matplotlib, que faz os gráficos, e as classes tabuleiro e jogador.
from tkinter import *
import matplotlib.pyplot as plt
from tabuleiro import *
from jogador import *
#Tupla da sequencia do teclado das letras
alfabeto = ('Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M')
linha = 0
play = True
#Criação das variaveis de botão selecionado e de tabuleiro vazias
selecionado = ""
board = "" 
user = Jogador({}) #Usuario da aplicação
resultado = () #Tupla dos acertos das letras da palavra
flag = True #Variavel de Flag de erro, que é desativada somente se uma palavra escrita é valida
btt_ent = {} #Dicionario dos botões de entrada de dados
btt_alf = {} #Dicionario dos botões de alfabeto
pontuacao = {} #Dicionario da pontuação do usuário
try: #Tenta ler o arquivo de pontuação do usuário
  f = open("pontos.bat", "r")
  for linha in f: #For para ler linha por linha o arquivo
    if linha[0] == 'x': #Caso tenha um x, entra nesse gif para colocar outra caractere
      pontuacao["✖ "] = int(linha[2:int(len(linha))])
    else: #Senão é uma pontuação entre 1 e 6
      pontuacao[linha[0]] = int(linha[2:int(len(linha))])
  f.close() #Fecha o arquivo
except: #Não possuindo ele cria uma pontuação zerada
  pontuacao["✖ "] = 0 #Erro do usuario
  for x in range(6,0,-1):
    pontuacao[str(x)] = 0
tela = Tk() #Tela principal
img = PhotoImage(file = "Icon.png") #Coloca a imagem como o icone da pagina
tela.iconphoto(False, img)
tela.configure(bg= "#CCCCCC")
tela.title("Termo Python")
#Largura e altura da tela
larg = 500
alt = 600
#Calcula as dimensões da tela que esta sendo usado pelo usuario
larg_s = tela.winfo_screenwidth() # largura da tela do usuario
alt_s = tela.winfo_screenheight() # altura da tela do usuario
#calcaula as coordenadas para mostrar a tela da aplicação no meio do monitor
a = (larg_s/2) - (larg/2)
b = (alt_s/2) - (alt/2)
tela.geometry('%dx%d+%d+%d' % (larg, alt, a, b-50))
tela.resizable(False, False) #Desabilita a redimensão da janela

def sair(): #Função que salva a pontuação do usuário e sai da aplicação
  global pontuacao
  f = open("pontos.bat", "w")
  linha = "x="+str(pontuacao["✖ "])+"\n"
  f.write(linha)
  for x in range(6,0,-1):
    linha = str(x)+'='+str(pontuacao[str(x)])+"\n"
    f.write(linha)
  f.close()
  quit()

def final(): #Função de quando o jogo é finalizado, para jogar novamente ou não
  global jogar, a, b, img
  pop_up = Toplevel()
  pop_up.iconphoto(False, img)
  pop_up.title("Jogar Novamente?")
  pop_up.geometry('%dx%d+%d+%d' % (310, 175, a+70, b+100)) #Aloca a nova tela, para que mostre o resultado do usuario
  pop_up.geometry("310x175") #Coloca o tamanho da tela como 310x175 pixels
  pop_up.resizable(False, False) #Desabilita a redimensão da janela
  pop_up.configure(bg= "#CCCCCC")
  pop_up.protocol("WM_DELETE_WINDOW", quit) #Coloca o X da janela para sair da aplicação toda
  lbl_pop = Label(pop_up, text="Deseja Jogar Novamente?", bg= "#3399FF", fg="#FFFFFF", font= "Calibri 15")
  lbl_pop.grid(row=0, column=0, columnspan=20)
  #Labels para melhor visualização dos botões
  lbl_aux1 = Label(pop_up, text="    ", bg= "#CCCCCC",font= "Calibri 15")
  lbl_aux1.grid(row=1, column=0, columnspan=20)
  lbl_aux2 = Label(pop_up, text="    ", bg= "#CCCCCC",font= "Calibri 15")
  lbl_aux2.grid(row=2, column=0)
  lbl_aux3 = Label(pop_up, text="    ", bg= "#CCCCCC",font= "Calibri 15")
  lbl_aux3.grid(row=2, column=2)
  lbl_aux4 = Label(pop_up, text="    ", bg= "#CCCCCC",font= "Calibri 15")
  lbl_aux4.grid(row=2, column=4)
  #Botões de resposta do usuário
  btt_sim = Button(pop_up, text='✓', padx=35, pady=25, bg="#66CC33", fg="#000000",command=lambda:again(pop_up), font= "Calibri 35")
  btt_nao = Button(pop_up, text='✖',padx=35, pady=25, bg="#CC0000", fg="#000000", command=sair, font= "Calibri 35")
  btt_sim.grid(row=2, column= 1)
  btt_nao.grid(row=2, column= 3)

def ajuda(): #Função de ajuda, que mostra como o jogo funciona
  global a, b, img
  pop_up = Toplevel()
  img = PhotoImage(file = "Icon.png") #Coloca a imagem como o icone da pagina
  pop_up.iconphoto(False, img)
  pop_up.title("Ajuda")
  pop_up.geometry('%dx%d+%d+%d' % (310, 175, a+70, b+100)) #Aloca a nova tela
  pop_up.geometry("550x280")
  pop_up.resizable(False, False) #Desabilita a redimensão da janela
  #Definição das labels e dos botões para exemplificar o jogo
  lbl_pop = Label(pop_up, text="Como Jogar", bg= "#3399FF", fg="#FFFFFF", font= "Calibri 10")
  lbl_pop.grid(row=0, column=0, columnspan=20)
  lbl_def = Label(pop_up, text="Descubra a palavra certa em 6 tentativas."
  "\nDepois de cada tentativa, as letras mostram o quão perto você está da solução.", fg="#000000", font= "Calibri 10")
  lbl_def.grid(row=2, column=0, columnspan=20)
  #Labels vazias para melhor visualização do conteudo
  lbls_aux = {}
  btts = {}
  for x in range(1,10,+2):
    lbls_aux["lbl_aux"+str(x)] = Label(pop_up, text="    ",font= "Calibri 5")
    lbls_aux["lbl_aux"+str(x)].grid(row=x, column=0, columnspan=20)
    if x != 9 and x>1: #Cria os botões de exemplo
      btts["btt_"+str(x)] = Button(pop_up, text="A", padx=5,pady=5, fg="#000000")
      btts["btt_"+str(x)].grid(row=x+1, column=1)
  lbl_aux6 = Label(pop_up, text="    ",font= "Calibri 10")
  lbl_aux6.grid(row=11, column=3)
  lbl_aux7 = Label(pop_up, text="    ",font= "Calibri 10")
  lbl_aux7.grid(row=11, column=0)
  btts["btt_3"].config(bg="#66CC00")
  btts["btt_5"].config(bg="#FFFF00")
  btts["btt_7"].config(bg="#000000", fg="#FFFFFF")
  #Labels de explicação
  lbl_verde = Label(pop_up, text="Verde significa que a letra faz parte da palavra e está na posição correta.", fg="#000000", font= "Calibri 10")
  lbl_verde.grid(row=4, column=2)
  lbl_amar = Label(pop_up, text="Amarelo significa que a letra faz parte da palavra, mas em outra posição.", fg="#000000", font= "Calibri 10")
  lbl_amar.grid(row=6, column=2)
  lbl_preto = Label(pop_up, text="Preto significa que a letra não faz parte da palavra.", fg="#000000", font= "Calibri 10")
  lbl_preto.grid(row=8, column=2)
  lbl_rep = Label(pop_up, text="As palavras podem possuir letras repetidas!", fg="#000000", font= "Calibri 10")
  lbl_rep.grid(row=10, column=0, columnspan=20)

  pop_up.bind('<Escape>',lambda event:pop_up.destroy()) #Aloca a tecla Esc para sair do pop up de ajuda


def graf(disc): #Função que mostra graficamente os acertos do usuário
  global a, b
  #Listas para a montagem do gráfico
  aux1 = []
  aux2 = []
  maxx = 0 #Valor máximo de acertos do gráfico
  for x,y in disc.items(): #Aloca os valores do dicionario nas listas
   aux1.append(x)
   aux2.append(y)
   if y > maxx: #Caso tenha um valor maior do que o atual
     maxx = y
  plt.rcParams['toolbar'] = 'None' #Desliga a toolbar do gráfico
  plt.figure("Placar") #Texto da Janela
  plt.barh(aux1,aux2) #Cria o grafico em barras
  plt.xlim(0, maxx+5) #Coloca o limite do eixo X do gráfico
  plt.title("Distribuição de Tentativas", fontweight='bold') #Coloca o titulo
  plt.axes().get_xaxis().set_visible(False) #Desativa os valores que aparecem abaixo do eixo X
  for i, v in enumerate(aux2): #Coloca os valores de cada barra no grafico
    plt.text(v + 0.5, i - 0.085, str(v), color='blue', fontweight='bold')
  plt.show() #Mostra o gráfico


def criar(): #Função que cria todos os dados necessarios para ser possivel a aplicação
  global play, linha, selecionado, board, resultado, user, pontuacao
  linha = 0 #Linha em que o usuario está
  selecionado = linha*5 #Botão atual selecionado do jogo
  board = Tabuleiro() #Cria o tabuleiro, ou seja, escolhe uma nova palavra
  resultado = (0, 0, 0, 0, 0) # Os acertos de cada letra da palavra do usuario
  user.tentativas = 1 #Qtd de tentativas que o usuario possui
  play = False #Variavel de inicio da aplicação

  #Criação dos botões de entrada dos dados
  i = 2 #Começa a alocação deles na linha 2 e na coluna 3
  j = 3
  for x in range(0,30): #Vao ser criados 30 botões
    btt_ent["btt_"+str(x)] = cBtt(x) #Adiciona o botão criado no dicionario
    if x%5 == 0: #Quando chegar a um multiplo de 5 volta pro começo das colunas e passa para proxima linha
      i += 1
      j = 3
    btt_ent["btt_"+str(x)].grid(row=i, column=j) #Aloca no grid o botão
    j +=1
  #Label para separar os botões de entrada dos botões de alfabeto
  lble4 = Label(tela, text="  ", bg= "#CCCCCC")
  lble4.grid(row=9, column=0, columnspan=10)

  #Criação dos botões do alfabeto
  i = 10
  j = 1
  for y, x in enumerate(alfabeto):
    btt_alf["btt_"+x] = cBttA(y)
    if x == 'A' or x == 'Z': #Quando for A ou Z, significa que foi ira começar uma nova linha
      i += 1 #Atualiza a linha, somando ela +1
      j = 1 #E retorna as colunas para 1
    btt_alf["btt_"+x].grid(row=i,column=j)
    j += 1
  user.letras = btt_alf


def limpar(): #Função que limpa a linha atual de botões de entrada
  global selecionado
  for x in range((linha*5),(linha*5)+5):
    btt_ent["btt_"+str(x)].config(text="  ")
  selecionado = linha*5 #Retorna pro primeiro botão da linha


def tecla(e): #Função que pega a tecla digitada no teclado e faz uma função devida
  if e.char.upper() in alfabeto: #Se for uma letra ela chama a função adicionar com o valor dela
    adicionar(e.char.upper())
  else: #Não sendo uma letra
    if e.keysym == 'Return' or e.keysym == 'KP_Enter': #Se for um dos enters, vai para printar
      verificar()
    elif e.keysym == 'Delete' or e.keysym == 'BackSpace':
      limpar()


def cBttA(n): #Função que cria botões de alfabeto, que inserem letras nos botões de entrada
  btt = Button(tela,text=str(alfabeto[n]), padx=15, pady=15, bg="#CCCCCC", fg="#000000")
  btt.config(command= lambda:adicionar(alfabeto[n]))
  return btt


def cBtt(valor): #Função que cria os botões de entrada
  bt = Button(tela,text="  ", padx=15, pady=15, bg="#FFFFFF", fg="#000000")
  if valor > 4: #Caso o valor ser maior que 4, significa que são botões fora da primeira linha...
    bt.config(state='disable') #logo tem que estar desativados
  bt.config(command= lambda:selecionar(valor))
  return bt


def selecionar(n): #Função que seleciona o botão a ser inserido
  global selecionado
  selecionado = int(n)


def adicionar(c): #Funçaõ que aloca uma letra no botão
  global selecionado, btt_ent
  try:
    btt_ent["btt_"+str(selecionado)].config(text=str(c))
    if (selecionado+1)%5 == 0: #Caso seja o ultimo botão da linha, o selecionado aponta pra nada
      selecionado = ""
    else: #Caso contrario ele vai para o próximo botão
      selecionado += 1
  except:
    pass


def again(aux): #Função que fecha o pop up de jogar novamente e cria denovo o tabuleiro e o jogador
  aux.destroy()
  lbl_erro.config(text="      ", bg= "#CCCCCC") #Limpa a label de erro/acerto
  criar()


def verificar(): #Função que verifica a palavra escrita e os acertos das letras
  global resultado, flag, btt_alf, btt_ent, linha, selecionado, board
  lbl_erro.config(text="      ", bg= "#CCCCCC") #Coloca a label de erro como vazia
  palavra = "" #Cria a variavel palavra vazia
  for x in range((linha*5),(linha*5)+5): #For para colocar cada letra de cada botão de entrada na variavel palavra
    palavra = palavra + str(btt_ent["btt_"+str(x)].cget("text"))
  resultado, flag = board.verifica(palavra) #Verifica se essa palavra é valido, e se for qual foi o qtd de acertos
  if flag == True: #Caso a palavra não seja valida o jogador deve colocar uma nova
    lbl_erro.config(text="Palavra Invalida!", bg= "#3399FF", fg="#FFFFFF", font= "Calibri 15")
    selecionado = linha*5 #Coloca como selecionado o primeiro botão da linha
  else: #Caso tenha sido uma palavra válida
    btt_alf=user.att(palavra, resultado) #Atualiza os botões alfabeto, os botões que representam o teclado
    j = 0 #J é a posição atual da tupla resultado
    for x in range((linha*5),(linha*5)+5): #For que desabilita os botões que foram usados para criar a palavra atual
      btt_ent["btt_"+str(x)].config(state='disabled')
      if resultado[j] == 0: #Caso a letra tenha sido um erro, botão fica preto
        btt_ent["btt_"+str(x)].config(bg="#000000", fg="#FFFFFF")
      elif resultado[j] == 2: #Caso seja um acerto na posição errada, botão fica amarelo
        btt_ent["btt_"+str(x)].config(bg="#FFFF00")
      else: #Senão ele fica verde
        btt_ent["btt_"+str(x)].config(bg="#66CC00")
      j += 1
    if resultado == (3,3,3,3,3): #Caso tenha acertado a palavra, mostra a mensagem de sucesso e chama a função final
      lbl_erro.config(text="Acertou!", bg= "#3399FF", fg="#FFFFFF", font= "Calibri 15")
      pontuacao[str(user.tentativas-1)] += 1
      final()
    elif user.tentativas == 7: #Caso tenha acabado as chances e não ter ganhado mostra a palavra e chama a função final
      lbl_erro.config(text=f"Perdeu!\nA palavra era: {board.atual}", bg= "#3399FF", fg="#FFFFFF", font= "Calibri 15")
      pontuacao["✖ "] += 1
      final()
    else: #Caso ainda tenha chances e não tenha acertado ainda
      linha += 1 #Vai para a proxima linha de botões
      for x in range((linha*5),(linha*5)+5): #Aciona a proxima linha de botões
        btt_ent["btt_"+str(x)].config(state='normal')
      selecionado = linha*5 #Coloca o primeiro botão da nova linha como o primeiro 


if play == True: #Caso seja o inicio da aplicação, cria as variaveis necessárias
  criar()

# Labels para uma melhor visualização do board
lble1 = Label(tela, text="      ", bg= "#CCCCCC")
lble1.grid(row=1, column=0, columnspan=20)
lbl_erro = Label(tela, text="      ", bg= "#CCCCCC")
lbl_erro.grid(row=1, column=0, columnspan=10)
lble2 = Label(tela, text="  ", bg= "#CCCCCC")
lble2.grid(row=2, column=0)
lble3 = Label(tela, text="  ", bg= "#CCCCCC")
lble3.grid(row=2, column=11)

#Criação e alocação do botão de ajuda
btt_help = Button(tela, text="?", padx=5,pady=5, command=ajuda, bg= "#CCCCCC")
btt_help.grid(row=3, column=10)

img_graph = PhotoImage(file="grafico_icon.png") #Imagem que possui o icone de grafico
btt_graph = Button(tela, image=img_graph,padx=5, pady=5, command= lambda:graf(pontuacao)) #Cria o botão com a imagem
btt_graph.grid(row= 2, column=10)

#Criação e alocação dos botões de limpeza e enter
btt_clear = Button(tela,text="⌫", padx=15, pady=15, command= limpar, bg= "#CCCCCC")
btt_enter = Button(tela,text="Enter", padx=47, pady=15, command= verificar, font= "Calibri 10", bg= "#CCCCCC")
btt_clear.grid(row=11, column=10)
btt_enter.grid(row=12, column=8, columnspan=20)

#Alocação das teclas do teclado a uma função
tela.bind_all('<Key>', tecla) #liga todas as teclas do teclado a tela e a uma função
tela.protocol("WM_DELETE_WINDOW", sair) #Botão X de saur da aplicação inicia a função sair()
tela.mainloop()

from operator import le
from tkinter import *
from turtle import color
import numpy as np
import math

# Configurações da janela
MAIN_COLOR = '#6260ca'
BG_COLOR = '#303030'
HEIGHT = 900
WIDTH = 1680

root = Tk()
# Tamanho da janela
root.geometry("1920x1080")
# Título da janela
root.title('Mini Blender')
# Cor de fundo da janela
root.configure(background=BG_COLOR)

# Guardar o centro do polígono criado (x, y)
centro = []

# Pontos do polígono criado
poligono = []

# Matriz padrão de rotação
def matrizR(teta):
    return np.array([[math.cos(teta), -math.sin(teta), 0],
                     [math.sin(teta), math.cos(teta), 0],
                     [0, 0, 1]])

# Matriz padrão de escala
def matrizE2d(sx, sy):
    return np.array([[sx, 0, 0], 
                    [0, sy, 0],
                    [0, 0, 1]])

# Matriz padrão de translação
def matrizT2d(tx, ty):
    return np.array([[1, 0, tx],
                     [0, 1, ty],
                     [0, 0, 1]])

def poligono_invalido():
    return not pontos_input.get().isdigit() or len(poligono) < int(pontos_input.get())

# Adicionar o valor 1 para cada ponto do polígono
def adicionar_uns(matriz):
    nova_matriz = []
    for linha in matriz:
        nova_matriz.append(linha + [1])
    return nova_matriz

# Criar um novo polígono na tela
def mostrar_novo_poligono(novo_poligono):
    c.delete("all")
    c.create_polygon(novo_poligono, fill=MAIN_COLOR)
    poligono.clear()
    poligono.extend(novo_poligono)

# Função que retorna o centro do polígono
def calcular_centro(vertices):
     pontos_x = [vertice [0] for vertice in vertices]
     pontos_y = [vertice [1] for vertice in vertices]
     quantidade_vertices = len(vertices)
     x_central = sum(pontos_x) / quantidade_vertices
     y_central = sum(pontos_y) / quantidade_vertices
     return [x_central, y_central]

def escala(sx, sy):
    novo_poligono = []
    poligono_atual = adicionar_uns(poligono)
    poligono_atual = np.array(poligono_atual)
    matriz = matrizE2d(sx, sy)

    # Multiplicar os pontos do polígono com a matriz de escala
    for i in range(len(poligono_atual)):
        [x2, y2, _] = np.matmul(matriz, poligono_atual[i])
        novo_poligono.append([x2, y2])        

    mostrar_novo_poligono(novo_poligono)

def translacao(tx, ty):
    novo_poligono = []
    poligono_atual = adicionar_uns(poligono)
    poligono_atual = np.array(poligono_atual)
    matriz = matrizT2d(tx, ty)
    
    # Multiplicar os pontos do polígono com a matriz de translação
    for i in range(len(poligono_atual)):
        [x2, y2, _] = np.matmul(matriz, poligono_atual[i])
        novo_poligono.append([x2, y2])        

    mostrar_novo_poligono(novo_poligono)

def rotacao(teta):
    matrizR2d = matrizR(teta)
    matrizT2D = matrizT2d(-centro[0], -centro[1])
    poligono_transladado = []
    poligono_rotacionado = []
    novo_poligono = []
    poligono_atual = adicionar_uns(poligono)
    poligono_atual = np.array(poligono_atual)

    # Transladar o polígono para o centro
    for i in range(len(poligono_atual)):
        [x2, y2, _] = np.matmul(matrizT2D, poligono_atual[i])
        poligono_transladado.append([x2, y2, 1])
    
    poligono_transladado = np.array(poligono_transladado)

    # Rotacionar os pontos do polígono
    for i in range(len(poligono_transladado)):
        [x2, y2, _] = np.matmul(matrizR2d, poligono_transladado[i])
        poligono_rotacionado.append([x2, y2, 1])
    
    matrizT2D = matrizT2d(centro[0], centro[1])
    
    # Transladar o polígono para a posição original
    for i in range(len(poligono_rotacionado)):
        [x2, y2, _] = np.matmul(matrizT2D, poligono_rotacionado[i])
        novo_poligono.append([x2, y2])

    mostrar_novo_poligono(novo_poligono)
    
# Função que cria um novo ponto clicado no canvas
def criar_ponto(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    c.create_oval(x1, y1, x2, y2, width=8, outline=MAIN_COLOR)

# Clicar no canvas e criar um polígono
def callback(event):
    if (poligono_invalido()):
        criar_ponto(event)
        poligono.append([event.x, event.y])

    if (len(poligono) == int(pontos_input.get())):
        criar_ponto(event)
        centro.extend(calcular_centro(poligono))
        c.delete("all")
        c.create_polygon(poligono, fill=MAIN_COLOR)

def button_click(number):
    if (number != 1 and poligono_invalido()): return
    
    # Limpar
    if number == 1:
        c.delete("all")
        poligono.clear()
        centro.clear()
    # Rotacionar 45º
    elif number == 2:
        rotacao(math.pi/4)
    # Rotacionar 90º
    elif number == 3:
        rotacao(math.pi/2)
    # Rotacionar 180º
    elif number == 4:
        rotacao(math.pi)
    # Escala 2x
    elif number == 5:
        escala(2, 2)
    # Escala 3x
    elif number == 6:
        escala(3, 3)
    # Escala 3x 4y
    elif number == 7:
        escala(3, 4)
    # Translação para cima
    elif number == 8:
        translacao(0, -10)
    # Translação para direita
    elif number == 9:
        translacao(10, 0)
    # Translação para esquerda
    elif number == 10:
        translacao(-10, 0)
    # Translação para baixo
    elif number == 11:
        translacao(0, 10)

#criando os elementos de interface
frame = Frame(root, bg=BG_COLOR, padx=5, pady=5)
buttons = Frame(root, bg=BG_COLOR, padx=5, pady=5)
c = Canvas(width=WIDTH, height=HEIGHT,bg="white")

# input de pontos
pontos_input = Entry(root, width=50)
pontos_input.insert(0, 4)	
pontos_input.grid(column=1, row=0)

#posicionando os objetos na interface
frame.grid(row=0,column=0, padx=5, pady=5)
buttons.grid(row=1,column=0, padx=5, pady=5)
c.grid(row=1,column=1,padx=5,pady=5)
c.bind("<Button-1>", callback)


#os botões serão criados dentro do frame
myButton1=Button(frame, text='Limpar', width=20, fg='#fff', bg='red', pady=3, command=lambda:button_click(1))
myButton1.pack()

# Botões de rotação
myButton2=Button(buttons, text='Rotacionar 45', fg='#fff', bg='#0096d6', width=20, pady=3, command=lambda:button_click(2))
myButton2.pack()
myButton3=Button(buttons, text='Rotacionar 90', fg='#fff', bg='#0096d6', width=20, pady=3, command=lambda:button_click(3))
myButton3.pack()
myButton4=Button(buttons, text='Rotacionar 180', fg='#fff', bg='#0096d6', width=20, pady=3, command=lambda:button_click(4))
myButton4.pack()

# Botões de escala
myButton5=Button(buttons, text='Escala (2,2)', fg='#fff', bg='#5eba7d', width=20, pady=3, command=lambda:button_click(5))
myButton5.pack()
myButton6=Button(buttons, text='Escala (3,3)', fg='#fff', bg='#5eba7d', width=20, pady=3, command=lambda:button_click(6))
myButton6.pack()
myButton7=Button(buttons, text='Escala (3,4)', fg='#fff', bg='#5eba7d', width=20, pady=3, command=lambda:button_click(7))
myButton7.pack()

# Botões de translação
myButton8=Button(buttons, text='Translação Cima', fg='#fff', bg='#f48225', width=20, pady=3, command=lambda:button_click(8))
myButton8.pack()
myButton9=Button(buttons, text='Translação Direita', fg='#fff', bg='#f48225', width=20, pady=3, command=lambda:button_click(9))
myButton9.pack()
myButton8=Button(buttons, text='Translação Esquerda', fg='#fff', bg='#f48225', width=20, pady=3, command=lambda:button_click(10))
myButton8.pack()
myButton9=Button(buttons, text='Translação Baixo', fg='#fff', bg='#f48225', width=20, pady=3, command=lambda:button_click(11))
myButton9.pack()

root.mainloop()

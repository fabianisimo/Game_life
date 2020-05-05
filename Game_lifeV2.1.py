import pygame
from pygame.locals import *
import sys

colorGris   = (50,50,50) 
colorBlanco = (200,200,200)
colorgrid   = (80,80,80)

colorFondo = colorGris
ancho_px, alto_px = 600, 600
ancho, alto = 40, 40

def dibujaGrilla(donde, color):
    for x in range(1,ancho):
        linea_x = x*ancho_px/ancho
        pygame.draw.line(donde,color,(linea_x,0),(linea_x,alto_px),1)
    for y in range(1,alto):
        linea_y = y*alto_px/alto
        pygame.draw.line(donde,color,(0,linea_y),(ancho_px,linea_y),1)

class cuadro(pygame.sprite.Sprite):
    ##  clase para la celda como unidad y su comportamiento  ##

    def __init__(self,pos,donde,estado = False,start = False,todas = False):                             ## pos es una tupla de coordenadas de celdas (5,3) por ejemplo
        ## ejemplo = cuadro((2,2),ventana,True)
        pygame.sprite.Sprite.__init__(self)
        vecinas = []
        vecinasVivas = 0
        self.start = start
        self.donde = donde
        self.viva = estado
        self.posX = pos[0] * ancho_px/ancho
        self.posY = pos[1] * alto_px/alto

        self.pos = pos
        self.ancho = ancho_px/ancho
        self.alto = alto_px/alto

        if start:
            vecinas = self.__vecinas()
            for v in vecinas:
                if v in todas:
                    vecinasVivas = vecinasVivas+1
        
        if self.viva:
            self.__dibujar()
            sobrevivio = self.pos

        if vecinasVivas > 3:
            self.viva = False
        if vecinasVivas < 2:
            self.viva = False
       # if vecinasVivas == 2:
        #    self.viva = True
        if vecinasVivas == 3:
            self.viva = True

    def __dibujar(self):  ## pinta un cuadrito en la celda
        pygame.draw.rect(self.donde,colorBlanco,(self.posX,self.posY,self.ancho,self.alto))

    def __vecinas(self):  ## entrega una lista con las celdas que rodean
        if self.pos[0] == 0:
            v1x = ancho-1
            v8x = ancho-1
            v7x = ancho-1
        else:
            v1x = self.pos[0] -1
            v8x = self.pos[0] -1
            v7x = self.pos[0] -1
        if self.pos[1] == 0:
            v1y = alto-1
            v2y = alto-1
            v3y = alto-1
        else:
            v1y = self.pos[1] -1
            v2y = self.pos[1] -1
            v3y = self.pos[1] -1
        if self.pos[0] == ancho-1:
            v3x = 0
            v4x = 0
            v5x = 0
        else:
            v3x = self.pos[0] +1
            v4x = self.pos[0] +1
            v5x = self.pos[0] +1
        if self.pos[1] == alto-1:
            v5y = 0
            v6y = 0
            v7y = 0
        else:
            v5y = self.pos[1] +1
            v6y = self.pos[1] +1
            v7y = self.pos[1] +1
        v2x = self.pos[0]
        v6x = self.pos[0]
        v4y = self.pos[1]
        v8y = self.pos[1]       
        vecinas = [(v1x,v1y),(v2x,v2y),(v3x,v3y),(v4x,v4y),(v5x,v5y),(v6x,v6y),(v7x,v7y),(v8x,v8y),]
        return vecinas

    def sobrevivio(self):
        if self.viva:
            return True
        else:
            return False

def grilla():
    grilla = []
    for x in range(ancho):
        for y in range(alto):
            cuadrito = (x,y)
            grilla.append(cuadrito)
    return grilla

def estado_inicial(iniciales,donde):
    ## iniciales será una lista con las seleccionadas por el ususario
    for a in iniciales:
        celda = cuadro(a,donde,True,False)
        
def iteracion(previas,donde,previas2):
    resultado = []
    red = grilla()
    
    for a in red:
        if a in previas:
            celda = cuadro(a,donde,True,True,previas2)
            if celda.sobrevivio():
                resultado.append(a)
        else:
            celda = cuadro(a,donde,False,True,previas2)
            if celda.sobrevivio():
                resultado.append(a)
    return resultado

def limpiar(lista):
    if len(lista)>1:
        for a in range(0,len(lista)-1):
            for b in range (a+1,len(lista)):
                if lista[a] == lista[b]:
                    lista.remove(lista[a])
    return lista

def juego():
    iniciales = []
    previo = []
    start = False
    while True:

        pygame.init()
        ventana = pygame.display.set_mode((ancho_px,alto_px))       ## crea ventana
        pygame.display.set_caption("Game Life_V2.1")                ## le pone titulo
        ventana.fill(colorFondo)                                    ## pinta la ventana
        dibujaGrilla(ventana,colorgrid)                             ## dibuja la red

        for evento in pygame.event.get():               
            if evento.type == QUIT:                     
                pygame.quit()                           
                sys.exit() 
            if evento.type == pygame.KEYDOWN:
                if evento.key == K_SPACE: 
                    start = True
                    print ("Comienzo")
        if pygame.mouse.get_pressed() == (1, 0, 0):                 ## v esta parte agrega las clikeadas 
            click_x = int(pygame.mouse.get_pos()[0]*ancho/ancho_px) ## | a la lista de celdas iniciales
            click_y = int(pygame.mouse.get_pos()[1]*alto/alto_px)   ## |
            posclik = (click_x,click_y)                             ## |
            iniciales.append(posclik)                               ## |  
            iniciales = limpiar(iniciales)                          ## ^

        quitar = []                                                     ## v esta parte quita de las iniciales las precionadas 
        if pygame.mouse.get_pressed() == (0, 0, 1):                     ## | con click derecho
            click_x = int(pygame.mouse.get_pos()[0]*ancho/ancho_px)     ## |
            click_y = int(pygame.mouse.get_pos()[1]*alto/alto_px)       ## |
            posclik = (click_x,click_y)                                 ## |
            quitar.append(posclik)                                      ## |
            quitar = limpiar(quitar)                                    ## |
            if len(quitar) > 0:                                         ## |
                for a in quitar:                                        ## |
                    if a in iniciales:                                  ## |
                        iniciales.remove(a)                             ## ^
        
        if len(iniciales) > 0:                          ## va printeando el estado inicial antes del start
            estado_inicial(iniciales,ventana)           ## incluyendo los click en pantalla
        contador_ciclos = False

        while start:   
            for evento in pygame.event.get():               
                if evento.type == QUIT:                     
                    pygame.quit()                           
                    sys.exit()              
            ventana.fill(colorFondo)            ## refresca la pantalla en cada iteracion
            dibujaGrilla(ventana,colorgrid)

            if contador_ciclos == False:
                resultado = iteracion(iniciales,ventana,iniciales)    ##
                contador_ciclos = True
                print ("en la primera vuelta")
                iteraciones = 0

            else:
                pause = False
                iteraciones = iteraciones +1
                previo = resultado
                resultado = iteracion(previo,ventana,previo)
                print ("iterando: ",iteraciones)
                
                for evento in pygame.event.get():               
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == K_SPACE:
                            pause = True
                        if evento.type == QUIT:                     
                            pygame.quit()                           
                            sys.exit() 
                while pause:
                    for evento in pygame.event.get():               
                        if evento.type == pygame.KEYDOWN:
                            if evento.key == K_SPACE:
                                pause = False 
                        if evento.type == QUIT:                     
                            pygame.quit()                           
                            sys.exit()  
                pygame.time.wait(10)
            pygame.display.update()            
        pygame.display.update() 
        
juego()
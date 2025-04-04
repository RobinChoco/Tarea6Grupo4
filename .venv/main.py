import pygame
import random
import time
import os
from pygame import mixer

# ♥ Iniciamos Pygame
pygame.init()

# ♥ Iniciamos mixer para los canales de disparo
#pygame.mixer.init()
canal_disparo = pygame.mixer.Channel(1)
canal_explosion = pygame.mixer.Channel(2)

# ♥ Definimos el Tamaño de pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Galaxy Survivor 💫")

# ♥ Reloj para controlar los FPS
clock = pygame.time.Clock()

# ♥ Cargamos imágenes (falta sonidos
# y pueden cambiar las imagenes o agregar efectos de explosion)
fondo = pygame.image.load("RecursosTarea/Fondo.png")
naves_img = [pygame.image.load("RecursosTarea/NaveFF.png"),
            pygame.image.load("RecursosTarea/nave4.png"),
            pygame.image.load("RecursosTarea/nave3.png"),
            pygame.image.load("RecursosTarea/nave2.png"),
            pygame.image.load("RecursosTarea/nave1.png")
            ]
meteorito_img = pygame.image.load("RecursosTarea/Meteorito.PNG")
laser_img = pygame.image.load("RecursosTarea/Laser.PNG")
explode = [pygame.image.load(f"RecursosTarea/Explosion/explosion{i}R.png") for i in range(1,5)]
fondo_final = pygame.image.load("RecursosTarea/fondo_final.png")
#Naves para las vidas restantes

#Sonido de Fondo
mixer.music.load("RecursosTarea/inicio.mp3")
mixer.music.play(-1)
mixer.music.set_volume(0.3)

# ♥ Ajustamos tamaños
naves_img = [pygame.transform.scale(img, (90, 90)) for img in naves_img]
meteorito_img = pygame.transform.scale(meteorito_img, (55, 55))
laser_img = pygame.transform.scale(laser_img, (20, 80))



# ♥data del  Jugador
nave_x = 368
nave_y = 500
nave_vel = 2.5  #  Velocidad porque se movia muchos
                # pixeles
nave_img = naves_img[0]
vidas = 5

# ♥ Laser
laser_y = nave_y
laser_vel = 14  #
laser_activo = False
#en el medio de la navecita xD
laser_x = nave_x + (nave_img.get_width() // 2) - (laser_img.get_width() // 2)

# Meteoritos
MAX_METEORITOS = 80
meteoritos_en_pantalla = []
meteoritos_totales = 0
meteoritos_destruidos = 0

# Tandas de meteoritos (para que sea controlado y no salgan de un solo)
#subir de nivel y que cada vez salgan mas
# que se muevan
meteoritos_por_tanda = 5
tiempo_tanda = time.time()

# ♥ Cronómetro
inicio_tiempo = time.time()

# ♥ Fuente de texto
fuente = pygame.font.Font("RecursosTarea/segoe-ui-emoji.ttf", 30)


def dibujar_texto(texto, x, y):
    t = fuente.render(texto, True, (255, 255, 255))
    pantalla.blit(t, (x, y))

def crear_meteorito():
    x = random.randint(0, ANCHO - 55)
    y = random.randint(0, 150)
    vel_x = random.uniform(-0.5, 0.5)  # ♥ SE MUEVEN UN poco lateralmente
    vel_y = random.uniform(0.7, 1.2)   # ♥ que salgan constantemenTE
    return {"x": x, "y": y, "vel_x": vel_x, "vel_y": vel_y}

def hay_colision(obj1_x, obj1_y, obj2_x, obj2_y):
    distancia = ((obj1_x - obj2_x) ** 2 + (obj1_y - obj2_y) ** 2) ** 0.5
    return distancia < 50

def explosion_meteorica(x,y):
    explosion.append({"x": x, "y": y, "frame": 0, "ultimo_frame":0})

# looop
ejecutando = True

explosion=[]

while ejecutando:
    clock.tick(60)
    # 60 por segundos que actualiza
    pantalla.blit(fondo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # ♥ Movimiento
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and nave_x > 0:
        nave_x -= nave_vel
    if teclas[pygame.K_RIGHT] and nave_x < ANCHO - nave_img.get_width():
        nave_x += nave_vel
    if teclas[pygame.K_SPACE] and not laser_activo:
        laser_x = nave_x + (nave_img.get_width() // 2) - (laser_img.get_width() // 2)
        laser_y = nave_y
        laser_activo = True
        sonido_laser = pygame.mixer.Sound("RecursosTarea/laser.wav")
        sonido_laser.set_volume(0.4)
        canal_disparo.play(sonido_laser)

    if laser_activo:
        pantalla.blit(laser_img, (laser_x, laser_y))
        laser_y -= laser_vel
        if laser_y < 0:
            laser_activo = False

    # ♥ Dibujar la nave
    pantalla.blit(nave_img, (nave_x, nave_y))

    # ♥ Generar meteoritos por tandas (una tras otra)
    if time.time() - tiempo_tanda > 2 and meteoritos_totales < MAX_METEORITOS:
        for _ in range(meteoritos_por_tanda):
            if meteoritos_totales < MAX_METEORITOS:
                meteoritos_en_pantalla.append(crear_meteorito())
                meteoritos_totales += 1
        tiempo_tanda = time.time()

    # ♥ Mover y dibujar meteoritos
    for meteorito in meteoritos_en_pantalla[:]:
        meteorito["x"] += meteorito["vel_x"]
        meteorito["y"] += meteorito["vel_y"]  # ♥ Ahora caen hacia abajo

        pantalla.blit(meteorito_img, (meteorito["x"], meteorito["y"]))

        # colisión con nave
        if hay_colision(meteorito["x"], meteorito["y"], nave_x, nave_y):
            sonido_colision_nave = mixer.Sound("RecursosTarea/choque.ogg")
            sonido_colision_nave.play()
            vidas -= 1
            if vidas == 5:
                nave_img = naves_img[0]
            elif vidas == 4:
                nave_img = naves_img[1]
            elif vidas == 3:
                nave_img = naves_img[2]
            elif vidas == 2:
                nave_img = naves_img[3]
            elif vidas == 1:
                nave_img = naves_img[4]

            meteoritos_en_pantalla.remove(meteorito)
            continue

        # colisión con láser
        if laser_activo and hay_colision(meteorito["x"], meteorito["y"], laser_x, laser_y):
            explosion_meteorica(meteorito["x"],meteorito["y"])#explosion de meteorito
            meteoritos_en_pantalla.remove(meteorito)
            sonido_colision_meteorito = pygame.mixer.Sound("RecursosTarea/explosion.mp3")
            sonido_colision_meteorito.set_volume(0.4)
            canal_explosion.play(sonido_colision_meteorito)
            meteoritos_destruidos += 1
            laser_activo = False

        # ♥ Eliminar si sale de la pantalla
        if meteorito["y"] > ALTO:
            meteoritos_en_pantalla.remove(meteorito)

    # ♥ Mostrar texto informativo
    tiempo_actual = time.time() - inicio_tiempo
    dibujar_texto(f"💖 Vidas: {vidas}", 10, 10)
    dibujar_texto(f"💖 Eliminados: {meteoritos_destruidos}", 10, 40)
    dibujar_texto(f"💖 Tiempo: {int(tiempo_actual)}s", 10, 70)

    # ♥ Explosion animada
    vel_explosion = 100
    for expl in explosion[:]:
        if expl["frame"] < len(explode):
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - expl["ultimo_frame"] > vel_explosion:
                expl["frame"] += 1
                expl["ultimo_frame"] = tiempo_actual
            if expl["frame"] < len(explode):
                pantalla.blit(explode[expl["frame"]], (expl["x"], expl["y"]))
        else:
            explosion.remove(expl)


    pygame.display.update()

    # del juego
    if vidas <= 0 or meteoritos_destruidos >= MAX_METEORITOS:
        pantalla.blit(fondo_final, (0, 0))
        dibujar_texto("💥 ¡Fin del Juego! 💥", 300, 250)
        dibujar_texto(f"💔 Vidas perdidas: {5 - vidas}", 300, 290)
        dibujar_texto(f"💥 Meteoritos eliminados: {meteoritos_destruidos}", 300, 320)
        dibujar_texto(f"🌌 Meteoritos restantes: {MAX_METEORITOS - meteoritos_destruidos}", 300, 350)
        dibujar_texto(f"🕒 Tiempo total: {int(tiempo_actual)}s", 300, 380)
        # Sonido Fin del juego
        mixer.music.load("RecursosTarea/final.mp3")
        mixer.music.play(-1)
        mixer.music.set_volume(0.3)
        pygame.display.update()
        time.sleep(6)
        ejecutando = False

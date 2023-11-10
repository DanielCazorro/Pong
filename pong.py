import pygame
from random import randint

# Constantes para el juego
ANCHO = 800
ALTO = 600
FPS = 60

# Colores
C_BLANCO = (255, 255, 255)
C_VERDE = (0, 100, 0)
C_GRAY = (66, 66, 66)

# Puntos necesarios para ganar
PUNTOS_PARTIDA = 9

# Dimensiones de las paletas y velocidad del jugador
ANCHO_PALETA = 10
ALTO_PALETA = 40
MARGEN_LATERAL = 40
MARGEN = 40
VEL_JUGADOR = 5

# Dimensiones de la pelota y velocidad máxima
TAM_PELOTA = 8
VEL_MAX_PELOTA = 5

# ...

# Clase Jugador
class Jugador(pygame.Rect):
    ARRIBA = True
    ABAJO = False
    VELOCIDAD = VEL_JUGADOR

    def __init__(self, pos_x, pos_y):
        super(Jugador, self).__init__(pos_x, pos_y, ANCHO_PALETA, ALTO_PALETA)

    def pintame(self, pantalla):
        pygame.draw.rect(pantalla, C_BLANCO, self)

    def muevete(self, direccion):
        if direccion == self.ARRIBA:
            self.y = self.y - self.VELOCIDAD
            if self.y < 0:
                self.y = 0
        else:
            self.y = self.y + self.VELOCIDAD
            if self.y > ALTO - ALTO_PALETA:
                self.y = ALTO - ALTO_PALETA

# ...

# Clase Pelota
class Pelota(pygame.Rect):
    def __init__(self, x, y):
        super(Pelota, self).__init__(x, y, TAM_PELOTA, TAM_PELOTA)
        self.velocidad_y = randint(-VEL_MAX_PELOTA, VEL_MAX_PELOTA)
        self.velocidad_x = 0
        while self.velocidad_x == 0:
            self.velocidad_x = randint(-VEL_MAX_PELOTA, VEL_MAX_PELOTA)

    def pintame(self, pantalla):
        pygame.draw.rect(pantalla, C_BLANCO, self)

    def mover(self):
        self.x = self.x + self.velocidad_x
        self.y = self.y + self.velocidad_y
        if self.y <= 0:
            self.y = 0
            self.velocidad_y = -self.velocidad_y
        if self.y >= ALTO - TAM_PELOTA:
            self.y = ALTO - TAM_PELOTA
            self.velocidad_y = -self.velocidad_y

    def comprobar_punto(self):
        resultado = 0
        if self.x < 0:
            self.x = (ANCHO - TAM_PELOTA) / 2
            self.y = (ALTO - TAM_PELOTA) / 2
            self.velocidad_y = randint(-VEL_MAX_PELOTA, VEL_MAX_PELOTA)
            self.velocidad_x = randint(-VEL_MAX_PELOTA, -1)
            print("Punto para el jugador 2")
            resultado = 2
        elif self.x > ANCHO:
            self.x = (ANCHO - TAM_PELOTA) / 2
            self.y = (ALTO - TAM_PELOTA) / 2
            self.velocidad_y = randint(-VEL_MAX_PELOTA, VEL_MAX_PELOTA)
            self.velocidad_x = randint(1, VEL_MAX_PELOTA)
            print("Punto para el jugador 1")
            resultado = 1

        return resultado

# ...

# Clase Marcador
class Marcador:
    ganador = 0

    def __init__(self):
        self.tipo_letra = pygame.font.SysFont('Ubuntu', 50, True)
        self.reset()

    def reset(self):
        self.puntuacion = [0, 0]
        self.ganador = 0

    def sumar_punto(self, jugador):
        self.puntuacion[jugador - 1] += 1

    def comprobar_ganador(self):
        if self.puntuacion[0] == PUNTOS_PARTIDA:
            self.reset()
            self.ganador = 1
        if self.puntuacion[1] == PUNTOS_PARTIDA:
            print("Gana el jugador 2")
            self.reset()
            self.ganador = 2
        return self.ganador > 0

    def pintar_ganador(self, pantalla):
        msg_texto = f"El ganador es el jugador {self.ganador}"
        texto = pygame.font.Font.render(
            self.tipo_letra, msg_texto, True, C_BLANCO)
        pos_x = ANCHO / 2 - texto.get_width() / 2
        pos_y = (ALTO - texto.get_height()) / 2
        pygame.Surface.blit(pantalla, texto, (pos_x, pos_y))

    def mostrar(self, pantalla=None):
        nuevo_marcador = f"({self.puntuacion[0]} - {self.puntuacion[1]})"
        if pantalla is not None or nuevo_marcador != self.ultimo_marcador:
            texto = self.tipo_letra.render(nuevo_marcador, True, C_BLANCO)
            if pantalla is not None:
                pos_x = ANCHO / 2 - texto.get_width() / 2
                pos_y = 20  # Ajusta la posición vertical del marcador en pantalla
                pygame.Surface.blit(pantalla, texto, (pos_x, pos_y))
            else:
                print(f"El marcador ahora es: {nuevo_marcador}")
            self.ultimo_marcador = nuevo_marcador


# ...

# Clase Pong
class Pong:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        self.reloj = pygame.time.Clock()

        pos_y = (ALTO - ALTO_PALETA) / 2
        pos_x_2 = ANCHO - MARGEN_LATERAL - ANCHO_PALETA
        self.jugador1 = Jugador(MARGEN_LATERAL, pos_y)
        self.jugador2 = Jugador(pos_x_2, pos_y)

        pelota_x = (ANCHO - TAM_PELOTA) / 2
        pelota_y = (ALTO - TAM_PELOTA) / 2
        self.pelota = Pelota(pelota_x, pelota_y)

        self.marcador = Marcador()

        pygame.font.init()

    def bucle_principal(self):
        salir = False
        while not salir:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    salir = True
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        salir = True

            estado_teclado = pygame.key.get_pressed()
            if estado_teclado[pygame.K_a]:
                self.jugador1.muevete(Jugador.ARRIBA)
            if estado_teclado[pygame.K_z]:
                self.jugador1.muevete(Jugador.ABAJO)
            if estado_teclado[pygame.K_UP]:
                self.jugador2.muevete(Jugador.ARRIBA)
            if estado_teclado[pygame.K_DOWN]:
                self.jugador2.muevete(Jugador.ABAJO)

            self.pantalla.fill(C_VERDE)  # Cambio de color de fondo a verde
            self.jugador1.pintame(self.pantalla)
            self.jugador2.pintame(self.pantalla)

            self.pinta_red()
            self.pinta_pelota()
            
            # Muestra el marcador en pantalla y en consola
            self.marcador.mostrar(self.pantalla)
            self.marcador.mostrar()

            jugador_que_puntua = self.pelota.comprobar_punto()
            if jugador_que_puntua > 0:
                self.marcador.sumar_punto(jugador_que_puntua)
            if self.marcador.comprobar_ganador():
                self.marcador.pintar_ganador(self.pantalla)
                salir = True

            pygame.display.flip()
            self.reloj.tick(FPS)

    def pinta_pelota(self):
        self.pelota.mover()
        if self.pelota.colliderect(self.jugador1) or self.pelota.colliderect(self.jugador2):
            self.pelota.velocidad_x = -self.pelota.velocidad_x + randint(-2, 2)
            self.pelota.velocidad_y = randint(-VEL_MAX_PELOTA, VEL_MAX_PELOTA)
        self.pelota.pintame(self.pantalla)

    def pinta_red(self):
        tramo_pintado = 20
        tramo_vacio = 10
        ancho_red = 4
        pos_x = ANCHO / 2 - ancho_red / 2

        for y in range(MARGEN, ALTO - MARGEN, tramo_pintado + tramo_vacio):
            pygame.draw.line(self.pantalla, C_BLANCO, (pos_x, y),
                             (pos_x, y + tramo_pintado), ancho_red)


if __name__ == "__main__":
    juego = Pong()
    juego.bucle_principal()

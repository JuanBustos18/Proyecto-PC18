class Ficha:
    def __init__(self, id_ficha: int, jugador, salida: int):
        self.id = id_ficha
        self.jugador = jugador
        self.posicion = None
        self.estado = 'carcel'  # carcel, juego, llegada
        self.casilla_salida = salida
        self.indice_llegada = None

    def salir(self, casillas):
        if self.estado == 'carcel':
            self.posicion = self.casilla_salida
            self.estado = 'juego'
            casillas[self.posicion].append(self)

    def mover(self, pasos: int, casillas):
        if self.estado == 'carcel':
            return False

        if self.estado == 'juego':
            nueva_pos = self.posicion + pasos
            if nueva_pos > 68:
                nueva_pos -= 68

            if nueva_pos == self.jugador.casilla_llegada_final:
                self.estado = 'llegada'
                self.posicion = None
                self.indice_llegada = 0
                self.jugador.zona_llegada[0] = self
                casillas[self.posicion].remove(self)
                return True

            if self.posicion in casillas:
                casillas[self.posicion].remove(self)
            self.posicion = nueva_pos
            casillas[self.posicion].append(self)
            return True

        elif self.estado == 'llegada':
            nuevo_indice = self.indice_llegada + pasos
            if nuevo_indice < len(self.jugador.zona_llegada) and self.jugador.zona_llegada[nuevo_indice] is None:
                self.jugador.zona_llegada[self.indice_llegada] = None
                self.jugador.zona_llegada[nuevo_indice] = self
                self.indice_llegada = nuevo_indice
                return True
            elif nuevo_indice == len(self.jugador.zona_llegada):
                self.jugador.zona_llegada[self.indice_llegada] = None
                self.indice_llegada = None
                print(f"Ficha {self.id} completó la llegada final.")
                return True
            else:
                print("Movimiento en llegada inválido.")
                return False

    def enviar_a_carcel(self, casillas):
        if self.estado == 'llegada' and self.indice_llegada is not None:
            self.jugador.zona_llegada[self.indice_llegada] = None
        elif self.estado == 'juego' and self.posicion in casillas:
            casillas[self.posicion].remove(self)
        self.estado = 'carcel'
        self.posicion = None
        self.indice_llegada = None

    def __str__(self):
        if self.estado == 'llegada':
            return f"Ficha {self.id} (llegada) - Casilla {self.indice_llegada + 1}"
        return f"Ficha {self.id} ({self.estado}) - Posición: {self.posicion}"


class Jugador:
    def __init__(self, nombre: str, color: str, casilla_salida: int, casillas_llegada: list):
        self.nombre = nombre
        self.color = color
        self.casilla_salida = casilla_salida
        self.casilla_llegada_final = casilla_salida - 1 if casilla_salida != 1 else 68
        self.zona_llegada = [None] * 8
        self.indices_llegada = casillas_llegada
        self.fichas = [Ficha(i + 1, self, casilla_salida) for i in range(4)]

    def mostrar_fichas(self):
        for ficha in self.fichas:
            print(ficha)

    def fichas_en_juego(self):
        return [f for f in self.fichas if f.estado == 'juego']

    def fichas_en_casilla(self, casilla):
        return [f for f in self.fichas if f.posicion == casilla]

    def tiene_bloqueo_en(self, casilla):
        return len(self.fichas_en_casilla(casilla)) == 2

    def ha_ganado(self):
        return all(f.estado == 'llegada' and f.indice_llegada == 7 for f in self.fichas)

    def mover_extra(self, pasos, casillas):
        activas = self.fichas_en_juego()
        if not activas:
            print(f"No hay fichas disponibles para usar los {pasos} pasos extra.")
            return
        print(f"Tienes {pasos} pasos extra. Fichas activas:")
        for f in activas:
            print(f"- Ficha {f.id} en posición {f.posicion}")
        while True:
            try:
                seleccion = int(input(f"Elige una ficha para mover {pasos} pasos: "))
                ficha = next((f for f in activas if f.id == seleccion), None)
                if ficha:
                    if ficha.mover(pasos, casillas):
                        print(f"Ficha {ficha.id} movida a la posición {ficha.posicion}.")
                        if ficha.estado == 'llegada':
                            print(f"¡Ficha {ficha.id} llegó a la meta!")
                            self.mover_extra(10, casillas)
                    break
                else:
                    print("Ficha inválida.")
            except ValueError:
                print("Entrada inválida.")

    def obtener_fichas_en(self, casilla, casillas):
        return casillas.get(casilla, [])
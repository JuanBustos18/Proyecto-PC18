from jugador import Jugador
from dados import Dado
from tablero_consola import mostrar_tablero
import random

casillas = {i: [] for i in range(1, 69)}  # Casillas del 1 al 68
casillas_seguras = [9, 17, 26, 34, 43, 51, 60, 68]
casillas_salida = [5, 22, 39, 56]

intentos_sin_salida = {}
pares_consecutivos = 0
ultima_ficha_movida = None


def es_seguro_o_salida(casilla):
    return casilla in casillas_seguras or casilla in casillas_salida


def hay_bloqueo_en_camino(jugador, posicion_actual, pasos):
    for i in range(1, pasos + 1):
        pos = posicion_actual + i
        if pos > 68:
            pos -= 68
        ocupantes = casillas.get(pos, [])
        if len(ocupantes) >= 2:
            mismos = all(f.jugador == ocupantes[0].jugador for f in ocupantes)
            if mismos or es_seguro_o_salida(pos):
                return pos
    return None


def capturar_si_corresponde(ficha, pasos, jugadores):
    nueva_pos = ficha.posicion + pasos
    if nueva_pos > 68:
        nueva_pos -= 68
    if es_seguro_o_salida(nueva_pos):
        return False

    for otro in jugadores:
        if otro != ficha.jugador:
            enemigas = otro.obtener_fichas_en(nueva_pos, casillas)
            if len(enemigas) == 1:
                enemiga = enemigas[0]
                enemiga.enviar_a_carcel(casillas)
                print(f"⚔️ ¡Captura! Ficha {enemiga.id} de {otro.nombre} fue enviada a la cárcel.")
                return True
    return False


def configurar_jugadores():
    colores_disponibles = ["Rojo", "Verde", "Azul", "Amarillo"]
    jugadores = []
    while True:
        try:
            num = int(input("¿Cuántos jugadores van a participar? (2 a 4): "))
            if 2 <= num <= 4:
                break
        except ValueError:
            print("Entrada inválida.")
    for i in range(num):
        nombre = input(f"Ingrese el nombre del Jugador {i+1}: ")
        color = random.choice(colores_disponibles)
        colores_disponibles.remove(color)
        salida = casillas_salida[i]
        llegada = list(range(69 + i * 8, 69 + (i + 1) * 8))
        jugador = Jugador(nombre, color, salida, llegada)
        jugadores.append(jugador)
        intentos_sin_salida[nombre] = 0
        print(f"{nombre} jugará con el color {color}.")
    return jugadores


def turno_jugador(jugador, jugadores, dado):
    global pares_consecutivos, ultima_ficha_movida

    print(f"\nTurno de {jugador.nombre} ({jugador.color})")
    jugador.mostrar_fichas()
    mostrar_tablero(jugadores, casillas)

    input("Presiona ENTER para lanzar los dados...")
    d1, d2 = dado.lanzar()
    es_par = d1 == d2

    if es_par:
        pares_consecutivos += 1
        print(f"¡Doble! Pares consecutivos: {pares_consecutivos}")
    else:
        pares_consecutivos = 0

    if pares_consecutivos == 3:
        print("¡Tres pares seguidos! La última ficha vuelve a la cárcel.")
        if ultima_ficha_movida:
            ultima_ficha_movida.enviar_a_carcel(casillas)
        pares_consecutivos = 0
        return False

    puede_sacar = dado.es_cinco(d1, d2)
    fichas_carcel = [f for f in jugador.fichas if f.estado == 'carcel']
    fichas_juego = jugador.fichas_en_juego()

    if len(fichas_carcel) == 4 and not puede_sacar:
        intentos_sin_salida[jugador.nombre] += 1
        print(f"No puedes sacar ficha. Intento {intentos_sin_salida[jugador.nombre]}/3.")
        if intentos_sin_salida[jugador.nombre] >= 3:
            print("Turno perdido por 3 intentos fallidos.")
            intentos_sin_salida[jugador.nombre] = 0
            return False
        return True
    else:
        intentos_sin_salida[jugador.nombre] = 0

    if puede_sacar and fichas_carcel:
        en_salida = jugador.fichas_en_casilla(jugador.casilla_salida)
        if len(en_salida) >= 2:
            print("La salida está bloqueada. No puedes sacar ficha.")
        else:
            print("Puedes sacar una ficha de la cárcel.")
            for f in fichas_carcel:
                print(f"- Ficha {f.id}")
            while True:
                try:
                    sel = int(input("Elige la ficha a sacar: "))
                    ficha = next((f for f in fichas_carcel if f.id == sel), None)
                    if ficha:
                        ficha.salir(casillas)
                        print(f"Ficha {ficha.id} ha salido.")
                        ultima_ficha_movida = ficha
                        break
                except ValueError:
                    print("Entrada inválida.")

    elif fichas_juego:
        eleccion = input(f"¿Mover una ficha con {d1 + d2} o dos fichas con {d1} y {d2}? (una/dos): ").lower()
        if eleccion == 'una':
            while True:
                try:
                    sel = int(input("Elige la ficha a mover: "))
                    ficha = next((f for f in fichas_juego if f.id == sel), None)
                    if ficha:
                        bloqueo = hay_bloqueo_en_camino(jugador, ficha.posicion, d1 + d2)
                        if bloqueo:
                            print(f"Movimiento bloqueado en la casilla {bloqueo}.")
                        else:
                            hubo_captura = capturar_si_corresponde(ficha, d1 + d2, jugadores)
                            if ficha.mover(d1 + d2, casillas):
                                ultima_ficha_movida = ficha
                                if ficha.estado == "llegada":
                                    print(f"¡Ficha {ficha.id} llegó a la meta!")
                                    jugador.mover_extra(10, casillas)
                                elif hubo_captura:
                                    jugador.mover_extra(20, casillas)
                        break
                except ValueError:
                    print("Entrada inválida.")
        elif eleccion == 'dos':
            for valor in [d1, d2]:
                while True:
                    try:
                        sel = int(input(f"Elige ficha para mover {valor} pasos: "))
                        ficha = next((f for f in fichas_juego if f.id == sel), None)
                        if ficha:
                            bloqueo = hay_bloqueo_en_camino(jugador, ficha.posicion, valor)
                            if bloqueo:
                                print(f"Movimiento bloqueado en la casilla {bloqueo}.")
                            else:
                                hubo_captura = capturar_si_corresponde(ficha, valor, jugadores)
                                if ficha.mover(valor, casillas):
                                    ultima_ficha_movida = ficha
                                    if ficha.estado == "llegada":
                                        print(f"¡Ficha {ficha.id} llegó a la meta!")
                                        jugador.mover_extra(10, casillas)
                                    elif hubo_captura:
                                        jugador.mover_extra(20, casillas)
                            break
                    except ValueError:
                        print("Entrada inválida.")
    else:
        print("No puedes mover ninguna ficha.")
        return False

    jugador.mostrar_fichas()
    mostrar_tablero(jugadores, casillas)

    if jugador.ha_ganado():
        print(f"\n🏆 ¡{jugador.nombre} ha ganado con todas sus fichas en la meta!")
        exit()

    return es_par


def iniciar_juego():
    print("Bienvenido a Parqués UN (modo consola)")
    jugadores = configurar_jugadores()
    dado = Dado(modo='desarrollador')  # Puedes cambiar a 'real'
    turno = 0

    while True:
        jugador_actual = jugadores[turno]
        repetir = turno_jugador(jugador_actual, jugadores, dado)
        if not repetir:
            turno = (turno + 1) % len(jugadores)
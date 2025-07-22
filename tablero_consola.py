def mostrar_tablero(jugadores, casillas):
    print("\n📍 Estado del Tablero [1–68]:")
    tablero = ['__'] * 68  # Representación base del tablero

    # Poblar casillas con fichas activas
    for pos in range(1, 69):
        contenido = casillas.get(pos, [])
        if contenido:
            etiquetas = [f"{f.jugador.color[0]}{f.id}" for f in contenido]
            tablero[pos - 1] = ",".join(etiquetas)

    # Mostrar en bloques de 10
    for i in range(0, 68, 10):
        etiquetas = [str(n).rjust(2) for n in range(i+1, min(i+11, 69))]
        valores = [tablero[j].center(6) for j in range(i, min(i+10, 68))]
        print(" ".join(etiquetas))
        print(" ".join(valores))
    print()

    # Mostrar zona de llegada
    for jugador in jugadores:
        llegada = jugador.zona_llegada
        if any(f is not None for f in llegada):
            print(f"🎯 Zona de llegada de {jugador.nombre} ({jugador.color}):")
            for i, ficha in enumerate(llegada):
                if ficha:
                    print(f"  Casilla {i+1}: F{ficha.id}")
            print()
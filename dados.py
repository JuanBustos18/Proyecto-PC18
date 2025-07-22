import random

class Dado:
    def __init__(self, modo='real'):
        self.modo = modo

    def lanzar(self):
        if self.modo == 'desarrollador':
            while True:
                try:
                    d1 = int(input("Ingresa el valor del primer dado (1-6): "))
                    d2 = int(input("Ingresa el valor del segundo dado (1-6): "))
                    if 1 <= d1 <= 6 and 1 <= d2 <= 6:
                        print(f"Dados lanzados manualmente: {d1} y {d2}")
                        return d1, d2
                    else:
                        print("Los valores deben estar entre 1 y 6.")
                except ValueError:
                    print("Entrada inválida. Debes ingresar números enteros.")
        else:
            d1 = random.randint(1, 6)
            d2 = random.randint(1, 6)
            print(f"Dados lanzados: {d1} y {d2}")
            return d1, d2

    def es_cinco(self, d1, d2):
        return d1 == 5 or d2 == 5 or (d1 + d2 == 5)

    def es_par(self, d1, d2):
        return d1 == d2
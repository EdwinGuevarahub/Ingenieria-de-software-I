from abc import ABC, abstractmethod
from math import sqrt, pi


class Punto:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distancia(self, otro):
        """Calcular la distancia entre dos puntos."""
        return sqrt((self.x - otro.x) ** 2 + (self.y - otro.y) ** 2)


# Polilinea
class Linea:
    def __init__(self, puntos: list[Punto]):
        if len(puntos) < 2:
            raise ValueError("Una línea debe tener al menos 2 puntos.")
        self.puntos = puntos

    def longitud(self):
        """Calcular la longitud total de la línea."""
        longitud_total = 0
        for i in range(len(self.puntos) - 1):
            longitud_total += self.puntos[i].distancia(self.puntos[i + 1])
        return longitud_total


# Poligono generico
class Poligono(ABC):
    def __init__(self, lineas: list[Linea]):
        self.lineas = lineas

    # Abstracto para que sea redefinido por la subclase
    @abstractmethod
    def area(self):
        pass

    def perimetro(self):
        """Calcular el perímetro del polígono."""
        return sum(linea.longitud() for linea in self.lineas)


class Circulo(Poligono):
    def __init__(self, centro: Punto, radio: float):
        super().__init__([])
        self.centro = centro
        self.radio = radio

    def area(self):
        """Calcular el área del círculo."""
        return pi * self.radio**2

    def perimetro(self):
        """Calcular el perímetro (circunferencia) del círculo."""
        return 2 * pi * self.radio


class PoligonoConvexo(Poligono):
    def __init__(self, puntos: list[Punto]):
        if len(puntos) < 3:
            raise ValueError("Un polígono debe tener al menos 3 puntos.")
        # (i + 1) % len(puntos) devuelve el i + 1 elemento de la lista excepto para el ultimo,
        # donde el modulo se vuelve 0, que corresponde al primer elemento de la lista.
        lineas = [Linea([puntos[i], puntos[(i + 1) % len(puntos)]])for i in range(len(puntos))]
        super().__init__(lineas)
        self.puntos = puntos

    def area(self):
        """Calcular el área del polígono convexo dividiéndolo en triángulos."""

        def area_triangulo(p1, p2, p3):
            """Función auxiliar para calcular el área de un triángulo."""
            return abs((p1.x * (p2.y - p3.y) + p2.x * (p3.y - p1.y) + p3.x * (p1.y - p2.y)) / 2)

        area_total = 0
        for i in range(1, len(self.puntos) - 1):
            area_total += area_triangulo(self.puntos[0], self.puntos[i], self.puntos[i + 1])
        return area_total


class Triangulo(PoligonoConvexo):
    def __init__(self, puntos: list[Punto]):
        if len(puntos) != 3:
            raise ValueError("Un triángulo debe tener exactamente 3 puntos.")
        super().__init__(puntos)

    def area(self):
        """Sobrescribir el método de área para usar la fórmula de Herón."""
        a, b, c = [linea.longitud() for linea in self.lineas]
        s = (a + b + c) / 2
        return sqrt(s * (s - a) * (s - b) * (s - c))


# Tests
p1 = Punto(0, 0)
p2 = Punto(3, 0)
p3 = Punto(3, 4)
p4 = Punto(1, 4)
p5 = Punto(0, 0)
p6 = Punto(0, 2)
p7 = Punto(2, 4)
p8 = Punto(4, 5)

# Test Linea (línea básica de 2 puntos)
linea1 = Linea([p1, p2])
linea2 = Linea([p1, p2, p3])
print(f"Longitud de la línea 1: {linea1.longitud()}")
print(f"Longitud de la línea 2: {linea2.longitud()}")

# Test Triángulo
triangulo = Triangulo([p1, p2, p3])
print(f"Area y Perimetro del triangulo: {triangulo.area()} | {triangulo.perimetro()}")

# Test Polígono Convexo
poligono_convexo1 = PoligonoConvexo([p1, p2, p3, p4])
poligono_convexo2 = PoligonoConvexo([p5, p6, p7, p8])
print(f"Area y Perimetro del poligono convexo 1: {poligono_convexo1.area()} | {poligono_convexo1.perimetro()}")
print(f"Area y Perimetro del poligono convexo 2: {poligono_convexo2.area()} | {poligono_convexo2.perimetro()}")

# Test Círculo
circulo = Circulo(centro=p1, radio=5)
print(f"Area y Perimetro del círculo: {circulo.area()} | {circulo.perimetro()}")

# MCIC - Ingenieria de Software I
# Ejercicio POO - Calculadora
# Edwin Guevara 
# 20241595001

import tkinter as tk
from tkinter import ttk, messagebox

class Numero:
    def __init__(self, valor: int, base: int):
        self.valor = valor
        self.base = base

    def convertir_hacia_base10(self) -> int:
        """Convierte el valor desde la base especificada a base 10."""
        return int(str(self.valor), self.base)

    def convertir_desde_base10(self, valor_base10: int) -> str:        
        # Convertir el valor base 10 a la base especificada
        numero_base_n = ""
        valor_base10 = int(valor_base10)  # Asegurar que estamos trabajando con un entero
        
        if valor_base10 == 0:
            return "0"
        
        while valor_base10 > 0:
            digito = valor_base10 % self.base
            if digito < 10:
                numero_base_n = chr(48 + digito) + numero_base_n  # 48 es el código ASCII de '0'
            else:
                numero_base_n = chr(87 + digito) + numero_base_n  # 87 es el código ASCII de 'a' - 10
            valor_base10 //= self.base

        return numero_base_n
    
    def validar(self) -> bool:
        """Valida si el valor pertenece a la base indicada."""
        try:
            int(str(self.valor), self.base)
            return True
        except ValueError:
            return False


class Operacion:
    def execute(self, a: Numero, b: Numero):
        raise NotImplementedError("Debe implementarse en la subclase")

class Addition(Operacion):
    def operar(self, a: Numero, b: Numero):
        return a.convertir_hacia_base10() + b.convertir_hacia_base10()

class Subtraction(Operacion):
    def operar(self, a: Numero, b: Numero):
        return a.convertir_hacia_base10() - b.convertir_hacia_base10()

class Multiplication(Operacion):
    def operar(self, a: Numero, b: Numero):
        return a.convertir_hacia_base10() * b.convertir_hacia_base10()

class Division(Operacion):
    def operar(self, a: Numero, b: Numero):
        if b.convertir_hacia_base10() == 0:
            raise ValueError("División por cero")
        return a.convertir_hacia_base10() / b.convertir_hacia_base10()


class Calculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora")

        self.bases = [2, 3, 4, 5, 6, 7, 8, 9, 10]

        # Crear la interfaz
        self.crear_ui()

    def crear_ui(self):

        self.num1_label = ttk.Label(self.root, text="Número 1:")
        self.num1_label.grid(column=0, row=0, padx=5, pady=5)

        self.num1_entrada = ttk.Entry(self.root)
        self.num1_entrada.insert(0, "0")
        self.num1_entrada.grid(column=1, row=0, padx=5, pady=5)

        self.base1_label = ttk.Label(self.root, text="Base de Número 1:")
        self.base1_label.grid(column=2, row=0, padx=5, pady=5)

        self.base_var1 = tk.IntVar(value=self.bases[-1])
        self.base1_menu = ttk.OptionMenu(self.root, self.base_var1, self.bases[-1], *self.bases)
        self.base1_menu.grid(column=3, row=0, padx=5, pady=5)

        self.num2_label = ttk.Label(self.root, text="Número 2:")
        self.num2_label.grid(column=0, row=1, padx=5, pady=5)

        self.num2_entrada = ttk.Entry(self.root)
        self.num2_entrada.insert(0, "0")
        self.num2_entrada.grid(column=1, row=1, padx=5, pady=5)

        self.base2_label = ttk.Label(self.root, text="Base de Número 2:")
        self.base2_label.grid(column=2, row=1, padx=5, pady=5)

        self.base_var2 = tk.IntVar(value=self.bases[-1])
        self.base2_menu = ttk.OptionMenu(self.root, self.base_var2, self.bases[-1], *self.bases)
        self.base2_menu.grid(column=3, row=1, padx=5, pady=5)

        self.resultado_base_label = ttk.Label(self.root, text="Base de Resultado:")
        self.resultado_base_label.grid(column=0, row=2, padx=5, pady=5)

        self.base_resultado = tk.IntVar(value=self.bases[-1])
        self.resultado_base_entrada = ttk.OptionMenu(self.root, self.base_resultado, self.bases[-1], *self.bases)
        self.resultado_base_entrada.grid(column=1, row=2, padx=5, pady=5)

        self.operacion_label = ttk.Label(self.root, text="Operacion:")
        self.operacion_label.grid(column=2, row=2, padx=5, pady=5)

        self.operaciones = {
            "Suma": Addition(),
            "Resta": Subtraction(),
            "Multiplicación": Multiplication(),
            "División": Division(),
        }

        self.operacion_var = tk.StringVar()
        self.operacion_var.set("Suma")

        self.operacion_menu = ttk.OptionMenu(self.root, self.operacion_var, *self.operaciones.keys())
        self.operacion_menu.grid(column=3, row=2, padx=5, pady=5)

        self.boton_calcular = ttk.Button(self.root, text="Calcular", command=self.calcular)
        self.boton_calcular.grid(column=2   , row=3, padx=5, pady=5)

        self.resultado_label = ttk.Label(self.root, text="Resultado:")
        self.resultado_label.grid(column=0, row=3, padx=5, pady=5)

        self.resultado_var = tk.StringVar()
        self.resultado_entry = ttk.Entry(self.root, textvariable=self.resultado_var, state="readonly")
        self.resultado_entry.grid(column=1, row=3, padx=5, pady=5)

    def calcular(self):
        try:
            num1 = self.num1_entrada.get()
            num2 = self.num2_entrada.get()
            base1 = int(self.base_var1.get())
            base2 = int(self.base_var2.get())
            result_base = int(self.base_resultado.get())

            # Crear instancias de la clase Número
            numero1 = Numero(int(num1), base1)
            numero2 = Numero(int(num2), base2)

            # Validar que los números pertenecen a sus respectivas bases
            if not numero1.validar():
                raise ValueError(f"Número 1 ingresado({num1}) no es válido en la base {base1}")
            if not numero2.validar():
                raise ValueError(f"Número 2 ingresado({num2}) no es válido en la base {base2}")
            
            # Instancia clase operacion en funcion del valor obtenido del formulario
            operacion = self.operaciones[self.operacion_var.get()]
            resultado_decimal = operacion.operar(numero1, numero2)

            numero_resultado = Numero(resultado_decimal, result_base)  # Base 10 para el cálculo
            resultado = numero_resultado.convertir_desde_base10(resultado_decimal)
            self.resultado_var.set(resultado)

        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", "Se produjo un error al calcular", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = Calculadora(root)
    root.mainloop()

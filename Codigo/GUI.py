'''
Proyecto 1 - GUI.py
Descripción: Esta implementación contiene la interfaz gráfica para ejecutar las soluciones de la terminal inteligente y la subasta pública.
Autores:
            Rodas Arango, Juan Manuel - 2259571
            García Castañeda, Alex - 2259517
            Gómez Agudelo, Juan Sebastián - 2259474
            Henao Aricapa, Stiven - 2259603
Docente:
            Delgado Saavedra, Carlos Andrés
Fecha: 2024-10-25
'''

import tkinter as tk
from tkinter import ttk, messagebox
from TerminalInteligente import (
    solucion_ingenua,
    solucion_dinamica,
    solucion_voraz,
    formatear_costos,
    generar_cadena_costos,
    aplicar_operaciones,
    operaciones_a_costos
)

from SubastaPublica import (
    fuerza_bruta,
    programacion_dinamica,
    voraz)

# Función para crear la interfaz gráfica
def crear_interfaz():
    root = tk.Tk()
    root.geometry("600x400")

    style = ttk.Style()
    style.configure("TButton",
                    font=("Helvetica", 14),
                    padding=14,
                    relief="groove",
                    background="#E0E0E0",
                    foreground="#000000")

    style.map("TButton",
              foreground=[('disabled', '#A0A0A0'), ('active', '#000000')],
              background=[('active', '#D5D5D5'), ('disabled', '#F0F0F0')])
    
    style = ttk.Style()
    style.configure("Treeview", rowheight=25)
    style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    style.configure("Treeview", bordercolor='black', relief='solid')
    
    # Ventana Principal
    def abrir_terminal_inteligente():
        ventana_terminal = tk.Toplevel(root)
        ventana_terminal.title("Terminal Inteligente")
        ventana_terminal.geometry("1200x800")
    
        # Configuración de Costos
        frame_costos = ttk.LabelFrame(ventana_terminal, text="Configuración de Costos")
        frame_costos.pack(fill="x", padx=10, pady=5)
    
        costos_vars = {}
        operaciones = ['a', 'd', 'r', 'i', 'k']
        etiquetas = {'a': 'Advance (a):', 'd': 'Delete (d):', 'r': 'Replace (r):',
                    'i': 'Insert (i):', 'k': 'Kill (k):'}
        for idx, operacion in enumerate(operaciones):
            ttk.Label(frame_costos, text=etiquetas[operacion]).grid(row=0, column=idx*2, padx=5, pady=5, sticky='e')
            var = tk.IntVar(value=1 if operacion in ['a', 'k'] else (2 if operacion in ['d', 'i'] else 3))
            entry = ttk.Entry(frame_costos, textvariable=var, width=5)
            entry.grid(row=0, column=idx*2 +1, padx=5, pady=5)
            costos_vars[operacion] = var
    
        # Campos de texto para cadenas
        frame_cadenas = ttk.LabelFrame(ventana_terminal, text="Cadenas de Texto")
        frame_cadenas.pack(fill="x", padx=10, pady=5)
    
        ttk.Label(frame_cadenas, text="Cadena inicial:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        cadena_inicial_var = tk.StringVar()
        ttk.Entry(frame_cadenas, textvariable=cadena_inicial_var, width=50).grid(row=0, column=1, padx=5, pady=5)
    
        ttk.Label(frame_cadenas, text="Cadena final:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        cadena_final_var = tk.StringVar()
        ttk.Entry(frame_cadenas, textvariable=cadena_final_var, width=50).grid(row=1, column=1, padx=5, pady=5)
    
        # Botón para ejecutar soluciones
        def ejecutar_soluciones():
            # Obtener costos
            costos_operaciones = {k: costos_vars[k].get() for k in costos_vars}
            # Validar que los costos sean positivos
            for op, cost in costos_operaciones.items():
                if cost <= 0:
                    messagebox.showerror("Error", f"El costo de la operación '{op}' debe ser positivo.")
                    return
            # Obtener cadenas
            cadena_inicial = cadena_inicial_var.get()
            cadena_final = cadena_final_var.get()
            if not cadena_inicial or not cadena_final:
                messagebox.showerror("Error", "Por favor, ingrese ambas cadenas.")
                return
            # Solución Ingenua
            costos_ingenua = {'a': 0, 'd': 0, 'r': 0, 'i': 0, 'k': 0}
            resultado_ingenua, costos_final_ingenua, operaciones_ingenua = solucion_ingenua(
                cadena_inicial, cadena_final, 0, costos_ingenua, []
            )
            if resultado_ingenua is None:
                messagebox.showwarning("Advertencia", "No se encontró una solución ingenua.")
                return
            # Solución Dinámica
            matriz_costos, costo_dinamica, operaciones_dinamica = solucion_dinamica(
                cadena_inicial, cadena_final, costos_operaciones
            )

            # Solución Voraz
            resultado_voraz, costos_final_voraz, operaciones_voraz = solucion_voraz(
                cadena_inicial, cadena_final, costos_operaciones
            )
            # Actualizar las cadenas finales
            # Tabla de Operaciones Paso a Paso para Ingenua
            for item in tabla_paso_a_paso_ingenua.get_children():
                tabla_paso_a_paso_ingenua.delete(item)
            _, _, _, estados_ingenua = aplicar_operaciones(operaciones_ingenua, cadena_inicial)
            for op, estado in estados_ingenua:
                tabla_paso_a_paso_ingenua.insert('', 'end', values=(op, estado))
            # Tabla de Operaciones Paso a Paso para Dinámica
            for item in tabla_paso_a_paso_dinamica.get_children():
                tabla_paso_a_paso_dinamica.delete(item)
            _, _, _, estados_dinamica = aplicar_operaciones(operaciones_dinamica, cadena_inicial)
            for op, estado in estados_dinamica:
                tabla_paso_a_paso_dinamica.insert('', 'end', values=(op, estado))
            # Tabla de Operaciones Paso a Paso para Voraz
            for item in tabla_paso_a_paso_voraz.get_children():
                tabla_paso_a_paso_voraz.delete(item)
            _, _, _, estados_voraz = aplicar_operaciones(operaciones_voraz, cadena_inicial)
            for op, estado in estados_voraz:
                tabla_paso_a_paso_voraz.insert('', 'end', values=(op, estado))
            # Informe de Costos
            texto_costos.config(state='normal')
            texto_costos.delete("1.0", tk.END)
            texto_costos.insert(tk.END, f"Costo Ingenua: {formatear_costos(costos_final_ingenua)}\n")
            texto_costos.insert(tk.END, f"Costo Dinámica: {aplicar_operaciones(operaciones_dinamica, cadena_inicial)[2]}\n")
            texto_costos.insert(tk.END, f"Costo Voraz: " + generar_cadena_costos(operaciones_a_costos(operaciones_voraz)))
            texto_costos.config(state='disabled')
            # Guardar la matriz de costos para visualizarla posteriormente
            ventana_terminal.matriz_costos = matriz_costos
            ventana_terminal.cadena_inicial_matriz = cadena_inicial
            ventana_terminal.cadena_final_matriz = cadena_final
    
        ttk.Button(ventana_terminal, text="Ejecutar soluciones", command=ejecutar_soluciones).pack(pady=10)
    
    
        # Tabla de Operaciones Paso a Paso
        frame_paso_a_paso = ttk.LabelFrame(ventana_terminal, text="Operaciones Paso a Paso")
        frame_paso_a_paso.pack(fill="both", expand=True, padx=10, pady=5)
    
        # Sub-frames para cada solución
        frame_paso_a_paso_ingenua = ttk.LabelFrame(frame_paso_a_paso, text="Ingenua")
        frame_paso_a_paso_ingenua.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        tabla_paso_a_paso_ingenua = ttk.Treeview(frame_paso_a_paso_ingenua, columns=("Operación", "Cadena"), show='headings')
        tabla_paso_a_paso_ingenua.heading("Operación", text="Operación")
        tabla_paso_a_paso_ingenua.heading("Cadena", text="Cadena")
        tabla_paso_a_paso_ingenua.pack(fill="both", expand=True)
    
        frame_paso_a_paso_dinamica = ttk.LabelFrame(frame_paso_a_paso, text="Dinámica")
        frame_paso_a_paso_dinamica.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        tabla_paso_a_paso_dinamica = ttk.Treeview(frame_paso_a_paso_dinamica, columns=("Operación", "Cadena"), show='headings')
        tabla_paso_a_paso_dinamica.heading("Operación", text="Operación")
        tabla_paso_a_paso_dinamica.heading("Cadena", text="Cadena")
        tabla_paso_a_paso_dinamica.pack(fill="both", expand=True)
    
        frame_paso_a_paso_voraz = ttk.LabelFrame(frame_paso_a_paso, text="Voraz")
        frame_paso_a_paso_voraz.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')
        tabla_paso_a_paso_voraz = ttk.Treeview(frame_paso_a_paso_voraz, columns=("Operación", "Cadena"), show='headings')
        tabla_paso_a_paso_voraz.heading("Operación", text="Operación")
        tabla_paso_a_paso_voraz.heading("Cadena", text="Cadena")
        tabla_paso_a_paso_voraz.pack(fill="both", expand=True)
    
        # Ajustar el peso de las columnas en el frame de paso a paso
        frame_paso_a_paso.columnconfigure(0, weight=1)
        frame_paso_a_paso.columnconfigure(1, weight=1)
        frame_paso_a_paso.columnconfigure(2, weight=1)
    
        # Informe de Costos
        frame_informe = ttk.LabelFrame(ventana_terminal, text="Informe de Costos")
        frame_informe.pack(fill="x", padx=10, pady=5)
    
        texto_costos = tk.Text(frame_informe, height=4, state='disabled')
        texto_costos.pack(fill="x", padx=5, pady=5)
    
        # Botón para ver la matriz de la solución dinámica
        def ver_matriz():
            try:
                matriz = ventana_terminal.matriz_costos
                cadena_ini = ventana_terminal.cadena_inicial_matriz
                cadena_fin = ventana_terminal.cadena_final_matriz
            except AttributeError:
                messagebox.showerror("Error", "No se ha ejecutado la solución dinámica todavía.")
                return

            ventana_matriz = tk.Toplevel(ventana_terminal)
            ventana_matriz.title("Matriz de Costos - Solución Dinámica")

            # Configurar la grid para que sea responsive
            ventana_matriz.columnconfigure(0, weight=1)
            ventana_matriz.rowconfigure(0, weight=1)

            # Crear una tabla usando Treeview
            tree = ttk.Treeview(ventana_matriz, style="Custom.Treeview")
            tree.grid(row=0, column=0, sticky='nsew')

            # Agregar un Scrollbar horizontal y vertical
            scrollbar_x = ttk.Scrollbar(ventana_matriz, orient="horizontal", command=tree.xview)
            scrollbar_y = ttk.Scrollbar(ventana_matriz, orient="vertical", command=tree.yview)
            tree.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
            scrollbar_x.grid(row=1, column=0, sticky='ew')
            scrollbar_y.grid(row=0, column=1, sticky='ns')

            # Definir columnas
            columnas = [""] + list(cadena_fin)
            tree["columns"] = columnas
            tree.heading("#0", text="")
            for col in columnas:
                tree.heading(col, text=col)
                tree.column(col, width=50, anchor='center')

            # Insertar filas
            for idx, fila in enumerate(matriz):
                if idx == 0:
                    fila_label = ""
                else:
                    fila_label = cadena_ini[idx-1]
                valores = [fila_label] + fila
                tree.insert("", "end", text="", values=valores)

            # Crear estilo para Treeview
            style = ttk.Style()
            style.configure("Custom.Treeview",
                            font=('Arial', 10),
                            rowheight=25,
                            bordercolor='black',
                            relief='solid')
            style.configure("Custom.Treeview.Heading",
                            font=('Arial', 10, 'bold'),
                            bordercolor='black',
                            relief='solid')
    
        ttk.Button(ventana_terminal, text="Ver matriz", command=ver_matriz).pack(pady=5)

    def abrir_subasta_publica():
            root = tk.Toplevel()
            root.title("Solución Subasta Pública")
            root.geometry("1350x850")

            # Entrada de acciones disponibles
            ttk.Label(root, text="Número de acciones disponibles").grid(row=0, column=0,padx=5, pady=5, sticky='e')
            acciones_var = ttk.Entry(root, width=10)
            acciones_var.grid(row=0, column=1, padx=5, pady=5)


            # Entrada de precio del gobierno
            ttk.Label(root, text="Precio del gobierno por acción:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
            precio_gobierno_var = ttk.Entry(root, width=10)
            precio_gobierno_var.grid(row=1, column=1, padx=5, pady=5)


            # Lista de ofertas
            ofertas = []

            # Listbox para mostrar las ofertas
            listbox_ofertas = tk.Listbox(root, width=50, height=10)
            listbox_ofertas.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

            # Botón para añadir oferta
            def agregar_oferta():
                try:
                    precio = int(entry_precio.get())
                    minimo = int(entry_minimo.get())
                    maximo = int(entry_maximo.get())
                    oferta = (precio, minimo, maximo)
                    ofertas.append(oferta)
                    listbox_ofertas.insert(tk.END, oferta)  # Agregar oferta a la lista
                except ValueError:
                    messagebox.showerror("Error", "Por favor, ingrese valores válidos.")

            ttk.Label(root, text="Precio").grid(row=3, column=0)
            entry_precio = ttk.Entry(root, width=10)
            entry_precio.grid(row=3, column=1)

            ttk.Label(root, text="Mínimo").grid(row=4, column=0)
            entry_minimo = ttk.Entry(root, width=10)
            entry_minimo.grid(row=4, column=1)

            ttk.Label(root, text="Máximo").grid(row=5, column=0)
            entry_maximo = ttk.Entry(root, width=10)
            entry_maximo.grid(row=5, column=1)

            # Botón para agregar oferta alineado a la derecha
            ttk.Button(root, text="Agregar Oferta", command=agregar_oferta).grid(row=4, column=1, padx=5, pady=5, sticky="e")

            # Tablas para soluciones (Ingenua, Dinámica, Voraz)
            frame_resultados = tk.Frame(root)
            frame_resultados.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
            
            tables = {}
            for i, solucion in enumerate(["Ingenua", "Dinámica", "Voraz"]):
                frame_table = tk.Frame(frame_resultados)
                frame_table.grid(row=0, column=i, padx=10)

                label_solucion = tk.Label(frame_table, text=solucion)
                label_solucion.pack()

                table = ttk.Treeview(frame_table, columns=("Oferta", "Acciones"), show="headings", height=6)
                table.heading("Oferta", text="Oferta")
                table.heading("Acciones", text="Acciones")
                table.pack()

                # Guardar la tabla en un diccionario
                tables[solucion] = table

                # Etiqueta para el resultado de cada solución
                label_resultado = tk.Label(frame_table, text="Valor: 0")
                label_resultado.pack()

            # Función para ejecutar soluciones
            def ejecutar_soluciones():
                # Obtener el número de acciones disponibles y el precio del gobierno
                A = int(acciones_var.get())
                precio_gobierno = int(precio_gobierno_var.get())


                if A <= 0:
                    messagebox.showerror("Error", "El número de acciones debe ser mayor que cero.")
                    return

                if precio_gobierno <= 0:
                    messagebox.showerror("Error", "El precio del gobierno debe ser mayor que cero.")
                    return

                if not ofertas:
                    messagebox.showerror("Error", "Debe agregar al menos una oferta.")
                    return

                # Llamar a las funciones de solución
                asignacion_bruta, valor_bruto = fuerza_bruta(A, ofertas, precio_gobierno)
                asignacion_dinamica, valor_dinamico, dp, _= programacion_dinamica(A, ofertas, precio_gobierno)
                asignacion_voraz, valor_voraz = voraz(A, ofertas, precio_gobierno)

                # Mostrar los resultados en las tablas y etiquetas
                tables["Ingenua"].delete(*tables["Ingenua"].get_children())
                for i, (precio, minimo, maximo) in enumerate(ofertas):
                    tables["Ingenua"].insert("", "end", values=(f"Oferta {i+1}", asignacion_bruta[i]))
                label_resultado = tables["Ingenua"].master.winfo_children()[-1]
                label_resultado.config(text=f"Valor: {valor_bruto}")
                # Mostrar asignacion de oferta de gobierno
                tables["Ingenua"].insert("", "end", values=(f"Oferta Gobierno", asignacion_bruta[-1]))

                tables["Dinámica"].delete(*tables["Dinámica"].get_children())
                for i, (precio, minimo, maximo) in enumerate(ofertas):
                    tables["Dinámica"].insert("", "end", values=(f"Oferta {i+1}", asignacion_dinamica[i]))
                label_resultado = tables["Dinámica"].master.winfo_children()[-1]
                label_resultado.config(text=f"Valor: {valor_dinamico}")
                # Mostrar asignacion de oferta de gobierno
                tables["Dinámica"].insert("", "end", values=(f"Oferta Gobierno", asignacion_dinamica[-1]))

                tables["Voraz"].delete(*tables["Voraz"].get_children())
                for i, (precio, minimo, maximo) in enumerate(ofertas):
                    tables["Voraz"].insert("", "end", values=(f"Oferta {i+1}", asignacion_voraz[i]))
                label_resultado = tables["Voraz"].master.winfo_children()[-1]
                label_resultado.config(text=f"Valor: {valor_voraz}")
                # Mostrar asignacion de oferta de gobierno
                tables["Voraz"].insert("", "end", values=(f"Oferta Gobierno", asignacion_voraz[-1]))


            # Función para reiniciar el formulario
            def reiniciar():
                acciones_var.delete(0, tk.END)
                precio_gobierno_var.delete(0, tk.END)
                listbox_ofertas.delete(0, tk.END)
                ofertas.clear()

                # Limpiar las tablas y restablecer los valores
                for solucion in tables:
                    tables[solucion].delete(*tables[solucion].get_children())
                    label_resultado = tables[solucion].master.winfo_children()[-1]
                    label_resultado.config(text="Valor: 0")

            # Botón para ejecutar soluciones
            ttk.Button(root, text="Ejecutar Soluciones", command=ejecutar_soluciones).grid(row=8, column=0, columnspan=2, padx=5, pady=5)

            # Botón para reiniciar el formulario
            ttk.Button(root, text="Reiniciar", command=reiniciar).grid(row=1, column=1, padx=5, pady=5, sticky="e")

            # Función para ver la tabla de asignaciones
            def ver_tabla_asignaciones():
                # Obtener el número de acciones disponibles y el precio del gobierno
                A = int(acciones_var.get())
                precio_gobierno = int(precio_gobierno_var.get())

                # Ejecutar la programación dinámica y obtener las asignaciones
                asignacion_dinamica, valor_dinamico, dp, asignaciones = programacion_dinamica(A, ofertas, precio_gobierno)

                # Crear una nueva ventana para mostrar la tabla de asignaciones
                ventana_asignaciones = tk.Toplevel(root)
                ventana_asignaciones.title("Tabla de Asignaciones - Solución Dinámica")
                ventana_asignaciones.geometry("800x600")

                # Crear un frame para contener la tabla y los scrollbars
                frame_tabla = tk.Frame(ventana_asignaciones)
                frame_tabla.pack(fill="both", expand=True)

                tree = ttk.Treeview(frame_tabla, style="Custom.Treeview")
                tree.pack(side="left", fill="both", expand=True)

                scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
                scrollbar_y.pack(side="right", fill="y")

                scrollbar_x = ttk.Scrollbar(ventana_asignaciones, orient="horizontal", command=tree.xview)
                scrollbar_x.pack(side="bottom", fill="x")

                tree.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

                # Definir columnas
                columnas = [""] + [f"Oferta {i+1}" for i in range(len(ofertas))] + ["Gobierno"]
                tree["columns"] = columnas
                tree.heading("#0", text="")
                for col in columnas:
                    tree.heading(col, text=col)
                    tree.column(col, width=50, anchor='center')

                # Insertar filas
                for idx, fila in enumerate(asignaciones):
                    fila_label = f"{idx} acciones"

                    # Verifica si hay acciones sobrantes para el gobierno en este valor de idx
                    if idx == len(asignaciones) - 1:  # Última fila, que corresponde a las asignaciones sobrantes al gobierno
                        fila.append(asignacion_dinamica[-1])
                    else:
                        fila.append(0)  # No se asignaron acciones al gobierno para otros casos

                    valores = [fila_label] + fila
                    tree.insert("", "end", text="", values=valores)

                style = ttk.Style()
                style.configure("Custom.Treeview",
                                font=('Arial', 10),
                                rowheight=25,
                                bordercolor='black',
                                relief='solid')

                style.configure("Custom.Treeview.Heading",
                                font=('Arial', 10, 'bold'),
                                bordercolor='black',
                                relief='solid')

            # Función para ver la tabla de programación dinámica
            def ver_tabla_dp():
                # Obtener el número de acciones disponibles y el precio del gobierno
                A = int(acciones_var.get())
                precio_gobierno = int(precio_gobierno_var.get())

                # Ejecutar la programación dinámica y obtener las asignaciones
                asignacion_dinamica, valor_dinamico, dp, asignaciones = programacion_dinamica(A, ofertas, precio_gobierno)

                # Crear una nueva ventana para mostrar la tabla de programación dinámica
                ventana_dp = tk.Toplevel(root)
                ventana_dp.title("Tabla de Programación Dinámica - Solución Dinámica")
                ventana_dp.geometry("600x400")

                # Crear un frame para contener la tabla y los scrollbars
                frame_tabla = tk.Frame(ventana_dp)
                frame_tabla.pack(fill="both", expand=True)

                # Crear una tabla usando Treeview
                tree = ttk.Treeview(frame_tabla, style="Custom.Treeview", columns=["Acciones", "Valor"])
                tree.pack(side="left", fill="both", expand=True)

                # Agregar Scrollbar horizontal y vertical
                scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
                scrollbar_y.pack(side="right", fill="y")

                scrollbar_x = ttk.Scrollbar(ventana_dp, orient="horizontal", command=tree.xview)
                scrollbar_x.pack(side="bottom", fill="x")

                tree.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

                # Definir columnas: "Acciones" y "Valor DP"
                tree.heading("#0", text="")
                tree.heading("Acciones", text="Acciones")
                tree.heading("Valor", text="Valor DP")

                tree.column("Acciones", anchor='center', width=100)
                tree.column("Valor", anchor='center', width=100)

                # Insertar los valores de dp en la tabla
                for idx, valor in enumerate(dp):
                    tree.insert("", "end", text="", values=(f"{idx}", valor))

                style = ttk.Style()
                style.configure("Custom.Treeview",
                                font=('Arial', 10),
                                rowheight=25,
                                bordercolor='black',
                                relief='solid')

                style.configure("Custom.Treeview.Heading",
                                font=('Arial', 10, 'bold'),
                                bordercolor='black',
                                relief='solid')


            # Botón para ver la tabla de asignaciones
            ttk.Button(root, text="Ver Tabla de Asignaciones", command=ver_tabla_asignaciones).grid(row=10, column=0, padx=5, pady=5, sticky="nsew")

            # Botón para ver la tabla de programación dinámica
            ttk.Button(root, text="Ver Tabla de Programación Dinámica", command=ver_tabla_dp).grid(row=10, column=1, padx=5, pady=5, sticky="nsew")
    
    # Botones en la ventana principal
    ttk.Button(root, text="Terminal Inteligente", command=abrir_terminal_inteligente, width=40, style="TButton").pack(pady=80)
    ttk.Button(root, text="Subasta Pública", command=abrir_subasta_publica, width=40, style="TButton").pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    crear_interfaz()
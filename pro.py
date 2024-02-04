import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Coordenadas de los routers

num_routers = 4
x_spacing = 150  # Ajusta el espaciado horizontal
router_positions = {f'Router{i+1}': (x_spacing * (i+1), 150) for i in range(num_routers)}

# Información de enrutamiento para cada router
router_info = {
    'Router1': {'Nombre': 'Router1', 'Tipo de Enrutamiento': 'Estático', 'Direccion de Red': '192.168.1.0', 'Mascara de Subred': '255.255.255.0', 'Gateway': '192.168.1.1', 'Interfaz de Red': 'eth0', 'Saltos': 1, 'Conexiones': ['Router2', 'Router3', 'Router4'], 'Encendido': True},
    'Router2': {'Nombre': 'Router2', 'Tipo de Enrutamiento': 'Dinámico', 'Direccion de Red': '192.168.2.0', 'Mascara de Subred': '255.255.255.0', 'Gateway': '192.168.2.1', 'Interfaz de Red': 'eth0', 'Saltos': 1, 'Conexiones': ['Router1', 'Router3', 'Router4'], 'Encendido': True},
    'Router3': {'Nombre': 'Router3', 'Tipo de Enrutamiento': 'Estático', 'Direccion de Red': '192.168.3.0', 'Mascara de Subred': '255.255.255.0', 'Gateway': '192.168.3.1', 'Interfaz de Red': 'eth0', 'Saltos': 1, 'Conexiones': ['Router1', 'Router2', 'Router4'], 'Encendido': True},
    'Router4': {'Nombre': 'Router4', 'Tipo de Enrutamiento': 'Dinámico', 'Direccion de Red': '192.168.4.0', 'Mascara de Subred': '255.255.255.0', 'Gateway': '192.168.4.1', 'Interfaz de Red': 'eth0', 'Saltos': 1, 'Conexiones': ['Router1', 'Router2', 'Router3'], 'Encendido': True},
}

def toggle_router(event):
    # Obtener el nombre del router seleccionado
    selected_router = event.widget.find_closest(event.x, event.y)
    selected_router_name = canvas.gettags(selected_router)[0]

    # Cambiar el estado de encendido/apagado
    router_info[selected_router_name]['Encendido'] = not router_info[selected_router_name]['Encendido']

    # Actualizar la representación visual
    mostrar_routers()
    mostrar_tabla()

def mostrar_routers():
    # Limpiar canvas antes de mostrar routers
    canvas.delete("all")

    for router, position in router_positions.items():
        # Cargar imagen y redimensionar
        image_path = 'router1.jpg' if router_info[router]['Encendido'] else 'router1.jpg'
        pil_image = Image.open(image_path)
        new_size = (100, 250)  # Ajusta el tamaño deseado
        pil_image.thumbnail(new_size)
        tk_image = ImageTk.PhotoImage(pil_image)
        router_images[router] = tk_image

        # Mostrar imagen y texto
        canvas.create_image(position[0], position[1], anchor=tk.NW, image=tk_image, tags=(router,))
        canvas.create_text(position[0] + new_size[0] // 2, position[1] + new_size[1] // 2, text=router, fill="white")

        # Dibujar conexiones
        conexiones = router_info[router]['Conexiones']
        for conexion in conexiones:
            if router_info[router]['Encendido'] and router_info[conexion]['Encendido']:
                start_pos = router_positions[router]
                end_pos = router_positions[conexion]
                canvas.create_line(
                    start_pos[0] + new_size[0] // 2, start_pos[1] + new_size[1] // 2,
                    end_pos[0] + new_size[0] // 2, end_pos[1] + new_size[1] // 2, fill="black"
                )

def mostrar_tabla():
    # Limpiar la tabla antes de mostrarla
    for widget in table_frame.winfo_children():
        widget.destroy()

    # Mostrar tabla solo si algún router está encendido
    routers_encendidos = [router for router, info in router_info.items() if info['Encendido']]
    if routers_encendidos:
        # Crear Treeview
        tree = ttk.Treeview(table_frame, columns=tuple(router_info['Router1'].keys()), show='headings')

        # Configurar encabezados
        for col in tree['columns']:
            tree.heading(col, text=col)

        # Insertar datos en la tabla solo para routers encendidos
        for router in routers_encendidos:
            info = router_info[router]
            tree.insert('', tk.END, values=list(info.values()))

        # Ajustar el ancho de las columnas
        for col in tree['columns']:
            tree.column(col, width=90)  # Ajusta el ancho de las columnas según sea necesario

        # Agregar Scrollbar
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        vsb.pack(side='right', fill='y')
        tree.configure(yscrollcommand=vsb.set)

        tree.pack(fill='both', expand=True)

# Crear ventana principal
root = tk.Tk()
root.title("Simulación de Routers interconectados")

# Crear un lienzo para los routers
canvas = tk.Canvas(root, width=890, height=500)
canvas.pack()

# Diccionario para almacenar imágenes
router_images = {}

# Mostrar routers inicialmente
mostrar_routers()

# Asociar evento para apagar/encender router al hacer clic en él
canvas.tag_bind("all", "<ButtonRelease-1>", toggle_router)

# Crear el marco para la tabla
table_frame = ttk.Frame(root)
table_frame.place(x=10, y=300, width=880, height=130)

# Mostrar tabla inicialmente
mostrar_tabla()

title_label = tk.Label(root, text="Proyecto De Redes", font=("Arial", 16, "bold"))
title_label.place(relx=0.5, rely=0.05, anchor="center")

logo_image_path = 'logo.png'  # Reemplaza con la ruta de tu imagen de logo
logo_image = Image.open(logo_image_path)
logo_image.thumbnail((150, 150))  # Ajusta el tamaño según sea necesario
tk_logo_image = ImageTk.PhotoImage(logo_image)

logo_label = tk.Label(root, image=tk_logo_image)
logo_label.place(x=10, y=10)

# Iniciar el bucle de la aplicación
root.mainloop()

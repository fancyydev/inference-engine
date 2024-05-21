from tkinter import *
from tkinter import ttk
 
cc_list = []
n_list = []
meta_list = []
bh_list = []
r_list = []

def reset_lists():
    global cc_list
    global n_list
    global meta_list
    global bh_list
    global r_list
    
    cc_list.clear()
    n_list.clear()
    meta_list.clear()
    bh_list.clear()
    r_list.clear()
    
def prepare_lists(list, type = None):
    second = []
    juntar = ""
    if type == "r":
        for i in list:  
            antecedentes = i[0]
            conclusion = i[1]
            juntar = antecedentes + "->" + conclusion
            second.append(juntar)
    else:
        for i in list:
            for j in i:
                antecedentes = j[0]
                conclusion = j[1]
                juntar += antecedentes + "->" + conclusion + ","
            second.append(juntar)
            juntar = ""
    return second

def get_bc():
    bc = []
    with open('base_conocimientos.txt', 'r') as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            linea  = linea.strip() #Elimina los espacios en blanco
            linea = linea.replace(",","")
            partes = linea.split(":")
            antecedentes = partes[0]
            consecuente = partes[1]
            bc_aux = [antecedentes,consecuente]
            bc.append(bc_aux)
            #print(linea)
    #print(bc)
    return bc

#[['abc','d'],]
def equiparar(bc=None, bh=None, meta = None, type = None):
    cc = []
    if type == "back":
        for regla in bc:
            meta_regla = regla[1]
            if meta in meta_regla:
                cc.append(regla)
    else:
        for regla in bc:
            ban = True
            antecedentes = regla[0]
            cant_antecedentes = len(antecedentes)
            cont = 0
            for hecho in bh:
                if hecho in antecedentes:
                    cont += 1    
                if cont == cant_antecedentes:
                    cc.append(regla)
                    break
    return cc
    

def forward_chaining(meta, hechos_iniciales):
    global cc_list
    global n_list
    global meta_list
    global bh_list
    global r_list
    
    basic_knowledge = get_bc()
    bh = hechos_iniciales
    cc = equiparar(basic_knowledge,bh)
    print("------")
    print(cc)
    cc_list.append(cc.copy())
    while len(cc)>0 and meta not in bh:
        r = cc[0]
        r_list.append(r)
        #Eliminamos de cc
        cc.remove(r)
        #Eliminamos de basic knowledge para no seguir obteniendo esa regla
        basic_knowledge.remove(r)
        
        nh = r[1]
        n_list.append(nh)
        
        #Actualizar bh
        if (nh not in bh):
            bh += nh
            bh_list.append(bh)
        #
        if meta not in bh:
            cc = equiparar(basic_knowledge,bh)
            cc_list.append(cc.copy())
        
    if meta in bh:
        print(bh)
        print("Exito")
        return True
    else:
        print(bh)
        print("Fracaso")
        return False
        
def backward_chaining(meta, bh):
    global cc_list
    global n_list
    global meta_list
    global bh_list
    global r_list
    
    basic_knowledge = get_bc()
    verificado = False
    if meta in bh:
        return True
    else:
        cc = equiparar(bc=basic_knowledge,meta=meta, type="back")
        while(len(cc)>0 and verificado == False):
            r = cc[0]
            r_list.append(r)
            cc_list.append(cc.copy())
            #Eliminamos de cc
            cc.remove(r)
            #Obtenemos los antecedentes
            nm = list(r[0])
            n_list.append(r[0])
            
            verificado = True
            while len(nm)>0 and verificado:
                meta = nm[0]
                meta_list.append(meta)
                nm.remove(meta)
                verificado = backward_chaining(meta,bh)
                if verificado:
                    if (meta not in bh):
                        bh += meta
                        bh_aux = bh_list[len(bh_list)-1] + meta
                        bh_list.append(bh_aux)
        return verificado
# #Forward ------------------------------------
# bh_list = ['abf']
# meta_list.append('h')    
# forward_chaining('h','abf')

# print(bh_list)
# print(n_list)

# cc_list = prepare_lists(cc_list)
# print(cc_list)
# r_list = prepare_lists(r_list,"r")
# print(r_list)
# print(meta_list)

# reset_lists()
# Backward--------------------------------------
#print("-----------------------------")
# bh_list = ['abf']
# meta_list.append('h')
# if backward_chaining('h', 'abf'):
#     bh_aux = bh_list[len(bh_list)-1] + 'h'
#     bh_list.append(bh_aux)
#     print(bh_list)
#     print(n_list)
#     cc_list = prepare_lists(cc_list)
#     print(cc_list)
#     r_list = prepare_lists(r_list,"r")
#     print(r_list)
#     print(meta_list)
#     print("Exito hacia atras")
# else:
#     print("Fracaso hacia atras")
def actualizar_posicion_label(exito):
    if exito:
        # Coordenadas para el éxito
        msgBoolean.set("EXITO")
        msg_exito.config(bg='Green')
        x, y = 430, 167
    else:
        # Coordenadas para el fracaso
        msgBoolean.set("FRACASO")
        msg_exito.config(bg='OrangeRed1')
        x, y = 390, 167
    msg_exito.place(x=x, y=y)

# Función para actualizar el Treeview con los valores de las listas globales
def update_treeview():
    global cc_list
    global n_list
    global meta_list
    global bh_list
    global r_list
    lens = []
    lens.append(len(cc_list))
    lens.append(len(n_list))
    lens.append(len(meta_list))
    lens.append(len(bh_list))
    lens.append(len(r_list))
    lens.sort(reverse=True)
    max_range = lens[0]

    cc_list = prepare_lists(cc_list)
    r_list = prepare_lists(r_list,"r")
    
    print(cc_list)
    print(n_list)
    print(meta_list)
    print(r_list)
    print(bh_list)
    # Limpiar el Treeview antes de agregar nuevos elementos
    for item in tv.get_children():
        tv.delete(item)
    
    # Insertar valores de las listas globales en el Treeview
    for i in range(max_range):
        cc = cc_list[i] if i < len(cc_list) else ""
        n = n_list[i] if i < len(n_list) else ""
        meta = meta_list[i] if i < len(meta_list) else ""
        r = r_list[i] if i < len(r_list) else ""
        bh = bh_list[i] if i < len(bh_list) else ""
        
        tv.insert("", END, values=(cc, n, meta, r, bh))

def button_forward():
    global meta_list
    global bh_list
    meta = meta_entry.get()
    base_hechos = bh_entry.get()
    bh_list = [base_hechos]
    meta_list.append(meta)    
    actualizar_posicion_label(forward_chaining(meta,base_hechos))
    update_treeview()
    reset_lists()
    
def button_backward():
    global cc_list
    global n_list
    global meta_list
    global bh_list
    global r_list
    meta = meta_entry.get()
    base_hechos = bh_entry.get()
    bh_list = [base_hechos]
    meta_list.append(meta)
    if backward_chaining(meta, base_hechos):
        bh_aux = bh_list[len(bh_list)-1] + meta
        bh_list.append(bh_aux) 
        cc_list = prepare_lists(cc_list)
        r_list = prepare_lists(r_list,"r")
    
        #Insertar en la tabla
        print("Exito hacia atras")
    else:
        print("Fracaso hacia atras")
     
    reset_lists()
    
    

#INTERFAZ------------------------------------------------------------------------------
def validate_input(action, value_if_allowed, text, value_before, text_after, flag):
    # Permitir solo una letra
    if action == '1':  # Si se intenta escribir (insertar texto)
        return len(value_if_allowed) == 1 and text.isalpha()
    return True

root = Tk()
root.geometry("1000x650")
root.configure(bg="Black")
root.title("INFERENCE ENGINE")

Label(root, text="INFERENCE ENGINE", font=("Helvetica", 25), bg='white smoke').pack(pady=(10,0))
Label(root, text='fancydev', font=('Helvetica', 18), bg='white smoke').pack(side=BOTTOM, pady=(0,10))

#Label no te permite modificar el texto de la aplicacion
Label(root, text ="Ingresa la meta:", font = ('Derive Unicode', 18), bg ='white smoke').place(x=150,y=100)

# Variable para Entry
Msg = StringVar()
# Configurar validación
vcmd = (root.register(validate_input), '%d', '%P', '%S', '%s', '%V', '%M')
# Entry Field centrado y con validación
meta_entry = Entry(root, textvariable=Msg, width=2, font=('Derive Unicode', 18), justify='center', validate='key', validatecommand=vcmd)
meta_entry.place(x=340, y=100, width=50, height=34)

#Label no te permite modificar el texto de la aplicacion
Label(root, text ="Ingresa la base de hechos: ", font = ('Derive Unicode', 18), bg ='white smoke').place(x=405,y=100)

# Variable para Entry
Msg2 = StringVar()
# Configurar validación
bh_entry = Entry(root, textvariable=Msg2, width=2, font=('Derive Unicode', 18), justify='center')
bh_entry.place(x=720, y=100, width=130, height=34)

Button(root, text = "FORWARD" , font = ('Derive Unicode', 25), command=lambda:button_forward()).place(x = 150, y = 160)
Button(root, text = 'BACKWARD', font=('Derive Unicode', 25), command=lambda:button_backward()).place(x = 625 , y = 160)

msgBoolean = StringVar()
# x = 430, y = 167 Exito x = 390, y = 167 Fracaso
msg_exito = Label(root, textvariable=msgBoolean, font = ('Derive Unicode', 30))
#msg_fracaso = Label(root, textvariable=msgBoolean, font = ('Derive Unicode', 30), bg ='white smoke').place(x=430, y=167)


tv = ttk.Treeview(root, columns=("cc", "n", "meta", "r", "bh"))

tv.column("#0", width=0, stretch=NO)  # Ocultar columna #0
tv.column("cc", width=180)
tv.column("n", width=180)
tv.column("meta", width=180)
tv.column("r", width=180)
tv.column("bh", width=180)

tv.heading("#0", text="", anchor=CENTER)  # Encabezado vacío para la columna #0
tv.heading("cc", text="CC", anchor=CENTER)
tv.heading("n", text="N(H/M)", anchor=CENTER)
tv.heading("meta", text="META", anchor=CENTER)
tv.heading("r", text="R", anchor=CENTER)
tv.heading("bh", text="BH", anchor=CENTER)

# Empaquetar el Treeview
tv.pack(pady=200)

# Empaquetar el Treeview
tv.pack(pady=200)

root.mainloop()
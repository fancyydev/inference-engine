from tkinter import *
from tkinter import ttk
 
cc_list = []
n_list = []
goal_list = []
bh_list = []
r_list = []

def reset_lists():
    global cc_list
    global n_list
    global goal_list
    global bh_list
    global r_list
    
    cc_list.clear()
    n_list.clear()
    goal_list.clear()
    bh_list.clear()
    r_list.clear()
    
def prepare_lists(list, type = None):
    second = []
    combine = ""
    if type == "r":
        for i in list:  
            antecedents = i[0]
            conclusion = i[1]
            combine = antecedents + "->" + conclusion
            second.append(combine)
    else:
        for i in list:
            for j in i:
                antecedents = j[0]
                conclusion = j[1]
                combine += antecedents + "->" + conclusion + ","
            second.append(combine)
            combine = ""
    return second

def get_bc():
    bc = []
    with open('base_conocimientos.txt', 'r') as archivo:
        lines = archivo.readlines()
        for line in lines:
            line  = line.strip() #Elimina los espacios en blanco
            line = line.replace(",","")
            parts = line.split(":")
            antecedents = parts[0]
            consecuent = parts[1]
            bc_aux = [antecedents,consecuent]
            bc.append(bc_aux)
    return bc

#[['abc','d'],]
def compare(bc=None, bh=None, goal = None, type = None, padre = None):
    cc = []
    ban = False
    if type == "back":
        for rule in bc:
            goal_rule = rule[1]
            if goal in goal_rule:
                ban = False
                if padre != None and padre in rule[0]:
                    ban = True
                cc.append(rule)
        
        if ban == True:
            return -1
    else:
        for rule in bc:
            ban = True
            antecedents = rule[0]
            num_antecedents = len(antecedents)
            count = 0
            for fact in bh:
                if fact in antecedents:
                    count += 1    
                if count == num_antecedents:
                    cc.append(rule)
                    break
    return cc
    

def forward_chaining(goal, initial_facts):
    global cc_list
    global n_list
    global goal_list
    global bh_list
    global r_list
    basic_knowledge = get_bc()
    bh = initial_facts
    cc = compare(basic_knowledge,bh)
    cc_list.append(cc.copy())
    while len(cc)>0 and goal not in bh:
        r = cc[0]
        r_list.append(r)
        #Eliminamos de cc
        cc.remove(r)
        #Eliminamos de basic knowledge para no seguir obteniendo esa rule
        basic_knowledge.remove(r)
        nh = r[1]
        n_list.append(nh)
        #Actualizar bh
        if (nh not in bh):
            bh += nh
            bh_list.append(bh)
        if goal not in bh:
            cc = compare(basic_knowledge,bh)
            cc_list.append(cc.copy())
        
    if goal in bh:
        print("Exito")
        return True
    else:
        print("Fracaso")
        return False
        
def backward_chaining(goal, bh):
    global cc_list
    global n_list
    global goal_list
    global bh_list
    global r_list
    
    basic_knowledge = get_bc()
    verified = False
    if goal in bh:
        return True
    else:
        cc = compare(bc=basic_knowledge,goal=goal, type="back")
        while(len(cc)>0 and verified == False):
            #Verificar que los antecedents no dependan de la rule
            if len(cc) > 0:
                for i in cc[0][0]:
                    if i not in bh:
                        comp = compare(bc=basic_knowledge,goal=i, type="back", padre=goal)
                        if comp == -1:
                            basic_knowledge.remove(cc[0])
                            cc.remove(cc[0])
                            break
            if len(cc)>0:
                r = cc[0]
                r_list.append(r)
                cc_list.append(cc.copy())
                #Eliminamos de cc
                cc.remove(r)
                #Obtenemos los antecedents
                nm = list(r[0])
                n_list.append(r[0])
                
                verified = True
                while len(nm)>0 and verified:
                    goal = nm[0]
                    goal_list.append(goal)
                    nm.remove(goal)
                    verified = backward_chaining(goal,bh)
                    if verified:
                        if (goal not in bh):
                            bh += goal
                            bh_aux = bh_list[len(bh_list)-1] + goal
                            bh_list.append(bh_aux)
            else:
                print("Tu base de conocimiento genera recursividad")
        return verified

def update_position_label(succes):
    if succes:
        # Coordenadas para el éxito
        msgBoolean.set("SUCCES")
        msg_succes.config(bg='Green')
        x, y = 405, 167
    else:
        # Coordenadas para el fracaso
        msgBoolean.set("FAILURE")
        msg_succes.config(bg='OrangeRed1')
        x, y = 405, 167
    msg_succes.place(x=x, y=y)

# Función para actualizar el Treeview con los valores de las listas globales
def update_treeview():
    global cc_list
    global n_list
    global goal_list
    global bh_list
    global r_list
    lens = []
    lens.append(len(cc_list))
    lens.append(len(n_list))
    lens.append(len(goal_list))
    lens.append(len(bh_list))
    lens.append(len(r_list))
    lens.sort(reverse=True)
    max_range = lens[0]

    cc_list = prepare_lists(cc_list)
    r_list = prepare_lists(r_list,"r")

    # Limpiar el Treeview antes de agregar nuevos elementos
    for item in tv.get_children():
        tv.delete(item)
    
    # Insertar valores de las listas globales en el Treeview
    for i in range(max_range):
        cc = cc_list[i] if i < len(cc_list) else ""
        n = n_list[i] if i < len(n_list) else ""
        goal = goal_list[i] if i < len(goal_list) else ""
        r = r_list[i] if i < len(r_list) else ""
        bh = bh_list[i] if i < len(bh_list) else ""
        
        tv.insert("", END, values=(cc, n, goal, r, bh))

def button_forward():
    global goal_list
    global bh_list
    goal = meta_entry.get()
    base_facts = bh_entry.get()
    bh_list = [base_facts]
    goal_list.append(goal)    
    update_position_label(forward_chaining(goal,base_facts))
    update_treeview()
    reset_lists()
    
def button_backward():
    global goal_list
    global bh_list
    goal = meta_entry.get()
    base_facts = bh_entry.get()
    bh_list = [base_facts]
    goal_list.append(goal)
    succes = backward_chaining(goal, base_facts)
    update_position_label(succes)
    if succes:
        bh_aux = bh_list[len(bh_list)-1] + goal
        bh_list.append(bh_aux) 
    update_treeview()
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
root.resizable(False, False)
root.title("INFERENCE ENGINE")

Label(root, text="INFERENCE ENGINE", font=("Helvetica", 25), bg='white smoke').pack(pady=(10,0))
Label(root, text='fancydev', font=('Helvetica', 18), bg='white smoke').pack(side=BOTTOM, pady=(0,10))

#Label no te permite modificar el texto de la aplicacion
Label(root, text ="Enter the goal: ", font = ('Derive Unicode', 18), bg ='white smoke').place(x=150,y=100)

# Variable para Entry
Msg = StringVar()
# Configurar validación
vcmd = (root.register(validate_input), '%d', '%P', '%S', '%s', '%V', '%M')
# Entry Field centrado y con validación
meta_entry = Entry(root, textvariable=Msg, width=2, font=('Derive Unicode', 18), justify='center', validate='key', validatecommand=vcmd)
meta_entry.place(x=340, y=100, width=50, height=34)

#Label no te permite modificar el texto de la aplicacion
Label(root, text ="Enter the fact base: ", font = ('Derive Unicode', 18), bg ='white smoke').place(x=475,y=100)

# Variable para Entry
Msg2 = StringVar()
# Configurar validación
bh_entry = Entry(root, textvariable=Msg2, width=2, font=('Derive Unicode', 18), justify='center')
bh_entry.place(x=720, y=100, width=130, height=34)

Button(root, text = "FORWARD" , font = ('Derive Unicode', 25), command=lambda:button_forward()).place(x = 150, y = 160)
Button(root, text = 'BACKWARD', font=('Derive Unicode', 25), command=lambda:button_backward()).place(x = 625 , y = 160)

msgBoolean = StringVar()
# x = 430, y = 167 Exito x = 390, y = 167 Fracaso
msg_succes = Label(root, textvariable=msgBoolean, font = ('Derive Unicode', 30))
#msg_fracaso = Label(root, textvariable=msgBoolean, font = ('Derive Unicode', 30), bg ='white smoke').place(x=430, y=167)


tv = ttk.Treeview(root, columns=("cc", "n", "goal", "r", "bh"))

tv.column("#0", width=0, stretch=NO) 
tv.column("cc", width=180)
tv.column("n", width=180)
tv.column("goal", width=180)
tv.column("r", width=180)
tv.column("bh", width=180)

tv.heading("#0", text="", anchor=CENTER) 
tv.heading("cc", text="CC", anchor=CENTER)
tv.heading("n", text="N(H/M)", anchor=CENTER)
tv.heading("goal", text="META", anchor=CENTER)
tv.heading("r", text="R", anchor=CENTER)
tv.heading("bh", text="BH", anchor=CENTER)

# Empaquetar el Treeview
tv.pack(pady=200)

root.mainloop()
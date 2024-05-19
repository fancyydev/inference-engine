
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
    basic_knowledge = get_bc()
    bh = hechos_iniciales
    cc = equiparar(basic_knowledge,bh)
    while len(cc)>0 and meta not in bh:
        r = cc[0]
        #Eliminamos de cc
        cc.remove(r)
        #Eliminamos de basic knowledge para no seguir obteniendo esa regla
        basic_knowledge.remove(r)
        
        nh = r[1]
        #Actualizar bh
        if (nh not in bh):
            bh += nh
        #
        if meta not in bh:
            cc = equiparar(basic_knowledge,bh)
            
    if meta in bh:
        print(bh)
        print("Exito")
    else:
        print(bh)
        print("Fracaso")
 
cc_list = []
nm_list = []
meta_list = []
bh_list = []

def backward_chaining(meta, bh):
    global cc_list
    global nm_list
    global meta_list
    global bh_list
    
    basic_knowledge = get_bc()
    verificado = False
    if meta in bh:
        print(bh)
        return True
    else:
        cc = equiparar(bc=basic_knowledge,meta=meta, type="back")
        while(len(cc)>0 and verificado == False):
            r = cc[0]
            #Eliminamos de cc
            cc.remove(r)
            #Obtenemos los antecedentes
            nm = list(r[0])
            verificado = True
            while len(nm)>0 and verificado:
                meta = nm[0]
                nm.remove(meta)
                verificado = backward_chaining(meta,bh)
                if verificado:
                    if (meta not in bh):
                        bh += meta
                        bh_list.append(meta)
        print(bh)
        return verificado
        
#forward_chaining('h','abf')
#print("-----------------------------")
bh_list = list('abf')
#if backward_chaining('h', 'ac'):
if backward_chaining('h', 'abf'):
    bh_list.append('h')
    print(bh_list)
    print("Exito hacia atras")
else:
    print("Fracaso hacia atras")
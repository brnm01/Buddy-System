import math

lista_memoria=[]
lista_proc_solicitados=[]

espaco_mais_requisitado = 0
tamanho_memoria_total= 0

#
#Classe Espaco_Memoria - inicio: onde começa o espaço de memoria
#                - fim: onde termina o espaço de memoria
#                - nome_proc: default: N - espaço memoria vazio
#                                        - nome do processo alocado no espaço 
class Espaco_Memoria:
  def __init__(self, inicio, fim, nome_proc):
    self.inicio = inicio 
    self.fim = fim       
    self.nome_proc = nome_proc 

# Função que inicializa o Buddy System
def inicia_buddy(tamanho_memoria):
    if (tamanho_memoria % 2 != 0):
        print("Memória não é multiplo de 2")
        return     
    
    global tamanho_memoria_total 
    tamanho_memoria_total = tamanho_memoria
    
    proc = Espaco_Memoria(0, tamanho_memoria, 'N')
    lista_memoria.append([proc.inicio, proc.fim, proc.nome_proc])
    print("Memoria iniciada de ", proc.inicio, " à ", proc.fim, ". nome_proc -", proc.nome_proc)

    return lista_memoria

#Calcula o espaço que esse processo ocuparia na memória, se mem_aloc=70 retorna fim=128 etc
def espaco_processo(mem_tam, mem_aloc):
    aux = mem_tam/2
    fim = 0
    while aux >= mem_aloc: 
        fim = int(aux) 
        aux = aux/2
    return fim

def multiplo(tam_proc):
    global tamanho_memoria_total 

    aux = tamanho_memoria_total*2
    while (aux != 0):
        aux = int(aux/2)
        if (aux == tam_proc):
            return 0
    return 1

def insere_lista_proc_solicitados(tam_processo):
    global espaco_mais_requisitado 
    global lista_proc_solicitados
    
    lista_proc_solicitados.append(tam_processo)

    #se existe apenas um elemento na minha lista meu espaço mais requisitado é ele.
    if (len(lista_proc_solicitados)== 1):
        espaco_mais_requisitado = lista_proc_solicitados[0]

    #limpa minha lista de solicitados se ficar mt grande (= 10) insere o processo que iria alocar, ele se torna o processo mais requisitado
    if (len(lista_proc_solicitados) >= 10):
        espaco_mais_requisitado = espaco_mais_requisitado.clear()
        lista_proc_solicitados.append(tam_processo)
        espaco_mais_requisitado = lista_proc_solicitados[0]

    return lista_proc_solicitados

def verifica_se_lista_sera_redividida(processo):
    global espaco_mais_requisitado
    global lista_proc_solicitados

    #é verificado se a quantidade de vezes que aparece esse tam_processo na lista é maior espaco_mais_requisitado, mudando assim quem é o elemento mais requisitado.
    if (lista_proc_solicitados.count(processo) > lista_proc_solicitados.count(espaco_mais_requisitado)):
        espaco_mais_requisitado = processo
        return 1
    else:
        return 0

#divide a memoria na pelas partes mais solicitadas de processos
def divide_ou_mergeia_espacos_memoria(lista_memoria, tam_processo):
    idx_d = 0
    
    while (idx_d != len(lista_memoria)):
        tam_mem = (lista_memoria[idx_d][1]) - (lista_memoria[idx_d][0])
        
        if (lista_memoria[idx_d][2] != "N"): #or (tam_processo > tam_mem)
            idx_d = idx_d + 1
        elif (tam_processo >= (tam_mem*2) and len(lista_memoria) != 1):
            #faz o merge de dois espaços de memória 
            tam_mem_dois_proc = (lista_memoria[idx_d-1][1] - lista_memoria[idx_d-1][0]) + (lista_memoria[idx_d][1] - lista_memoria[idx_d][0])

            if((multiplo(tam_mem_dois_proc) == 0) and (lista_memoria[idx_d-1][2] == 'N') and (tam_processo == tam_mem_dois_proc)):
                
                desaloca_proc = Espaco_Memoria((lista_memoria[idx_d-1][0]), (lista_memoria[idx_d][1]), 'N')
                
                lista_memoria.insert(idx_d+1, [desaloca_proc.inicio, desaloca_proc.fim, desaloca_proc.nome_proc]) 

                lista_memoria.pop(idx_d)
                lista_memoria.pop(idx_d-1)  
                print (" *  Memoria mergeada - inicio: ", desaloca_proc.inicio," - fim: ", desaloca_proc.fim, "tamanho: ", (desaloca_proc.fim- desaloca_proc.inicio))

                idx_d = 0
                continue

            idx_d = idx_d + 1
            continue
        else:
            if ((tam_mem/2) >= tam_processo):

                div1 = Espaco_Memoria ((lista_memoria[idx_d][0]), int(lista_memoria[idx_d][0] + (tam_mem /2)), 'N')
                div2 = Espaco_Memoria (int(lista_memoria[idx_d][0] + (tam_mem /2)), (lista_memoria[idx_d][1]), 'N')
                
                lista_memoria.insert(idx_d+1, [div1.inicio, div1.fim, div1.nome_proc])
                lista_memoria.insert(idx_d+2, [div2.inicio, div2.fim, div2.nome_proc])                
                lista_memoria.pop(idx_d)
                           
                idx_d = 0
            else:
                idx_d = idx_d + 1
    
    print("Memoria dividida/mergeada em espaços de:", tam_mem, "\n")
    return lista_memoria

#Aloca Processo quick fit
def aloca_quick_fit(nome_processo, tam_processo, lista_memoria):
    idx = 0
    alocado = "false"
    global tamanho_memoria_total 
    global espaco_mais_requisitado

    if (nome_processo == "N"):
        print("Nome do processo não pode ser 'N'.")
        return 

    #tenho o espaço de memmória que meu processo precisa
    espaco_que_proc_ocupa = espaco_processo(tamanho_memoria_total, tam_processo)

    #verifica se o espaço que o processo que eu quero alocar ocupa é maior que o tamanho da memória.
    if (espaco_que_proc_ocupa > tamanho_memoria_total):
        print("Tamanho do processo é maior que o tamanho da memória")
        return 

    #insere esse espaço na minha lista de requisições
    insere_lista_proc_solicitados(espaco_que_proc_ocupa)

    print ("\n lista_proc_solicitados =", lista_proc_solicitados)

    #verifica se a lista será dividida ou mergeada
    verica = verifica_se_lista_sera_redividida(espaco_que_proc_ocupa)

    if ((verica == 1) or (len(lista_memoria) == 1)):
        lista_memoria = divide_ou_mergeia_espacos_memoria(lista_memoria, espaco_que_proc_ocupa)   
        
    print ("\n Meu processo ",nome_processo, " de tamanho:", tam_processo ," ocupa um espaço de:", espaco_que_proc_ocupa)
    

    while (idx != len(lista_memoria)):

        tam_mem = (lista_memoria[idx][1]) - (lista_memoria[idx][0])
        
        if (lista_memoria[idx][2] != 'N'):
            idx = idx + 1
            continue

        elif (tam_mem == espaco_que_proc_ocupa):
        
            proc1 = Espaco_Memoria((lista_memoria[idx][0]), (lista_memoria[idx][1]), nome_processo)
            
            lista_memoria.insert(idx+1, [proc1.inicio, proc1.fim, proc1.nome_proc]) 
            lista_memoria.pop(idx)
            
            alocado = "true"

            print (" *\n Processo:", tam_processo ," alocado - inicio: ", proc1.inicio," - fim: ", proc1.fim, "- nome_proc:", proc1.nome_proc, " Tamanho do Espaço que o Processo foi alocado: ",  (proc1.fim - proc1.inicio)) 

            break

        elif (tam_processo < (tam_mem/2)):
            #divide o espaço de memoria em dois
            div1 = Espaco_Memoria ((lista_memoria[idx][0]), int(lista_memoria[idx][0] + (tam_mem /2)), 'N')
            div2 = Espaco_Memoria (int(lista_memoria[idx][0] + (tam_mem /2)), (lista_memoria[idx][1]), 'N')
            
            lista_memoria.insert(idx+1, [div1.inicio, div1.fim, div1.nome_proc])
            lista_memoria.insert(idx+2, [div2.inicio, div2.fim, div2.nome_proc])                
            lista_memoria.pop(idx)
            
            print (" * Memoria dividida - inicio: ", div1.inicio," - fim: ", div1.fim, "- nome_proc:", div1.nome_proc, "tamanho: ", (div1.fim- div1.inicio))
            print (" * Memoria dividida - inicio: ", div2.inicio," - fim: ", div2.fim, "- nome_proc:", div2.nome_proc, "tamanho: ", (div2.fim- div2.inicio))   
            
            idx = 0
        
        elif (espaco_que_proc_ocupa >= (tam_mem*2)):  
            #faz o merge de dois espaços de memória 
    
            tam_mem_dois_proc = (lista_memoria[idx-1][1] - lista_memoria[idx-1][0]) + (lista_memoria[idx][1] - lista_memoria[idx][0])
    
            if(multiplo(tam_mem_dois_proc) == 0  and (lista_memoria[idx-1][2]) == 'N'):
                
                desaloca_proc = Espaco_Memoria((lista_memoria[idx-1][0]), (lista_memoria[idx][1]), 'N')
                
                lista_memoria.insert(idx+1, [desaloca_proc.inicio, desaloca_proc.fim, desaloca_proc.nome_proc]) 

                lista_memoria.pop(idx)
                lista_memoria.pop(idx-1)  
                print (" *  Memoria mergeada - inicio: ", desaloca_proc.inicio," - fim: ", desaloca_proc.fim, "tamanho: ", (desaloca_proc.fim- desaloca_proc.inicio))

                idx = 0
                continue

            idx = idx + 1
            continue
        else:
            idx = idx + 1
            continue
    
    if (alocado != "true"):
        print("Espaço não encontrado para alocar")

    return lista_memoria

def desaloca(nome_processo, lista_memoria):
    idx = 0
    desalocado = "false"
    
    while (idx != len(lista_memoria)):
        tam_mem = (lista_memoria[idx][1]) - (lista_memoria[idx][0])

        if (lista_memoria[idx][2] == nome_processo):
        
            desaloca_proc = Espaco_Memoria((lista_memoria[idx][0]), (lista_memoria[idx][1]), 'N')
        
            lista_memoria.insert(idx+1, [desaloca_proc.inicio, desaloca_proc.fim, desaloca_proc.nome_proc]) 
            lista_memoria.pop(idx)          
            desalocado = "true"
            #continua verificando se vai aumentar a area de desalocamento
            idx = 0  
        else:
            if(lista_memoria[idx-1][2] == 'N' and (idx != 0) and (lista_memoria[idx][2] == 'N')):
                tam_mem_dois_proc = (lista_memoria[idx-1][1] - lista_memoria[idx-1][0]) + tam_mem 
                
                if(tam_mem_dois_proc % 2 == 0):
                    desaloca_proc2 = Espaco_Memoria((lista_memoria[idx-1][0]), (lista_memoria[idx][1]), 'N')
                    
                    lista_memoria.insert(idx+1, [desaloca_proc2.inicio, desaloca_proc2.fim, desaloca_proc2.nome_proc]) 
    
                    lista_memoria.pop(idx)
                    lista_memoria.pop(idx-1)  
                    
                    #continua verificando se vai aumentar a area de desalocamento
                    idx = 0  
                    continue
                
            idx = idx + 1
    
    if desalocado != "true":
        print ("Processo não encontrado para desalocar")
    else:
        print ("Processo:",nome_processo ," desalocado \n")
        
    return lista_memoria

def main():

    inicia_buddy(1024) #1024 KB é 1G
    print("lista 1: ", lista_memoria)
    
    aloca_quick_fit("P1", 70,lista_memoria)    
    print("lista 2: ", lista_memoria)

    aloca_quick_fit("P2", 35,lista_memoria)    
    print("lista 2: ", lista_memoria)

    #aloca_quick_fit("P3", 80,lista_memoria)    
    #print("lista 2: ", lista_memoria)
    
    #desaloca("P1", lista_memoria) 
    #print("lista 5: ", lista_memoria)      
    
    #aloca_quick_fit("P4", 60,lista_memoria)    
    #print("lista 2: ", lista_memoria)   
    
    #desaloca("P2", lista_memoria) 
    #print("lista 5: ", lista_memoria)    
    
    #desaloca("P4", lista_memoria) 
    #print("lista 6: ", lista_memoria)     
    
    #desaloca("P3", lista_memoria) 
    #print("lista 7: ", lista_memoria)   

    #

    #continua = 'Y'
    #tamanho_memoria_t = input("Digite o tamanho de memória inteiro em KB (1G = 1024KB): ")
    #inicia_buddy(int(tamanho_memoria_t)) #1024 KB é 1G

    #print("lista Iniciada:  ", lista_memoria)

    #while (continua == "Y" or continua == "y" and (tamanho_memoria_t > 0)):
    #    op = input ("\n Para alocar um processo na memória 'I', para desalocar um Processo 'D': ")

    #    if (op == "I" or op == "i"):
    #        nome_processo = input("\n Digite o nome do processo (Ex: P1, A), o nome 'N' é considerado inválido: ")
    #        tamanho_processo = input("\n Digite o tamanho do processo em KB: ")
            
    #        aloca_quick_fit(nome_processo, int(tamanho_processo) ,lista_memoria)    

    #        print("\n Lista após Alocamento = ", lista_memoria) 

    #    elif (op == "D" or op == "d"):
    #        nome_processo = input("\n Digite o nome do processo para o desalocamento: ")
            
    #        desaloca(nome_processo ,lista_memoria)    
    #        print("\n Lista após Desalocamento = ", lista_memoria) 

    #    continua = str(input("\n Deseja continuar inserindo ou removendo Processos? Y/N: "))    

main()     
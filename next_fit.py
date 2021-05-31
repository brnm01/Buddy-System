import math

lista_memoria=[]
tamanho_memoria_total= 0
#
#Classe Espaco_Memoria - inicio: onde começa a alocação/ espaço memoria
#                - fim: onde termina a alocação/ espaço memoria
#                - nome_proc: default: N - espaço memoria vazio
#                                        - nome do processo
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

#Processo alocado em next fit
count = 0
def aloca_next_fit(nome_processo, tam_processo, lista_memoria):
    global count 
    
    if (nome_processo == "N"):
        print("Nome do processo não pode ser 'N'.")
        return 

    if (count == len(lista_memoria)):
        count = 0
    idx = count
    
    while (idx != len(lista_memoria)):

        tam_mem = (lista_memoria[idx][1]) - (lista_memoria[idx][0])

        print("idx=", idx, " lista_memoria[idx]", lista_memoria[idx])
        if ((tam_processo > tam_mem) or (lista_memoria[idx][2] != 'N')):

            idx = idx + 1
            continue
        
        elif (tam_processo == tam_mem):
            
            proc1 = Espaco_Memoria((lista_memoria[idx][0]), (lista_memoria[idx][1]), nome_processo)
            
            lista_memoria.insert(idx+1, [proc1.inicio, proc1.fim, proc1.nome_proc]) 
            lista_memoria.pop(idx)   
            
            print (" *\n Processo:", tam_processo ,"- inicio: ", proc1.inicio," - fim: ", proc1.fim, "- nome_proc:", proc1.nome_proc, " Tamanho do Espaço que o Processo foi alocado: ",  (proc1.fim - proc1.inicio)) 
            count = count + 1
            break
        else:

            if ((tam_mem/2) >= tam_processo):
                div1 = Espaco_Memoria ((lista_memoria[idx][0]), int(lista_memoria[idx][0] + (tam_mem /2)), 'N')
                div2 = Espaco_Memoria (int(lista_memoria[idx][0] + (tam_mem /2)), (lista_memoria[idx][1]), 'N')
                
                lista_memoria.insert(idx+1, [div1.inicio, div1.fim, div1.nome_proc])
                lista_memoria.insert(idx+2, [div2.inicio, div2.fim, div2.nome_proc])

                lista_memoria.pop(idx)
                
                print (" * Memoria dividida - inicio: ", div1.inicio," - fim: ", div1.fim, "- nome_proc:", div1.nome_proc)
                print (" * Memoria dividida - inicio: ", div2.inicio," - fim: ", div2.fim, "- nome_proc:", div2.nome_proc)
                
                print (lista_memoria, "\n",)
                
                idx = count                
            else:
                proc2 = Espaco_Memoria((lista_memoria[idx][0]), (lista_memoria[idx][1]), nome_processo)
                
                lista_memoria.insert(idx+1, [proc2.inicio, proc2.fim, proc2.nome_proc]) 
                lista_memoria.pop(idx)

                print ("\n Processo:", tam_processo ,"alocado: - inicio: ", proc2.inicio," - fim: ", proc2.fim, "- nome_proc:", proc2.nome_proc, " Tamanho do Espaço que o Processo foi alocado: ",  (proc2.fim - proc2.inicio)) 
                count = count + 1
                break
            
    return lista_memoria
    
def multiplo(tam_proc):
    global tamanho_memoria_total 

    aux = tamanho_memoria_total*2
    while (aux != 0):
        aux = int(aux/2)
        if (aux == tam_proc):
            return 0
    return 1

#desaloca processo na memória
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
                
                if(multiplo(tam_mem_dois_proc) == 0):
                    
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

    inicia_buddy(1024) #1024 é 1G
    print("lista 1: ", lista_memoria)
    
    aloca_next_fit("P1", 70, lista_memoria)
    print("lista 2: ", lista_memoria)

    aloca_next_fit("P2", 70,lista_memoria)    
    print("lista 2: ", lista_memoria)
    
    #aloca_next_fit("P2", 35,lista_memoria)    
    #print("lista 2: ", lista_memoria)

    #aloca_next_fit("P3", 80,lista_memoria)    
    #print("lista 2: ", lista_memoria)
    
    #desaloca("P1", lista_memoria) 
    #print("lista 5: ", lista_memoria)      
    
    #aloca_next_fit("P4", 60,lista_memoria)    
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
            
    #        aloca_next_fit(nome_processo, int(tamanho_processo) ,lista_memoria)    

    #        print("\n Lista após Alocamento = ", lista_memoria) 

    #    elif (op == "D" or op == "d"):
    #        nome_processo = input("\n Digite o nome do processo para o desalocamento: ")
            
    #        desaloca(nome_processo ,lista_memoria)    
    #        print("\n Lista após Desalocamento = ", lista_memoria) 

    #    continua = str(input("\n Deseja continuar inserindo ou removendo Processos? Y/N: "))   

main()        
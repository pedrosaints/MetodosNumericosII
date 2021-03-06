import numpy as np
import math

def met_calc_J_deR( A, i, j, n):
    I = np.zeros((n,n))
    for k in range(n):
        I[k][k]=1
    J = I
    erro = 0.000001
    if (math.fabs(A[i][j]) < erro):
        return J
    if (math.fabs(A[j][j]) < erro):
        if(math.fabs(A[i][j]) < 0):
            teta = (math.pi)/2
        else:
            teta = -(math.pi)/2
    else:
        teta = (math.atan((-A[i][j])/(A[j][j])))/2
    J[i][i] = math.cos(teta)
    J[j][j] = math.cos(teta)
    J[i][j] = math.sin(teta)
    J[j][i] = -math.sin(teta)
    return J

def decomposicao_QR(A , n):
    I = np.zeros((n,n))
    for k in range(n):
        I[k][k]=1
    QT = I
    Rvelha = A
    for j in range(n-1):
        for i in range(j+1,n):
            Jij = met_calc_J_deR( Rvelha, i, j, n)
            Rnova = np.dot(Jij, Rvelha)
            Rvelha = Rnova
            QT = Jij.dot(QT)
    Q = QT.T
    R = Rnova
    return(Q,R)

def metodo_QR(A , n, erro):
    Lamb = np.zeros(n)
    val = 100
    I = np.zeros((n,n))
    for k in range(n):
        I[k][k]=1
    P = I
    Avelha = A
    while(val>erro):
        Aux = decomposicao_QR(Avelha , n)
        Q = Aux[0]
        R = Aux[1]
        Anova = np.dot(R,Q)
        Avelha = Anova
        P = P.dot(Q)
        val = verifica_diagonal(Anova,n)
    for j in range(n):
        Lamb[j] = Anova[j][j] 
    return(Anova,P,Lamb)
    ##P COLUNAS SAO AUTOVETORES
    ##LAMB VETOR DE AUTOVALORES

def met_calc_J( A, i, j, n):
    I = np.zeros((n,n))
    for k in range(n):
        I[k][k]=1
    J = I
    erro = 0.000001
    if (math.fabs(A[i][j]) < erro):
        return J
    if (math.fabs(A[i][i]-A[i][j]) < erro):
        teta = (math.pi)/4
    else:
        teta = (math.atan((-2*A[i][j])/(A[i][i]-A[i][j])))/2
    J[i][i] = math.cos(teta)
    J[j][j] = math.cos(teta)
    J[i][j] = math.sin(teta)
    J[j][i] = -math.sin(teta)
    return J

def varredura_jacobi(A , n):
    I = np.zeros((n,n))
    for k in range(n):
        I[k][k]=1
    J = I
    Avelha = A
    for j in range(n-1):
        for i in range(j+1,n):
            Jij = met_calc_J( Avelha, i, j, n)
            Anova = multiplica( multiplica(Jij.T, Avelha), Jij)
            Avelha = Anova
            J = J.dot(Jij)
    Ã = Anova
    return(Ã,J)
            
def metodo_jacobi(A , n, erro):
    Lamb = np.zeros(n)
    val = 100
    I = np.zeros((n,n))
    for k in range(n):
        I[k][k]=1
    P = I
    Avelha = A
    while(val>erro):
        Aux = varredura_jacobi(Avelha , n)
        Anova = Aux[0]
        #print('Varredura de Jacobi')
        #print(Anova)
        J = Aux[1]
        Avelha = Anova
        P = P.dot(J)
        val = verifica_diagonal(Anova,n)
    for j in range(n):
        Lamb[j] = Anova[j][j] 
    return(Anova,P,Lamb)
    ##P COLUNAS SAO AUTOVETORES
    ##LAMB VETOR DE AUTOVALORES

def met_calc_H( A, i, n):
    w = np.zeros(n)
    wlinha = np.zeros(n)
    e = np.zeros(n)
    for j in range(i+1,n):
        w[j] = A[j][i]
    Lw = comprimento(w)
    wlinha[i+1] = Lw
    N = w - wlinha
    no = N / comprimento(N)
    #criando identidade
    I = np.zeros((n,n))
    for j in range(n):
        I[j][j]=1
    aux = np.zeros((1,n))
    for j in range(n):
        aux[0][j] = no[j]
    H = I - 2 *(TranspostaVetor(no).dot(aux))
    return H
    
def met_householder(A,n):
    #H = I
    H = np.zeros((n,n))
    for j in range(n):
        H[j][j]=1
    A_ant = A
    for i in range(0,n-2):
        H_atual = met_calc_H( A_ant, i, n)
        A_atual = multiplica( multiplica(H_atual, A_ant), H_atual)
        A_ant = A_atual
        H = H.dot(H_atual)
    Ã = A_atual
    return(Ã,H)
    


def comprimento(w):
    return math.sqrt(sum( [ w.dot(w) ] ))


def verifica_diagonal(M,n):
    s = 0
    for i in range(n):
        for j in range(n):
            if i>j:
                s = s + math.pow(M[i][j],2)
    return s

def TranspostaVetor(vetor):
    n = len(vetor)
    T = np.zeros((n,1))
    for i in range(n):
        T[i][0]=vetor[i]
    return T
    
    n = len(matriz)
    T = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            T[i][j]=matriz[j][i]
    return T    

def multiplica(m1, m2):
    n = len(m1)
    if n != len(m2):
        print("erro dimensão")
        return None
    result = np.zeros((n,n))
    for i in range(n):
        for k in range(n):
            somatorio = 0
            for j in range(n):
                somatorio += m1[i][j] * m2[j][k]
            result[i][k] = somatorio
    return result

    
A = np.array([[40,8,4,2,1],[8,30,12,6,2],[4,12,20,1,2],[2,6,1,25,4],[1,2,2,4,5]])
print('MATRIZ:')
print(A)

print('QUESTAO 1')
print('METODO QR')
metodoQR = metodo_QR(A , 5, 0.000001)
print('')
print('Ã: ')
print(metodoQR[0])
print('')
print('P: ')
print(metodoQR[1])
print('')
print('LAMB: ')
print(metodoQR[2])
print('')
print('')
print('PARES AUTOVALOR E AUTOVETOR')
print('')
for p in range(5):
    print('Autovalor: ')
    print(metodoQR[2][p])
    print('Autovetor: ')
    print(metodoQR[1].T[p])
    print('')
    print('TESTE')
    print(np.dot(A,metodoQR[1].T[p]))
    print(np.dot(metodoQR[2][p],metodoQR[1].T[p]))
    print('')

print('')
print('METODO DE Jacobi')
metodoJ = metodo_jacobi(A , 5, 0.000001)
print('')
print('Ã: ')
print(metodoJ[0])
print('')
print('P: ')
print(metodoJ[1])
print('')
print('LAMB: ')
print(metodoJ[2])
print('PODEMOS NOTAR QUE EM JACOBI OS AUTOVALORES ESTAO EM ORDEM CRESCENTE, JÁ NO QR EM ORDEM DESCRESCENTE')
print('')
print('')

print('')
print('')
print('QUESTAO 2')
print('METODO DE HOUSEHOLDER')
metodoHH = met_householder(A,5)
print('')
print('Ã: ')
print(metodoHH[0])
print('')
print('H: ')
print(metodoHH[1])
print('')
print('METODO DE QR')
metodoQRHH = metodo_QR(metodoHH[0] , 5, 0.000001)
print('')
print('Ã: ')
print(metodoQRHH[0])
print('')
print('LAMB: ')
print(metodoQRHH[2])
print('')
print('P obtido: ')
print(metodoQRHH[1])
print('')
print('P com autovetores corretos: ')
print(metodoQR[1])
print('')
print('H * P obtido: ')
print(np.dot(metodoHH[1],metodoQRHH[1]))



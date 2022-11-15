from os import system, name
from tworzenie_danych import roz_plaski

def m_c(fx, a, b, n):
    # metoda monte carlo
    losx = roz_plaski(a,b,n)
    wyn = [] 
    for i in losx:
        wyn.append(fx(i))
    losy = roz_plaski(min(wyn),max(wyn), n)
    L = 0
    for i in range(n):
        if wyn[i] > 0 and losy[i] < wyn[i]:
            L += 1 
        elif wyn[i] <= 0 and losy[i] > wyn[i]:
            L -= 1
    pole = L/n*(b-a)*(max(wyn)-min(wyn))
    return pole
        
def fx2(x):
    # losowa funkcja x^2 zeby sprawdzic czy m_c() dziala
    return x*x

def riemanns(fx, a, b, n):
    delta = (b-a)/n
    pole = 0
    for i in range(n):
        pole += fx(delta*i)*delta
    return pole


def dowolna_figura(punkty, n):
    """UWAGA; funkcja dziala dla kazdego 3+kata po warunkiem ze nie ma dwoch sasiadujacych punktow jeden pod drugim np. [0,0],[0,1],..."""
    # punkty - lista koordynatów punktów [[X,Y],...] - musza byc podane jednen po drugim (punkty)
    # n - ilosc "strzalów" monte carlo
    if len(punkty) < 3:
        return 'Nie ma opcji na obliczenie pola :)'
    a,b = [],[]
    # ustalenie granic na podstawie najodleglejszych punktow (jak podamy prostokat rownolegly do osi x,y to monte carlo zawsze bedzie trafiac)
    minx = punkty[0][0]
    maxx = punkty[0][0]
    miny = punkty[0][1]
    maxy = punkty[0][1]
    for i in range(len(punkty)):
        if minx > punkty[i][0]:
            minx = punkty[i][0]
        if maxx < punkty[i][0]:
            maxx = punkty[i][0]
        if miny > punkty[i][1]:
            miny = punkty[i][1]
        if maxy < punkty[i][1]:
            maxy = punkty[i][1]
        # wyliczenie a i b (równania prostych) dla kazdej pary punktów (znow wazna kolejnosc)
        if punkty[i][0] == punkty[i-1][0]:
            a.append(0)
        else:
            a.append((punkty[i][1]-punkty[i-1][1])/(punkty[i][0]-punkty[i-1][0]))
        b.append(punkty[i][1] - a[i]*punkty[i][0])
    L = 0 # to beda trafione strzaly
    losy = roz_plaski(miny, maxy, n)    # zlaczam dwa zbiory z rozkladu plaskiego jako strzaly w osi y
    losx = roz_plaski(minx, maxx, n)    # i osi x
    for l in range(len(losx)): # dla kazdego strzalu
        for i in range(len(punkty)):    # posrod podanych punktow 
            if ( punkty[i][0] <= losx[l] and punkty[i-1][0] >= losx[l] ) or ( punkty[i][0] >= losx[l] and punkty[i-1][0] <= losx[l] ): # szukam dwoch pomiedzy ktorymi znajdzie sie strzal 
                for j in range(len(punkty)): # a potem szukam drugiej takiej pary 
                    if i == j: # innej od poprzedniej
                        pass
                    elif ( punkty[j][0] <= losx[l] and punkty[j-1][0] >= losx[l] ) or ( punkty[j][0] >= losx[l] and punkty[j-1][0] <= losx[l] ): # tutaj ją znajduje - w ten sposob wiem ze punkt jest pomiedzy rownaniami tych dwoch par punktow
                        if (a[i]*losx[l] + b[i] >= losy[l] and a[j]*losx[l] +b[j] <= losy[l]) or (a[i]*losx[l] + b[i] <= losy[l] and a[j]*losx[l] +b[j] >= losy[l]): # sprawdzam czy jest pomiedzy dwoma rownosciami
                            L+=1    # jezeli tak to strzal trafiony :)
                    break   # jezeli nie to znaczy ze strzal jest poza figura :(
    return abs(L/n*(minx-maxx)*(miny-maxy))

if __name__ == "__main__":
    # czyszczenie terminala 
    system('clear' if name=='posix' else 'cls')

    mc = m_c(fx2, 0, 2, 100000)
    ri = riemanns(fx2, 0, 2, 100000)
    print("Monte Carlo: " +str(mc))
    print("Riemanns: "+str(ri))
    print("Roznica miedzy nimi: "+str(abs(mc-ri)))
    punkciki = [[0,0],[1,2],[2,2],[1,-2]]
    print(f"Pole figury okreslonej punktami {punkciki} wynosi: {dowolna_figura(punkciki, 10000)}")
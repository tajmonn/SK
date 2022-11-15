import json
from scipy.stats import kurtosis, chi2, chisquare, shapiro, ks_2samp
import matplotlib.pyplot as plt
import seaborn as sb
from os import system, name
from tworzenie_danych import roz_plaski

#READ_ME
"""Ten plik był przesyłany z zajęć na zajęcia więc wysyłam go również w ostatnim zipie (żeby nie było, 
że po 3 tygodniach nagle zniknał), ale jako że uważam że jest w nim niezły bajzel to podzielilem go na 
4 Tygodnie - osobne pliki gdzie łatwiej zrozumiec co sie dzialo i dlaczego. Niektóre tygodnie korzystaja 
z poprzednich wiec funkcje sa importotowane zamiast kopiowane - dlatego moze byc wymagane posiadanie 
wszystkich w jednym folderze, gdy chcemy je uruchomic"""


# czyszczenie terminala 
system('clear' if name=='posix' else 'cls')

def zaladowanie_danych(filename):
    # funkcja do zaladowywania danych z pliku
    with open(filename, 'r') as f:
        dane = json.load(f)
    return dane

def srednia(dane):
    # oblicza srednia
    return (sum(dane)/len(dane))

def mediana(dane):
    # oblicza mediane na podstawie srodkowych elementow w posortowanej liscie
    n_dane = sorted(dane)
    if len(n_dane)%2 == 0:
        wynik = (n_dane[len(dane)//2] + n_dane[len(dane)//2 -1]) / 2
    else:
        wynik = (n_dane[len(dane)//2])
    return wynik

def odchylenie_std(dane):
    # oblicza odchylenie standardowe
    suma = 0
    sre = srednia(dane)
    for i in dane:
        suma += (i - sre) ** 2
    suma /= len(dane)
    suma = suma ** (0.5)
    return suma

def skosnosc(dane):
    # oblicza skosnosc na podstawie wzoru 3*(srednia arytmetycczna - mediana)/odchylenie standardowe
    wynik = 3* ( srednia(dane) - mediana(dane))/ odchylenie_std(dane)
    return wynik

def kurtoza(dane):
    # oblicza kurtoze z funkcja z biblioteki scipy
    return kurtosis(dane)

def tworzenie_wykresu(dane, nazwa):
    # tworzy histogramy liiniowe i zapisuje je w .png bo nie zainstalowalem tkinter-a
    # sb.distplot(dane, hist = False, kde = True) <- stara funkcja (wyrzuca informacje ze jest przestarzala i ja wylaczaja)
    sb.scatterplot(dane)
    plt.savefig(f"{nazwa}.png")
    plt.clf()

def chi_kwadrat(dane):
    # robienie testu chi kwadrat ze wzoru z wikipedi (suma((wartosc - srednia)**2)/srednia)
    sre = srednia(dane)
    test = 0
    for i in dane:
        test += ((i-sre)**2)/sre
    swoboda = len(dane) - 1
    wart_kryt = chi2.ppf(0.95, df = swoboda)
    # jezeli wart_kryt bedzie wieksza niz test to nie mamy powodow do odrzucenia hipotezy 0 (ktorych dotyczy test)
    if wart_kryt > test:
        print("Nie ma powodu by odrzucic hipoteze, ze dane sa rozkladem plaskim na poziomie istotnosci 0.05")
    else:
        print("Nie jest to rozklad plaski na poziomie istotnosci 0.05")
    print("Wartosc statystyki testowej: ",test)
    print("Wartosc statystyki testowej dla scipy: ",chisquare(dane).statistic)

def wilk(dane):
    # test Shapiro-Wilka 
    # nie jestem pewien czy 100 to maloliczny zbior danych wiec nie wiem czy smitnowa nie bylby lepszy ale go kompletnie nie rozumiem
    dane_s = sorted(dane)
    l = len(dane)
    w_g, w_d = 0, 0
    sre = srednia(dane)
    wilk_tablica = [0.3158, 0.2089, 0.1892, 0.1752, 0.164, 0.1547, 0.1466, 0.1394, 0.1329, 0.127, 0.1215, 0.1163, 0.1115, 0.1069, 0.1026, 0.0984, 0.0944, 0.0906, 0.0869, 0.0834, 0.0834, 0.0765, 0.0733, 0.0701, 0.067, 0.0639, 0.0609, 0.058, 0.0551, 0.0523, 0.0495, 0.0467, 0.044, 0.0413, 0.0387, 0.0361, 0.0335, 0.0309, 0.0284, 0.0258, 0.0233, 0.0208, 0.0183, 0.0159, 0.0134, 0.011, 0.0083, 0.0061, 0.0037, 0.0012]
    for i in range(l//2):
        w_g += wilk_tablica[i]*(dane_s[l-i-1]-dane_s[i])
    w_g = w_g ** 2
    for i in range(l):
        w_d += (dane[i] - sre)**2
    w = w_g/w_d
    if w > 0.963:
        # tutaj jest moment zwatpienia bo w tablicach W nie mamy wartosci 100 (konczy sie na 95), ale z drugiej strony nie ma też wartości 93 
        # jak to mozliwe ze jest tylko jedna tablica W w calym internecie?
        # czy to Pan stworzyl Shapiro-Wilka i wkrecil nas w robienie tego w ten sposob?
        print("Nie ma powodu by odrzucic hipoteze, ze dane sa rozkladem normalnym na poziomie istotnosci 0.05")
    else:
        print("Nie jest to rozklad plaski na poziomie istotnosci 0.05")
    print("Wartosc statystki testowej: ", w)
    print("Wartosc statystki testowej dla scipy: ", shapiro(dane).statistic)

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
    
# Pliki z rozkladami
plaski = zaladowanie_danych('r_plaski.json')
normalny = zaladowanie_danych('r_normalny.json')
lcg = zaladowanie_danych('r_lcg.json')
box = zaladowanie_danych('r_box.json')

# Tydzien 1
"""
print("Srednia:")
print(f"Rozklad plaski: {srednia(plaski)}")
print(f"Rozklad normlany: {srednia(normalny)}")
print("")
print("Mediana:")
print(f"Rozklad plaski: {mediana(plaski)}")
print(f"Rozklad normlany: {mediana(normalny)}")
print("")
print("Skosnosc:")
print(f"Rozklad plaski: {skosnosc(plaski)}")
print(f"Rozklad normlany: {skosnosc(normalny)}")
print("")
print("Kurtoza:")
print(f"Rozklad plaski: {kurtoza(plaski)}")
print(f"Rozklad normlany: {kurtoza(normalny)}")
"""

# Tydzien 2
"""
tworzenie_wykresu(plaski, 'plaski')
tworzenie_wykresu(normalny, 'normalny')
tworzenie_wykresu(box, 'normlany_box')
tworzenie_wykresu(lcg, 'plaski_lcg')
chi_kwadrat(plaski)
wilk(normalny)
"""

# Tydzien 3
"""
print("Testowanie rozkladu plaskiego:")
prawd_plaski = ks_2samp(plaski, lcg, alternative='two-sided')       # sprawdzamy czy sa z tego samego rozkladu metoda kolmogorova-smirnova
if prawd_plaski[0] < prawd_plaski[1]:
    print("Dane sa z tego samego rozkladu na poziomie istotnosci 0.05")
else:
    print("Dane nie sa z tego samego rozkladu na poziomie istotnosci 0.05")
print("")
print("Testowanie rozkladu normalnego:")
prawd_normalny = ks_2samp(normalny, box, alternative='two-sided')   # sprawdzamy czy sa z tego samego rozkladu metoda kolmogorova-smirnova
if prawd_normalny[0] < prawd_normalny[1]:
    print("Dane sa z tego samego rozkladu na poziomie istotnosci 0.05")
else:
    print("Dane nie sa z tego samego rozkladu na poziomie istotnosci 0.05")

"""
# Tydzien 4
mc = m_c(fx2, 0, 2, 100000)
ri = riemanns(fx2, 0, 2, 100000)
print("Monte Carlo: " +str(mc))
print("Riemanns: "+str(ri))
print("Roznica miedzy nimi: "+str(abs(mc-ri)))
punkciki = [[0,0],[1,2],[2,2],[1,-2]]
print(f"Pole figury okreslonej punktami {punkciki} wynosi: {dowolna_figura(punkciki, 10000)}")
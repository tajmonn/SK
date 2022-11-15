from os import system, name
from scipy.stats import kurtosis
import json

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

if __name__ == "__main__":
    # czyszczenie terminala 
    system('clear' if name=='posix' else 'cls')

    # Pliki z rozkladami
    plaski = zaladowanie_danych('r_plaski.json')
    normalny = zaladowanie_danych('r_normalny.json')

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
from scipy.stats import ks_2samp
from Tydzien1 import zaladowanie_danych
from os import system, name 

if __name__ == "__main__":
    # czyszczenie terminala 
    system('clear' if name=='posix' else 'cls')
    
    # Pliki z rozkladami
    plaski = zaladowanie_danych('r_plaski.json')
    normalny = zaladowanie_danych('r_normalny.json')
    lcg = zaladowanie_danych('r_lcg.json')
    box = zaladowanie_danych('r_box.json')

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
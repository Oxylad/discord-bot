def tri_selection(tab):
    N = len(tab)
    for k in range(N):
        imin = k
        for i in range(k+1 , N):
            if tab[i] < tab[imin] :
                imin = i
        tab[k], tab[imin] = tab[imin], tab[k]
    return tab

print("\U0001f5ff")        
        
print(tri_selection([41, 55, 21, 18, 12, 6, 6, 25]))
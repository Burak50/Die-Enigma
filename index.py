from collections import deque

def str2num(zeichenkette):
    return deque([ord(c)-65 for c in zeichenkette])


walzen_r = ['EKMFLGDQVZNTOWYHXUSPAIBRCJ', #Walze 1(Ⅰ)
            'AJDKSIRUXBLHWTMCQGZNPYFVOE', #Walze 2(Ⅱ)
            'BDFHJLCPRTXVZNYEIWGAKMUSQO', #Walze 3(Ⅲ)
            'ESOVPZJAYQUIRHXLNFTGKDCMWB', #Walze 4(Ⅳ)
            'VZBRGITYUPSDNHLXAWMJQOFECK', #Walze 5(Ⅴ)
            'JPGVOUMFYQBENHZRDKASXLICTW', #Walze 6(Ⅵ)
            'NZJHGRCXMYSWBOUFAIVLPEKQDT', #Walze 7(Ⅶ)
            'FKQHTLXOCBJSPDZRAMEWNIUYGV'] #Walze 8(Ⅷ)
walzen_r = [str2num(zeile) for zeile in walzen_r]
walzen_l = deque(range(26))

UKWs = ['EJMZALYXVBWFCRQUONTSPIKHGD', #Walze "UKW A"
        'YRUHQSLDPXNGOKMIEBFZCWVJAT', #Walze "UKW B"
        'FVPJIAOYEDRZXWGCTKUQSBNMHL'] #Walze "UKW C"
UKWs = [str2num(zeile) for zeile in UKWs]

kerbenKat = "Q E V J Z ZM ZM ZM"
kerbenKat = [str2num(zeile) for zeile in kerbenKat.split()]

# print(KerbenKat)

class Walze():
    def __init__(self, nr, w_pos, r_pos):
        self.w_pos = w_pos
        self.r_pos = r_pos
        self.verdr_r = walzen_r[nr].copy()
        self.verdr_l = walzen_l.copy()
        self.kerben = kerbenKat[nr]
        self.setup()

    def setup(self):
        offset = self.r_pos-self.w_pos
        self.verdr_l.rotate(offset)
        self.verdr_r.rotate(offset)
        self.kerben = [(k-self.r_pos) % 26 for k in self.kerben]
    
    def show(self):
        for nr in self.verdr_l:
            print(chr(nr+65),end='')
        print()
        for nr in self.verdr_r:
            print(chr(nr+65),end='')
        print()
        for nr in self.kerben:
            print(chr(nr+65),end='')
        print()

    def click(self):
        self.verdr_l.rotate(-1)
        self.verdr_r.rotate(-1)
        
    def schaltung(self):
        return self.verdr_l[0] in self.kerben


# w = Walze(3, ord("T")-65, 4)
# w.show()

class Enigma():
    def __init__(self):
        self.walzen = []
        self.ukw = []
        self.steckerbr = {}

    def setup(self, nr_ukw, nr_walzen, w_pos, r_pos, paare_steckerbr):
        for i,nr in enumerate(nr_walzen):
            wpos = ord(w_pos[i])-65
            rpos = r_pos[i]-1
            self.walzen.append(Walze(nr-1, wpos, rpos))
        self.ukw = UKWs[nr_ukw-1]
        for a,b in paare_steckerbr.split():
            self.steckerbr[ord(a)-65] = ord(b)-65
            self.steckerbr[ord(b)-65] = ord(a)-65


    def rotiere(self):
        links, mitte, rechts = self.walzen
        if mitte.schaltung():
            mitte.click()
            links.click()
        elif rechts.schaltung():
            mitte.click()
        rechts.click()

def umwandeln(e, text):
    u_text = ""
    text = text.upper()
    for c in text:
        c = ord(c)-65
        if c < 0 or c> 26: continue
        e.rotiere()
        c = e.steckerbr.get(c,c)
        for w in reversed(e.walzen):
            c = w.verdr_r[c]
            c = w.verdr_l.index(c)
        c = e.ukw[c]
        for w in e.walzen:
            c = w.verdr_l[c]
            c = w.verdr_r.index(c)
        c = e.steckerbr.get(c,c)
        u_text += chr(c+65)
    return u_text

enigma = Enigma()
#Ring einstellungen#
enigma.setup(1, #Umkehr walze(A)
[2,1,3], #Walzen
"ABL", #Tages schlüssel
[24,13,22], #Ringpositionen
"AM FI NV PS TU WZ") #Steckerbrett

print('Die Enigma')
text = input('Texteingabe: ')
u_text = umwandeln(enigma, text)
u_text = u_text.replace('X', ' ')
u_text = u_text.replace('Q', 'CH')
print(u_text)


#http://wiki.franklinheath.co.uk/index.php/Enigma/Sample_Messages
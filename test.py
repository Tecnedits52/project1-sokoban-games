def faktorial(n):
    if n == 0:
        return 1
    
    return n*faktorial(n-1)

print(faktorial(2))     # 2
print(faktorial(3))     # 6
print(faktorial(4))     # 24
print(faktorial(5))     # 120
print(faktorial(0))     # 1

# 4! = 4 * 3!
# faktorial(4) = 4 * faktorial(3)




def cetak_menurun(n):
    print(n)
    if n == 1:
        return    
    else:
        cetak_menurun(n-1)
    


cetak_menurun(10)   # 10 9 8 7 ... 1
cetak_menurun(1)   # 10 9 8 7 ... 1



def hitung_vokal(s, index=0):
    if index == len(s):
        return 0
    else:
        if s[index] in ["a","o","u","i","e"]:
            return (hitung_vokal(s,index+1)) + 1
        else:
            return (hitung_vokal(s,index+1))
    
print(f"vocal {hitung_vokal("andro")}")        

def hitung_vokal2(s):
    if len(s) == 0:
        return 0
    else:
        if s[0] in ["a","o","u","i","e"]:
            return (hitung_vokal(s[1:])) + 1
        else:
            return (hitung_vokal(s[1:]))
print(f"vocal {hitung_vokal2("andro")}")     

def jumlah_digit(n):
    if n < 10:
        return 1
    return 1+jumlah_digit(n//10)



print(jumlah_digit(198))                # 3
print(jumlah_digit(12298))            # 5

def count_digit(n):
    if n<10:
        return n
    return n%10+count_digit(n//10) 



def palindrom(s):
    if len(s) <= 1:
        return True
    else:
        if s[0] == s[len(s)-1]:
            return palindrom(s[1:len(s)-1])

        else:
            return False
    
        


    # for i in range(len(s)//2):
    #     if s[i] != s[(len(s)-i)-1]:
    #         return False
    
    # return True

print(palindrom(""))
print(palindrom("x"))
print(palindrom("aa"))
print(palindrom("ab"))
print(palindrom("ini"))
print(palindrom("itu"))
print(palindrom("anna"))
print(palindrom("iburatnaantarubi"))
print(palindrom("rumahmurah"))
print(palindrom("akusukarajawalibapakapabilawajarakusuka"))



def biner(n):
    if n == 0:
        return "0"
    elif n==1:
        return "1"
    else:
        return biner(n//2) + str(n%2)

print(biner(0))
print(biner(1))
print(biner(512))
print(biner(1697))
print(biner(1048575))
print(biner(13))


def ispowerof2(n):
    if n == 1:
        return True
    return (n%2 == 0) and ispowerof2(n//2)  



    # for i in range(n):
    #     if 2 ** i == n:
    #         return True
    # return False
print(ispowerof2(64))

def max_value(lst):
    if len(lst) == 1:
        return lst[0]
    else:
        max = max_value(lst[1:])
        if (lst[0]) > max:
            return lst[0]
        else:
            return max
print(max_value([3, 1, 9, 2, 7]))
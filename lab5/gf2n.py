# 50.042 FCS Lab 5 Modular Arithmetics
# Year 2021

import copy
class Polynomial2:
    def __init__(self,coeffs):
        self.coeffs = coeffs
        self.length = len(coeffs)

    def add(self, p2):
        a = copy.copy(self.coeffs)
        b = copy.copy(p2.coeffs)

        for i in range(p2.length - self.length): 
            a.append(0)
        for i in range(self.length - p2.length):
            b.append(0)
        
        # Bitwise XOR
        result = [a[i] ^ b[i] for i in range(len(a))]
        return Polynomial2(result)

    def sub(self,p2):
        return self.add(p2)

    def mul(self,p2,modp=None):
        result = Polynomial2([0])

        # Iterate through p2 and find the 1s
        for i in range(p2.length):
            if p2.coeffs[i] == 1:

                # If no modp, just left shift
                if modp == None:
                    ref = [0 for j in range(i)]
                    ref.extend(self.coeffs)

                # If there is modp, left shift and modulo i times
                else:
                    ref = self.coeffs
                    for j in range(i):
                        partial = [0]
                        partial.extend(ref)

                        if len(partial) == modp.length:
                            # Reduce if MSB = 1
                            if partial[-1] == 1:
                                partial = Polynomial2(partial).sub(modp).coeffs
                                
                            # Remove MSB if partial result has too many bits
                            partial.pop()
                        ref = partial
                
                # Add partial result
                result = result.add(Polynomial2(ref))
                
        return result

    def div(self,p2):
        q = Polynomial2([0 for i in range(self.length)])
        r = Polynomial2(self.coeffs)
        d = p2.deg()
        # c = 1 since this is GF2, so 1 is the only possible lc
        
        rd = r.deg()
        while rd >= d:
            # Coeff of s = 1, same explanation as above
            # Construct polynomial s
            temp = [0 for i in range(rd - d)]
            temp.append(1)
            s = Polynomial2(temp)

            q = q.add(s)
            r = r.sub(s.mul(p2))
            rd = r.deg()
        return q, r

    def __str__(self):
        first = True
        for i in range(self.length-1, -1, -1):
            if self.coeffs[i] == 1:
                if first:
                    result = f"x^{i}"
                    first = False
                else:
                    result += f"+x^{i}"
        return result

    def getInt(p):
        result = 0b0
        for i in range(p.length):
            result += p.coeffs[i] << i
        return result

    # div helper functions
    def deg(self):
        for i in range(self.length-1, -1, -1):
            if self.coeffs[i] == 1:
                return i
    
    def lc(self, d):
        return self.coeffs[d]


class GF2N:
    affinemat=[[1,0,0,0,1,1,1,1],
               [1,1,0,0,0,1,1,1],
               [1,1,1,0,0,0,1,1],
               [1,1,1,1,0,0,0,1],
               [1,1,1,1,1,0,0,0],
               [0,1,1,1,1,1,0,0],
               [0,0,1,1,1,1,1,0],
               [0,0,0,1,1,1,1,1]]

    def __init__(self,x,n=8,ip=Polynomial2([1,1,0,1,1,0,0,0,1])):
        poly = [0 for i in range(n)]
        for i in range(n-1, -1, -1):
            if x >= 2**i:
                poly[i] = 1
                x -= 2**i
        self.poly = Polynomial2(poly)
        self.ip = ip

    def add(self,g2):
        result = self.poly.add(g2.poly)
        return GF2N(Polynomial2.getInt(result))

    def sub(self,g2):
        result = self.poly.sub(g2.poly)
        return GF2N(Polynomial2.getInt(result))
    
    def mul(self,g2):
        result = self.poly.mul(g2.poly, self.ip)
        return GF2N(Polynomial2.getInt(result))

    def div(self,g2):
        q, r = self.poly.div(g2.poly)
        return GF2N(Polynomial2.getInt(q)), GF2N(Polynomial2.getInt(r))

    def getPolynomial2(self):
        return self.poly

    def __str__(self):
        return f"{self.getInt()}"

    def getInt(self):
        return Polynomial2.getInt(self.poly)

    def mulInv(self):
        pass

    def affineMap(self):
        pass

def genTable1():
    print("ADDITION\n")
    print("   | 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15")
    print("---|-----------------------------------------------")
    for i in range(16):
        line = ""
        if i < 10:
            line += "0"
        line += f"{i} |"

        for j in range(16):
            a = GF2N(i, 4, Polynomial2([1,0,0,1,1]))
            b = GF2N(j, 4, Polynomial2([1,0,0,1,1]))
            result = a.add(b).getInt()
            if result < 10:
                line += " 0"
            else:
                line += " "
            line += f"{result}"

        print(line)
    
    print("\n\n\nMULTIPLICATION\n")
    print("   | 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15")
    print("---|-----------------------------------------------")
    for i in range(16):
        line = ""
        if i < 10:
            line += "0"
        line += f"{i} |"

        for j in range(16):
            a = GF2N(i, 4, Polynomial2([1,0,0,1,1]))
            b = GF2N(j, 4, Polynomial2([1,0,0,1,1]))
            result = a.mul(b).getInt()
            if result < 10:
                line += " 0"
            else:
                line += " "
            line += f"{result}"

        print(line)

# To quickly produce the result for table1.txt
#genTable1()

print('\nTest 1')
print('======')
print('p1=x^5+x^2+x')
print('p2=x^3+x^2+1')
p1=Polynomial2([0,1,1,0,0,1])
p2=Polynomial2([1,0,1,1])
p3=p1.add(p2)
print('p3= p1+p2 = ',p3)

print('\nTest 2')
print('======')
print('p4=x^7+x^4+x^3+x^2+x')
print('modp=x^8+x^7+x^5+x^4+1')
p4=Polynomial2([0,1,1,1,1,0,0,1])
# modp=Polynomial2([1,1,0,1,1,0,0,0,1])
modp=Polynomial2([1,0,0,0,1,1,0,1,1])
p5=p1.mul(p4,modp)
print('p5=p1*p4 mod (modp)=',p5)

print('\nTest 3')
print('======')
print('p6=x^12+x^7+x^2')
print('p7=x^8+x^4+x^3+x+1')
p6=Polynomial2([0,0,1,0,0,0,0,1,0,0,0,0,1])    
p7=Polynomial2([1,1,0,1,1,0,0,0,1])
p8q,p8r=p6.div(p7)
print('q for p6/p7=',p8q)
print('r for p6/p7=',p8r)

####
print('\nTest 4')
print('======')
g1=GF2N(100)
g2=GF2N(5)
print('g1 = ',g1.getPolynomial2())
print('g2 = ',g2.getPolynomial2())
g3=g1.add(g2)
print('g1+g2 = ',g3)

print('\nTest 5')
print('======')
ip=Polynomial2([1,1,0,0,1])
print('irreducible polynomial',ip)
g4=GF2N(0b1101,4,ip)
g5=GF2N(0b110,4,ip)
print('g4 = ',g4.getPolynomial2())
print('g5 = ',g5.getPolynomial2())
g6=g4.mul(g5)
print('g4 x g5 = ',g6.getPolynomial2()) # I assume this was what g6.p meant

print('\nTest 6')
print('======')
g7=GF2N(0b1000010000100,13,None)
g8=GF2N(0b100011011,13,None)
print('g7 = ',g7.getPolynomial2())
print('g8 = ',g8.getPolynomial2())
q,r=g7.div(g8)
print('g7/g8 =')
print('q = ',q.getPolynomial2())
print('r = ',r.getPolynomial2())

#print('\nTest 7')
#print('======')
#ip=Polynomial2([1,1,0,0,1])
#print('irreducible polynomial',ip)
#g9=GF2N(0b101,4,ip)
#print('g9 = ',g9.getPolynomial2())
#print('inverse of g9 =',g9.mulInv().getPolynomial2())

#print('\nTest 8')
#print('======')
#ip=Polynomial2([1,1,0,1,1,0,0,0,1])
#print('irreducible polynomial',ip)
#g10=GF2N(0xc2,8,ip)
#print('g10 = 0xc2')
#g11=g10.mulInv()
#print('inverse of g10 = g11 =', hex(g11.getInt()))
#g12=g11.affineMap()
#print('affine map of g11 =',hex(g12.getInt()))

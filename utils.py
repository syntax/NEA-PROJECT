from api import Database
import random
import hashlib
import math


def generatekey(random_chars, alphabet="0123456789abcdefghijklmnopqrstuvwxyz"):
    r = random.SystemRandom()
    return ''.join([r.choice(alphabet) for i in range(random_chars)])

def createLicense():
    while True:
        license = generatekey(random_chars=16)
        conn = Database()
        if conn.checkIfLicenseExists(license):
            continue
        else:
            print(f'created license {license}')
            conn.commitLicense(license)
            conn.closeConnection()
            return license

def gensalt(username):

    # a strange algorithm to create larger salts, as well as remove the predictability vulnerability for as long as this algorithm is kept secret
    def ceaser(shift,string):
        alphabet = '0abcdefghijkl1234mnopqrst567uvwx89yz'
        output = []

        for letter in string:
            if letter.strip() and letter in alphabet:
                output.append(alphabet[(alphabet.index(letter) + shift) % 36])

        return ''.join(output)

    def manipulationalgo(inputstr):
        doubled = ''.join([element*2 for element in inputstr])
        output = []
        count = 1
        for letter in doubled:
            #cant use .index() as letter appears multiple times!
            if count % 2 == 0:
                output.append(ceaser(count,letter))
            else:
                output.append(ceaser(-1,letter))
            count += 1
            
        return ''.join(output)
    
    salt = manipulationalgo(username)
    pepper = '3UwF4zVIB2CkF3uOMkmAifCMjO+88RKNfL4u6EXifPQ='

    return salt+pepper

def hash(username,password):
    hashdpw = hashlib.pbkdf2_hmac(
        hash_name='sha256',  # The hash digest algorithm for HMAC
        password=password.encode('utf-8'),
        salt=gensalt(username).encode('utf-8'),
        iterations=100000  # 100,000 iterations of SHA-256
    )

    return hashdpw
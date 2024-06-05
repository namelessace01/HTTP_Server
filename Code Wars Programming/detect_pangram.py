# Complete the solution so that it splits the string into pairs of two characters.
# If the string contains an odd number of characters then it should replace the 
# missing second character of the final pair with an underscore ('_').

def pangram(p):
    if len(p) == 0:
        return []
    elif (len(p) % 2) != (2 % 2):
        return p
    else:
        return [p[i:i+2] for i in range(0, len(p), 2)]
    

print(pangram("abcdefg"))



def solution(A):
    # write your code in Python 3.6
    if max(A) <= 0:
        return 1
    if A == [1]:
        return 2
    if len(A) == 1 and max(A) > 0:
        return A[0] - 1 
    # if max(A) == min(A):
    #     return max(A) + 1
    for x in sorted(A):
        if x + 1 in A:
            pass
        else:
            return (x+1)
    
import re
x = "We test coders. Give us a try?"
y = "Forget  CVs..Save time . x x"
# print(re.split('[.?!]',x))
# def word_count(text):
#     return(len(text.split()))

def answer(S):
    S_list = re.split('[.?!]',S)
    print(S_list)
    word_count = [len(x.split()) for x in S_list]
    print(word_count)
# answer(x)
# answer(y)

def sol(S,T):
    if S == T[1:]:
        return f"INSERT {T[0]}"
print(sol('test','btest'))

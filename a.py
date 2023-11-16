import itertools

def is_flowing(my_string):
    my_string = list(my_string)
    sorted_string = sorted(my_string)
    return my_string == sorted_string

def is_receiding(my_string):
    my_string = list(my_string)
    sorted_string = sorted(my_string, reverse=True)
    return my_string == sorted_string

def is_turbulent(my_string):
    return not(is_flowing(word)) and not(is_receiding(word))

alphabet = [chr(ord("a") + i) for i in range(26)]


for i in range(1, 5+1):
    words = [p for p in itertools.product(alphabet, repeat=i)]
    sf = 0
    sr = 0
    st = 0
    for word in words:
        if is_receiding(word):
            sr += 1
        if is_flowing(word):
            sf += 1
        if is_turbulent(word):
            st += 1

    print(f"For i={i} is", st)

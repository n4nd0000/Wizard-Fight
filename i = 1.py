import time

i = 1
while i != 10:
    print(i)
    i += 2
    time.sleep(1)
    if i ==9 or i == 11:
        print(i, "é o mais perto que vai chegar de 10") 
    if i > 15:
        print("chegamos no limite, pararemos aqui.")
        break
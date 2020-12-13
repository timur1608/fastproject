list_of_numbers = list()
for i in range(2 * (10 ** 10), 4 * (10 ** 10) + 1):
    if i % 7 == 0 and i % 100000 == 0 and i % 13 != 0 and i % 29 != 0 and i % 43 != 0 and i % 101 != 0:
        list_of_numbers.append(i)
    print(i)
print(len(list_of_numbers))
print(min(list_of_numbers))

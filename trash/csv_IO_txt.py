import csv

with open('bitkoin_quotes.csv', 'r') as f:
    csv_file = csv.reader(f)
    array = []
    for line in csv_file:
        array.append(line)
    print(len(array))

    with open('new_btc_cource.txt', 'a', encoding='utf-8') as file:
        for i in range(4958, 0, -1):
            file.write(f'{array[i][3]}\n{array[i][4]}\n')
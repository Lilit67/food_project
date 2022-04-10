import csv
import argparse


def parse_args():
    return opts

def main():
    data = []
    with open('./test.csv', 'r') as f:
        print(f)
        reader = csv.reader(f)
        for row in reader:
            print(', '.join(row))
            data.append(row)

    for row in data[1:]:
        #print(type(row))
        row[0] = int(row[0]) + 86400000 * tms
        #row = ','.join(row1)


    with open('output.csv', 'w') as f1:
        writer = csv.writer(f1, delimiter=',')
        for row in data:
            writer.writerow(row)




if __name__ == '__main__':
    main()
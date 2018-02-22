import os


def compute_changes(in_dir, out_file_path):
    buckets = {}

    with open(out_file_path, 'w') as out_file:
        out_file.writelines('month,count,group\n')
        for year in [2013, 2014, 2015, 2016, 2017]:
            for month in range(1, 13):
                filename = os.path.join(in_dir, '%d-%02d.csv' % (year, month))
                if os.path.exists(filename):
                    with open(filename, 'r') as in_file:
                        in_file.readline()
                        for line in in_file:
                            data = list(map(lambda x: int(x), line.split(',')))
                            out_file.writelines('%d/%02d,%d,%s\n' % (year, month, data[1], data[0]))


def main():
    distribution_dir = 'gender_distributions'
    results_file = 'gender_distribution_changes.csv'

    compute_changes(distribution_dir, results_file)


if __name__ == '__main__':
    main()
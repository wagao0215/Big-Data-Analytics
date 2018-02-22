import os
import math


def compute_changes(in_dir, out_file_path):
    bucket_labels = []
    buckets = {}
    for i in range(15, 90, 5):
        label = '%d-%d' % (i, i+5)
        bucket_labels.append(label)
        buckets[label] = 0

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
                            if data[0] > 85:
                                continue
                            bucket = bucket_labels[int((math.floor(data[0] - 15) / 5))]
                            buckets[bucket] += data[1]
                    for bucket in buckets:
                        out_file.writelines('%d/%02d,%d,%s\n' % (year, month, buckets[bucket], bucket))
                        buckets[bucket] = 0


def main():
    distribution_dir = 'age_distributions'
    results_file = 'age_distribution_changes.csv'

    compute_changes(distribution_dir, results_file)


if __name__ == '__main__':
    main()
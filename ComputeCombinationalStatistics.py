import os
import math
from collections import OrderedDict


def compute_changes(total_file_path, out_file_path):
    bucket_labels = []
    buckets = {}
    for i in range(15, 90, 5):
        label = '%d-%d' % (i, i + 5)
        bucket_labels.append(label)
        buckets[label] = 0

    cumulative_results = OrderedDict()
    for year in range(2013, 2018):
        temp_month = {}
        for month in range(1, 13):
            temp_age_groups = {}
            for bucket in range(15, 90, 5):
                temp_age_groups['%d-%d' % (bucket, bucket + 5)] = {}
            temp_month[month] = temp_age_groups
        cumulative_results[year] = temp_month

    with open(total_file_path, 'r') as total_file:
        total_file.readline()
        for line in total_file:
            data = line.strip().split(',')
            month = int(data[-1].replace('"', ''), 10)
            year = int(data[-2].replace('"', ''), 10)
            gender = int(data[-3].replace('"', ''), 10)

            try:
                age = 2017 - int(data[-4].replace('"', ''), 10)
                age_group = bucket_labels[int((math.floor(age - 15) / 5))]
            except Exception as _:
                continue

            if gender in cumulative_results[year][month][age_group]:
                cumulative_results[year][month][age_group][gender] += 1
            else:
                cumulative_results[year][month][age_group][gender] = 1

    with open(out_file_path, 'w') as out_file:
        out_file.writelines('month,year,group,gender,count\n')
        for year in cumulative_results:
            for month in cumulative_results[year]:
                for age_group in cumulative_results[year][month]:
                    for gender in cumulative_results[year][month][age_group]:
                        out_file.writelines('%d,%d,%s,%d,%d\n' % (month, year, age_group, gender, cumulative_results[year][month][age_group][gender]))

def main():
    total_file_path = 'total.csv'
    results_file = 'combinational_statistics.csv'

    compute_changes(total_file_path, results_file)


if __name__ == '__main__':
    main()
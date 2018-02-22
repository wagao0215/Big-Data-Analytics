import os
import urllib.error
import urllib.request
import zipfile
import time


def get_trip_url_name(year, month):
    if year < 2017:
        file_name = '%d%02d-citibike-tripdata.zip' % (year, month)
    else:
        file_name = '%d%02d-citibike-tripdata.csv.zip' % (year, month)

    return file_name


def get_trip_data_file(year, month, save_dir):
    file_name = get_trip_url_name(year, month)
    save_path = None

    try:
        file_url = 'https://s3.amazonaws.com/tripdata/' + file_name
        save_url = save_dir + '/' + file_name

        urllib.request.urlretrieve(file_url, save_url)

        zip_ref = zipfile.ZipFile(save_url, 'r')
        save_path = save_dir + '/%d-%02d.csv' % (year, month)
        for f in zip_ref.filelist:
            f.filename = save_path
            zip_ref.extract(f)
        zip_ref.close()

        os.remove(save_url)

    except urllib.error.HTTPError as e:
        print('\t\t\t' + file_name + ' - ' + e.reason)

    return save_path


def add_data_to_file(in_file_path, out_file_path, year, month):
    in_file = open(in_file_path, 'r')
    out_file = open(out_file_path, 'a')

    header_line = in_file.readline()
    if os.stat(out_file_path).st_size == 0:
        # Writing header
        out_file.writelines(header_line[:-1] + ',"data year","data month"\n')

    additional_info = ',"%d","%02d"\n' % (year, month)
    for line in in_file:
        out_file.writelines([line[:-1], additional_info])

    in_file.close()
    out_file.close()


def download_data(download_dir, cumulative_file):
    # Create directories if they do not exist
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Create empty cumulative file
    open(cumulative_file, 'a').close()

    # Download all data files
    for year in range(2013, 2018):
        print('\t\tGetting data of Year %d' % (year))
        for month in range(1, 13):
            data_file = get_trip_data_file(year, month, download_dir)
            if data_file is not None:
                add_data_to_file(data_file, cumulative_file, year, month)
            print('\t\t\tFinished month: %d' % (month))


def increment_count(age, age_counts):
    if age in age_counts:
        age_counts[age] += 1
    else:
        age_counts[age] = 1


def write_dict_to_csv(out_file_path, buckets):
    with open(out_file_path, 'w') as out_file:
        out_file.writelines('age,count\n')
        for bucket in buckets:
            out_file.writelines('{},{}\n'.format(bucket, buckets[bucket]))


def compute_age_distributions(in_dir, out_dir, cumulative_file):
    # Create directories if they do not exist
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    years = range(2013, 2018)
    total_distribution = {}
    year_age_distributions = {}
    for year in years:
        year_age_distributions[year] = {}

    for filename in os.listdir(in_dir):
        age_distribution = {}
        current_year = 2013
        if filename.endswith('.csv'):
            for year in years:
                if str(year) in filename:
                    current_year = year

            with open(os.path.join(in_dir, filename)) as file:
                file.readline()
                for line in file:
                    data_point = line.split(',')

                    try:
                        age = 2017 - int(data_point[-2].replace('"', ''), 10)
                        increment_count(age, age_distribution)
                        increment_count(age, total_distribution)
                        increment_count(age, year_age_distributions[current_year])
                    except ValueError as _:
                        continue

            write_dict_to_csv(os.path.join(out_dir, filename), age_distribution)
        print('\t\tFinished file: %s' % filename)

    for year in year_age_distributions:
        write_dict_to_csv(os.path.join(out_dir, '{}.csv'.format(year)), year_age_distributions[year])

    write_dict_to_csv(cumulative_file, total_distribution)


def compute_gender_distributions(in_dir, out_dir, cumulative_file):
    # Create directories if they do not exist
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    years = range(2013, 2018)
    total_distribution = {}
    year_gender_distributions = {}
    for year in years:
        year_gender_distributions[year] = {}

    for filename in os.listdir(in_dir):
        gender_distribution = {}
        current_year = 2013
        if filename.endswith('.csv'):
            for year in years:
                if str(year) in filename:
                    current_year = year

            with open(os.path.join(in_dir, filename)) as file:
                file.readline()
                for line in file:
                    data_point = line.split(',')

                    try:
                        gender = data_point[-1].strip().replace('"', '')
                        increment_count(gender, gender_distribution)
                        increment_count(gender, total_distribution)
                        increment_count(gender, year_gender_distributions[current_year])
                    except ValueError as _:
                        continue

            write_dict_to_csv(os.path.join(out_dir, filename), gender_distribution)
        print('\t\tFinished file: %s' % filename)

    for year in year_gender_distributions:
        write_dict_to_csv(os.path.join(out_dir, '{}.csv'.format(year)), year_gender_distributions[year])

    write_dict_to_csv(cumulative_file, total_distribution)


def main():
    start = time.clock()

    download_dir = 'data'
    cumulative_file = 'total.csv'
    age_distribution_dir = 'age_distributions'
    age_distribution_file = 'total_age_distributions.csv'
    gender_distribution_dir = 'gender_distributions'
    gender_distribution_file = 'total_gender_distributions.csv'

    if not os.path.exists(download_dir) or not os.path.exists(cumulative_file):
        print('\tDownloading data files')
        download_data(download_dir, cumulative_file)

    if not os.path.exists(age_distribution_dir) or not os.path.exists(age_distribution_file):
        print('\tProcessing age distributions')
        compute_age_distributions(download_dir, age_distribution_dir, age_distribution_file)

    if not os.path.exists(gender_distribution_dir) or not os.path.exists(gender_distribution_file):
        print('\tProcessing gender distributions')
        compute_gender_distributions(download_dir, gender_distribution_dir, gender_distribution_file)

    end = time.clock()
    print('Total elapsed time: %.2f m' % ((end - start) / 60.0))

if __name__ == '__main__':
    main()

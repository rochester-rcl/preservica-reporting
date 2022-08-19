from pyPreservica import *
from datetime import datetime
import csv

client = EntityAPI()

folder_dict = {
    'RBSCP Root Folder': 'be83e38b-776c-4369-aa32-4a444f721004',
    'Charlotte Perkins Gilman papers': '95ad8d5a-639b-4a18-a09b-b9a5da4453ab',
    'John McGraw Civil War letters': '423b8c89-af0b-45f3-9bbf-fdb651a34fe9'
}

now = datetime.now()
date_time = now.strftime('%Y-%m-%d_%H-%M-%S')

with open('preservica_storage_report_' + date_time + '.csv', 'w', newline='') as report:
    csv_writer = csv.writer(report)
    csv_writer.writerow(['Folder Name', 'Folder Ref', 'Bytes', 'MB', 'GB', 'TB', 'Assets', 'Files Uploaded', 'Total Files'])
    for key, value in folder_dict.items():
        csv_row = [key, value]
        folder_target = client.folder(value)
        folder_size = 0
        total_assets = 0
        files_uploaded = 0
        total_files = 0
        for asset in filter(only_assets, client.all_descendants(folder_target.reference)):
            total_assets += 1
            for representation in client.representations(asset):
                for content_object in client.content_objects(representation):
                    files_uploaded += 1
                    for generation in client.generations(content_object):
                        for bitstream in generation.bitstreams:
                            total_files += 1
                            folder_size += bitstream.length
                            print(bitstream.length)
        csv_row.append(folder_size)
        csv_row.append(round(folder_size / 1000000, 2))
        csv_row.append(round(folder_size / 1000000000, 2))
        csv_row.append(round(folder_size / 1000000000000, 2))
        csv_row.append(total_assets)
        csv_row.append(files_uploaded)
        csv_row.append(total_files)
        print(csv_row)
        csv_writer.writerow(csv_row)

import fileinput
import csv
import sys

from volume_details import get_volume_details

if __name__ == "__main__":
    fieldnames = [
        "volume_id",
        "volume_host",
        "volume_name",
        "user_name",
        "user_email",
        "project_name",
        "attachment_server_id",
        "attachment_server_name",
        "attachment_host_name",
        "attachment_device"
    ]
    csv_writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    csv_writer.writeheader()

    for line in fileinput.input():
        volume_id = line.strip()
        volume_details = get_volume_details(volume_id=volume_id)
        csv_writer.writerow(volume_details)

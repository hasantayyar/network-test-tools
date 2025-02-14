import datetime
import os
import requests
import sys
import time

url = "...."
download_count = 10
file_name = "downloaded_file.zip"
report_file = "download_speed_report.csv"
report_header = "Time,Download Speed,Download Size,Download Time"
report_data = []
report_file_path = os.path.join(os.path.dirname(__file__), report_file)

def download_speed(url, file_name):
    start_time = time.time()
    print("Start Time: {}".format(datetime.datetime.now()))
    print("Downloading file...")
    r = requests.get(url, stream=True)
    end_time = time.time()
    download_time = end_time - start_time

    download_size = 0
    chunk_size = 1024  # 1 KB
    with open(file_name, "wb") as f:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                download_size += len(chunk)
                current_time = time.time()
                elapsed_time = current_time - start_time
                if elapsed_time > 0:
                    current_speed = download_size / elapsed_time
                    sys.stdout.write("\rCurrent Download Speed: {:.2f} MB/sec".format(current_speed/1024/1024))
                    sys.stdout.flush()
    end_time = time.time()
    download_time = end_time - start_time
    download_speed = download_size / download_time
    print("End Time: {}".format(datetime.datetime.now()))
    print("Download Time: {} seconds".format(download_time))
    print("Download Size: {} bytes".format(download_size))
    # Return the download speed
    return download_speed, download_size, download_time

# Create the report file
with open(report_file_path, "w") as f:
    f.write(report_header + "\n")

# Download the file multiple times
for i in range(download_count):
    download_speed_result = download_speed(url, file_name)
    report_data.append("{},{},{},{}".format(datetime.datetime.now(), download_speed_result[0], download_speed_result[1], download_speed_result[2]))
    print("Download Speed: {} bytes/sec".format(download_speed_result[0]))
    time.sleep(1) # Wait for 1 second

# Append the report data
with open(report_file_path, "a") as f:
    for report_line in report_data:
        f.write(report_line + "\n")

print("Report File: {}".format(report_file_path))

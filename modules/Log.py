from datetime import datetime

def log (msg):
    data_moment = datetime.now()
    log_file_name = f"log_{datetime.strftime(data_moment, '%d-%m-%Y')}"

    with open(f"./logs/{log_file_name}.txt", "a") as log_file:
                log_file.writelines(f"{datetime.strftime(data_moment, '%d-%m-%Y %H:%M:%S - ')}{msg}\n")
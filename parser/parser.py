import re
from datetime import datetime
from .cronJob import CronJob


def detect_log_format(line: str) -> str:
    iso8601_start = re.match(r'^\d{4}-\d{2}-\d{2}T', line)
    bsd_start = re.match(r'^[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}', line)

    if iso8601_start:
        return "iso"
    elif bsd_start:
        return "bsd"
    else:
        return "unknown"


def extract_cron_iso (log_splitted: list[str]) -> CronJob:
	
	date_string = log_splitted[0][0:log_splitted[0].find("T")]
	time_string = log_splitted[0][log_splitted[0].find("T")+1:log_splitted[0].find("+")]

	return CronJob (
		date = datetime.strptime(date_string,"%Y-%m-%d").date(),
		timestamp = datetime.strptime(time_string, "%H:%M:%S.%f").time(),
    	user = log_splitted[3][log_splitted[3].find("(")+1:log_splitted[3].find(")")],
    	command = ' '.join(log_splitted[5:]),
    	hostname =	log_splitted[1],
    	pid = log_splitted[2][log_splitted[2].find("[")+1:log_splitted[2].find("]")]
	)

def extract_cron_bsd (log_splitted: list[str]) -> CronJob:
	date_string = ' '.join(log_splitted[0:2])
	date_string = str(datetime.now().year)+' '+date_string
	time_string = log_splitted[2]

	return CronJob (
		date = datetime.strptime(date_string, "%Y %b %d").date(),
		timestamp = datetime.strptime(time_string, "%H:%M:%S").time(),
		user = log_splitted[5][log_splitted[5].find("(")+1:log_splitted[5].find(")")],
		command = ' '.join(log_splitted[7:]),
		hostname = log_splitted[3],
		pid = log_splitted[4][log_splitted[4].find("[")+1:log_splitted[4].find("]")]
	) 


def extract_cron_entries (file_path: str="/var/log/syslog") -> list[CronJob]:

	log_format = ""
	cron_entries = list()

	with open(file_path, "rt") as logs:
		for log in logs:

			log_splitted = log.strip().split(" ")

			if log_format == "":

				log_format = detect_log_format(log.strip())




			if log_format == "iso" :
				
				if "CRON" in log_splitted[2].upper():	
					job = extract_cron_iso(log_splitted)
					print(job)
					cron_entries.append(job)
					

			elif log_format == "bsd":
				try:
					if "CRON" in log_splitted[4].upper():
						job = extract_cron_bsd(log_splitted)
						print(job)
						cron_entries.append(job)
				except Exception:
					continue

			else:
				raise Exception("The syslog file has an undefined structure")

			

	return cron_entries

extract_cron_entries("/home/mohsen2/Documents/cr0nd4mp/test.txt")

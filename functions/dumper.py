from cronJob import CronJob
from Job import Job
from parser import extract_cron_entries
from datetime import datetime


def extract_cron_jobs (entries: list[CronJob]) -> list[Job]:

	jobs = dict()

	for entry in entries:

		aux = (entry.user, entry.command)

		if aux in jobs:

			if len(jobs[aux]) < 2:
				
				jobs[aux].append(entry.timestamp)

		else:

			jobs[aux] = list()



	Jobs = []
	print(jobs)

	for job in jobs:

		if len(jobs[job]) >= 2:

			

			today = datetime.today().date()
			start_dt = datetime.combine(today, jobs[job][0])
			end_dt = datetime.combine(today, jobs[job][1])

			schedule = end_dt - start_dt

			newJob = Job(
					user = job[0],
					command = job[1],
					schedule = schedule
				)
			
			Jobs.append(newJob)



	return Jobs

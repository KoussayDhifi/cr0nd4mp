from datetime import date, time

class CronJob:

    def __init__(self, date: date, timestamp: time, user: str, command: str, hostname: str = "", pid: int = -1, log_type: str = "CMD"):
        self.date = date
        self.timestamp = timestamp      
        self.user = user                
        self.command = command          
        self.hostname = hostname        
        self.pid = pid
        self.log_type = log_type                  

    def __repr__(self):
        return f"< CronJob {self.timestamp} | {self.user} | {self.command} | {self.pid} | {self.log_type} >"

    def to_dict(self) -> dict:
        return {
        	"date": self.date,
            "timestamp": self.timestamp,
            "user": self.user,
            "command": self.command,
            "hostname": self.hostname,
            "pid": self.pid,
            "log_type": self.log_type
        }


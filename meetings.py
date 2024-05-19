import pickle
import os.path
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import messages
import mailene


filePath = "meetings.pickle"
meetings = []

sched = BackgroundScheduler()
sched.start()

def createNewMeeting(dt: datetime, reminderMessage: str):
    loadMeetings()

    meetings.append([dt, reminderMessage])
    startTimerForMeeting(dt, reminderMessage)

    saveMeetings()


def loadMeetingsAfterBoot():
    print("loader møder")   

    loadMeetings()

    for i in range(len(meetings)):
        meet = meetings[i]
        startTimerForMeeting(meet[0], meet[1])
    
    print(str(len(meetings)) + " møder loaded!")  


def getNextMeeting() -> str:
    pass


def startTimerForMeeting(dt: datetime, reminderMessage: str):
    if (isMeetingLater(dt)):
        startTimer(dt, messages.meetNow + reminderMessage)

        if (isMeetingdayLater(dt)):
            startTimer(dt - timedelta(days=1), messages.meetTomorrow + reminderMessage)



# timer util

def startTimer(dt: datetime, msg: str):
    sched.add_job(mailene.sendReminder, 'date', msg, next_run_time=dt)

def isMeetingdayLater(dt: datetime) -> bool:
    now = datetime.now() + timedelta(days=1)
    return now < dt

def isMeetingLater(dt: datetime) -> bool:
    now = datetime.now()
    return now < dt

# save file util

def loadMeetings():
    if (os.path.isfile(filePath)):
        with open(filePath, 'rb') as file:
            meetings = pickle.load(file)
    else:
        meetings = []

def saveMeetings():
    with open(filePath, 'wb') as file:
        pickle.dump(meetings, file)

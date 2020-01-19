import shutil
import dropbox_transfer
import sched, time
from program_data import BACKUP_PERIOD


def beginPeriodicBackup(sc):
    dropbox_transfer.beginTransfer()
    s.enter(BACKUP_PERIOD, 1, beginPeriodicBackup, (sc,))   # recursive run in backup_timeperiod


if __name__ == '__main__':
    s = sched.scheduler(time.time, time.sleep)              # setup scheduler to run
    s.enter(1, 1, beginPeriodicBackup, (s,))                # init run in 1 second 
    s.run()
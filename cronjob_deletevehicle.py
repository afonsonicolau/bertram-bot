# This cronjob checks the "is_deleted" column for timestamps that have exceed 30 days to delete the row
import sql
from datetime import datetime

def check_timestamp():
    if sql.open_connection():
        date_now = datetime.today()
        date_now = date_now.strftime('%Y/%m/%d')

        cursor = sql.connect_cursor()
        cursor.execute("SELECT plate FROM owned_vehicles WHERE is_deleted IS NOT NULL AND DATEDIFF(DATE(NOW()), DATE(is_deleted)) >= 0")
        vehicles = cursor.fetchall()

        log_file = open("cronjob_logs.txt", "a")

        if len(vehicles) > 0:
            print(vehicles)
            log_file.writelines("\n\n***Cronjob - Delete expired vehicles*** - " + date_now)

            i = 1
            while i <= len(vehicles):
                for plate in vehicles[i - 1]:
                    print(plate)
                    log_file.writelines("\nThe vehicle with the plate '" + plate + "' was deleted from the database.")
                    query = "DELETE FROM owned_vehicles WHERE is_deleted IS NOT NULL AND DATEDIFF(DATE(NOW()), DATE(is_deleted)) > 30"
                    break

                i += 1
        else:
            log_file.writelines("\n\n***Cronjob - Delete expired vehicles*** - " + date_now + "\n No cars were deleted on this day.")

        log_file.close()

    sql.close_connection()

if __name__ == "__main__":
    check_timestamp()

""" from crontab import CronTab
from datetime import datetime

cron_user = CronTab(user='nicolau')

job = cron_user.new(command='python home/nicolau/git/bertram-bot/cronjob_deletevehicle.py')
job.minute.every(1)

for job in cron_user:
    myFile = open('crontab_logs.txt', 'a')
    myFile.write('\nAccessed on ' + str(datetime.now()))
    print(job) """

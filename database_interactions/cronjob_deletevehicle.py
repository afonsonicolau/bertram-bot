#!/home/nicolau/git/bertram-bot/bertram-bot/bin/python3

# This cronjob checks the "is_deleted" column for timestamps that have exceed 30 days to delete the row
import services.sql as sql
from datetime import datetime


def check_timestamp():
    if sql.open_connection():
        date_now = datetime.today()
        date_now = date_now.strftime('%Y/%m/%d %H:%M')

        cursor = sql.connect_cursor()
        cursor.execute("SELECT plate FROM owned_vehicles WHERE is_deleted IS NOT NULL AND DATEDIFF(DATE(NOW()), DATE(is_deleted)) >= 30")
        vehicles = cursor.fetchall()

        log_file = open("cronjob_logs.txt", "a")
        vehicle_plates = [plate[0] for plate in vehicles]

        if len(vehicles) > 0:
            log_file.writelines("\n\n***Cronjob - Delete expired vehicles*** - " + date_now)
            log_file.writelines("\nThe following vehicles were deleted from the database: " + ", ".join(vehicle_plates))

            sql.run_query("CALL delete_vehicle()", '')
        else:
            log_file.writelines("\n\n***Cronjob - Delete expired vehicles*** - " + date_now + "\n No cars were deleted on this day.")

        log_file.close()

    sql.close_connection()


check_timestamp()

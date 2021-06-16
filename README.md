# bertram-bot
***
## Bertram's Objectives

### Cronjob to run "delete_vehicle" script every day
0 0 * * * cd /home/nicolau/git/bertram-bot/ && ./cronjob_deletevehicle.py 2>&1 > /tmp/output.log

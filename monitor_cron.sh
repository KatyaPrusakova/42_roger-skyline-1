	#!/bin/bash
	now = `md5sum /etc/crontab`
	old = "/home/amamy/cron_tab_status"

	if [ "$now" != "$old" ]; then
		echo "Crontab has been modified" | mail -s "Crontab has been modified" root
	fi
	md5sum /etc/crontab > /home/new_eprusako/cron_tab_status

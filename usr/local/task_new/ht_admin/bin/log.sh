#!/usr/local/bin/bash
filename=`date +%Y%m%d`
oldname=`date -v-30d +%Y%m%d`

/bin/rm -f /var/log/nginx-access_${filename}.log /var/log/nginx-access_${filename}.log.gz
/bin/ln /var/log/nginx-access.log /var/log/nginx-access_${filename}.log
/usr/bin/touch /var/log/nginx-access-tt.log
/usr/sbin/chown root:wheel /var/log/nginx-access-tt.log
/bin/mv /var/log/nginx-access-tt.log /var/log/nginx-access.log

/bin/rm -f /var/log/nginx-error_${filename}.log /var/log/nginx-error_${filename}.log.gz
/bin/ln /var/log/nginx-error.log /var/log/nginx-error_${filename}.log
/usr/bin/touch /var/log/nginx-error-tt.log
/usr/sbin/chown root:wheel /var/log/nginx-error-tt.log
/bin/mv /var/log/nginx-error-tt.log /var/log/nginx-error.log

/usr/local/etc/rc.d/nginx restart
/bin/sleep 1

/usr/bin/gzip -9 /var/log/nginx-access_${filename}.log /var/log/nginx-error_${filename}.log 
/bin/rm -f /var/log/nginx-access_${oldname}.log.gz /var/log/nginx-error_${oldname}.log.gz

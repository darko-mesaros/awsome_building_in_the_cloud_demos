yum -y update
yum -y install httpd
service httpd start
service enable httpd
# Instance magic
INSTANCEID=`curl http://169.254.169.254/latest/dynamic/instance-identity/document|grep instanceId | awk -F\" '{print $4}'`
echo "<h1>Super Amazing Website</h1>" > /var/www/html/index.html
echo "Welcome our Web app - running on instance: " $INSTANCEID >> /var/www/html/index.html


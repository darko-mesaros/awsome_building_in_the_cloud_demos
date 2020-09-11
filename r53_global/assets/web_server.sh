yum -y update
yum -y install httpd
service httpd start
service enable httpd
# Region magic
REGION=`curl http://169.254.169.254/latest/dynamic/instance-identity/document|grep region|awk -F\" '{print $4}'`
echo "<h1>Super Amazing Website</h1>" > /var/www/html/index.html
echo "Welcome our Web app - running in" $REGION >> /var/www/html/index.html


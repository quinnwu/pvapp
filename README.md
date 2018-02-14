# pvapp
Pennvention Landing Page

To edit the code in real-time for the near future:
1. Download the "pennvention-app.pem" file from the repo.
2. Open up Terminal (Mac) or Powershell (Windows) and change the directory to the one containing the pem file. If the file was not moved, you should go to the Downloads folder. For example, on Mac, you would type `cd ~/Downloads`. You can check if the file is there by typing `find pennvention-app.pem`
3. Then, you will need to connect to the AWS EC2 Instance, which you can do by typing the following: ```ssh -i "pennvention-app.pem" ubuntu@54.147.222.177```
4. It should load a bash line that shows the user as `ubuntu@ip-172-31-11-163`. You can then type `cd /var/www/pvapp` to find the main directory and then from there type `cd pvapp/templates` to find the main html files that one can edit to change the basic front-end text, etc.
5. Head to http://ec2-54-147-222-177.compute-1.amazonaws.com/ to see your changes in real time. They will be updated on pennvention.io as well but with a slight delay as it contacts the hostname server.

**NOTE: After downloading code, edit folder name for "venv1" to "venv".**

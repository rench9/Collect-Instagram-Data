# Installation on amazon ec2 Instance #

1.Update the installed packages and package cache on your machine.

`sudo yum update -y`

2.Install the most recent Docker Community Edition package.

`sudo yum install -y docker`

3.Start the Docker service.

`sudo service docker start`

4.Add the ec2-user to the docker group so you can execute Docker commands without using sudo.

`sudo usermod -a -G docker ec2-user`

5.Log out and log back in again to pick up the new docker group permissions.

6.Verify that the ec2-user can run Docker commands without sudo.

`docker info`



7.Download the latest version of Docker Compose, use the latest Compose release number in the download command.

``sudo curl -L https://github.com/docker/compose/releases/download/1.16.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose``

To ensure you have the latest version, check the Compose repository release page on GitHub.

8.Apply executable permissions to the binary:

`sudo chmod +x /usr/local/bin/docker-compose`

9.Test the installation.

`docker-compose --version`

# Execution #

1.Clone the GIT repo(This is private repository, will ask for password).

`git clone https://github.com/rench9/Collect-Instagram-Data.git`

2.Change directory

`cd webapp`

3.Compose the image and run container.

`docker-compose up`

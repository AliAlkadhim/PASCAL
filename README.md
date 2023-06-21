





## *PASCAL=Python+SQL*, or, if you like *Python Analysis and SQL Computation and Logic*.


<br>

[PASCAL](https://hub.docker.com/repository/docker/alialkadhim/pascal/general) is a docker image that provides tools for retrieval and analysis of the data in the INT2R HGCAL database with python or in the terminal. 

> **Click on "Pages" on the left tab to read more about the HGCAL database.**


<br>
This document assumes that you have docker installed already. If you are unfamiliar with docker or installing/running it, see the [Docker tutorial I wrote below](#Docker_Tutorials). This assumes you don't have a mac with the recent M1 chip (blame Apple for this). 







## Run a tutorial jupyter notebook interactively

### 1. Pull the [image](https://hub.docker.com/repository/docker/alialkadhim/pascal/general)
```bash
docker pull alialkadhim/pascal
```

### 2. Run the image in an interactive container:


Long command (preferred):

```bash
sudo docker run --net=host -e DISPLAY=$DISPLAY --volume="$HOME/.Xauthority:/root/.Xauthority:rw" --volume="/tmp/.X11-unix:/tmp/.X11-unix" -p 8888:8888 -it alialkadhim/pascal /bin/bash
```
Short command (works):

```bash
sudo docker run --net=host -p 8888:8888 -it alialkadhim/pascal /bin/bash
```

### 3. Now you're inside the docker container. Your working directory is `/home/`: See what's there! Establish an ssh tunnel to `lxplus`: do the following inside the docker container


```bash
bash tunnel.sh <your_cern_username>
```

> `tunnel.sh` is included out of the box in `/home/` directory of the docker container.
If interested, the run command looks like:
```bash 
#!/bin/bash
lsof -ti:10131 | xargs kill -9
lsof -ti:10132 | xargs kill -9
username=$1
ssh -4 -fNL 10131:itrac1609-v.cern.ch:10121 -L 10132:itrac1601-v.cern.ch:10121 $username@lxplus.cern.ch
```

Of course, type "yes" if asked "are you sure?" and enter your CERN account (lxplus)  password.

> Note: If you get an error `bund: address already in use` this means the initial port is already in use in the host machine. Exit the container (by typing `exit`) then on your host (local) machine do `lsof -ti:10131 | xargs kill -9` then start the container again (with the `docker run` command in step 2.

### 4. **Inside the docker container, start a jupyterlab session** using the same port forwarding (8888 in this case):

```bash
jupyter-lab --ip 0.0.0.0 --port 8888 --allow-root &
```


> Note: the `&` at the end is so that you don't lose that terminal! (press enter in terminal to use it). 

### 5. **Now in your host (local) machine**, go to the url that is given to you in the docker terminal (either click it or copy and paste it into your local machine's browser). 

> Note: It will say something like `Or copy and paste one of these URLs:`. If you have some other version of jupyterlab on your local machine, you might have to go to `localhost:8888` in a browser and type the password from the docker container that is shown after `?=""`. Note: some other versions of jupyterlab use token instead of password, the token will be after `lab?token=` once you start jupyter-lab.


### 6. Follow the HGCAL DB Python Query Tutorial in by double-clicking `Pascal_jupyter_tutrial_1.ipynb` in the left tab of the jupyterlab session that you've opened in your browser.


-----
<!--

## Simply execute Common queries in the terminal of the docker container (no jupyterbook)
1. Pull the image (if you haven't already)
```
docker pull alialkadhim/pascal
```

2. Run the image in an interactive container:
```bash
sudo docker run --net=host -e DISPLAY=$DISPLAY --volume="$HOME/.Xauthority:/root/.Xauthority:rw" --volume="/tmp/.X11-unix:/tmp/.X11-unix" -p 8000:8000 -it alialkadhim/pascal /bin/bash
```
3. Now you're inside the docker container. Your working directory is `/home/`: See what's there! Establish an ssh tunnel to `lxplus`: do the follwoing inside the docker container
***Replace `aalkadhi` to your lxplus username in `/home/tunnel.sh` and do `bash tunnel.sh`** *

> `tunnel.sh` is included out of the box in `/home/` directory of the docker container.
If interested, the run command looks like:
```bash
#!/bin/bash
lsof -ti:10131 | xargs kill -9
ssh -4 -fNL 10131:itrac1609-v.cern.ch:10121 -L 10132:itrac1601-v.cern.ch:10121 aalkadhi@lxplus.cern.ch
```

4. Inside the container, either 1. Start a jupyter notebook and follow the tutorial descrubed here, or 2. Execute simple queries as described here. 
------

<! ---
# Jupyter notebook Ideas




# Jupyter notebook Ideas

## Interactive Jupyter notebook for DB Interaction/analysis

We will be using the python module `cx_Oracle` to connect and execute SQL queries for the HGCAL INT2R database. The documentation of `cx_Oracle` is [here](https://cx-oracle.readthedocs.io/en/latest/index.html), but I took care of the installation/configuration, etc, so that you focus on the simplest ways that you can interact with the database.
-->

## Extra recommended (optional) parameters for `docker run` command.
Put this in a file like `RUN_dca_int2e-linux-gui.sh` so that you don't forget these commands

```bash
#!/bin/bash
sudo docker run \
--rm \
--net=host \
-e DISPLAY=$DISPLAY \
--volume="$HOME/.Xauthority:/root/.Xauthority:rw" \
--volume="/tmp/.X11-unix:/tmp/.X11-unix" \
-p 8888:8888 \
-it alialkadhim/pascal \
/bin/bash
```
and do `bash RUN_dca_int2e-linux-gui.sh` to run it.

Here are what the options do
- `-v /media/ali/DATA/DATABASE/DCA:/home/shared` mounts the directory `/media/ali/DATA/DATABASE/DCA` on your local machine (host) to `/home/shared` on the Docker container (client). 

- `-p 8000:8000`  maps the `8000` port of your container to the `8000` port of your real server (the host network), i.e. publishes this port. 
	- The order of ports in the `p` flag is `-p <host-port>:<container-port>`.

- `-it alialkadhim/dca_int2r:linux-gui` run the `alialkadhim/dca_int2r:linux-gui` docker image (username `alialkadhim` , image name: `dca_int2r` , tag: `linux-gui` ) wich can be found on dockerhub here, interactively (meaning when you run it your shell will be inside the docker container).
	- `-i` for interactive. `-t` is for enabling a terminal typing interface (i.e. it makes sure the container will work as a terminal would)


----

<! -- PUT THE INSTRUCTIONS FOR LCD_XML ON THE READTHEDOCS -->

## Features (potentially) to be implemented in the next version 

1. the option to run the docker querieries non-interactively - i.e. a user will be able to do a simple query anywhere in the local machine terminal. (The issue here is the tunnel command, I'll have to figure out a way that the lxplus password can be passed to docker run securely without having to type it).
2. Containarize the queries into functions with one variable, the sensor ID. The user can run the program from anywhere in the terminal by calleing eg 
```docker run pascal whereis Sensor ID 24958```
But allow the possibility for people to enter SQL commands themselves. These commands can be inserted in the command line or called on by typing the command in .txt` or `.sql` file.
3. Make the feature to expert the results of the query into a csv file or a json file. Maybe also ROOT, Yaml
4. Documentation of everything on readthedocs and elsewhere if needed.
5. Add "query helpers" being BOTH: the GUI and/or the voice AI system
6. See if I can use [OpenShift](OpenShift.md) fot it somehow
7. Incorporate AI speech recognition feature likerrrrrrrrrrr r AI assistant that you can talk to.  https://www.ai2sql.io/
8. Make the use of the program improve the program itself, especially for your needs, such that it learns from your queries, like a recommender system. such that the AI tool is able to self-correct  its prediction for what you want.
9. More help for particular queries that  you type by tab support autocompletion.
10. more support arm64 architectures. ((it already works for them Im pretty sure)
11. have one page on readthedocs be my jupyter notebook, maybe it can be opened in Swan like Olia suggested. It will have a button (open in swan)
12. Have a GUI query builder
13. I think this thing should be a web application hosted on [[PaaS or OpenShift]]. Or API. The application would  be a browser, s SQL query, or a SQL query helper with viuce, etc. It will also have the possibility of just starting a jupyter notebook.  
14. Collect info from users on how they liked it and what can be improved
15. Have more complex useful queries, especially for HPK data.
16. add a query with the analogue of "did my sensor upload correctly?"
17. THe system improves itself in the future. Everytime you use it for a query, it remembers that query and  shows that to you.
18. Support uploading results as well 
19. Could be incorporated into Patrick code openshift API
20. hgcweb?

Queries:
- What baseplates and detector parts at what locations.

---

### X forwarding-related flags
see
- https://www.howtogeek.com/devops/how-to-run-gui-applications-in-a-docker-container/
- http://fabiorehm.com/blog/2014/09/11/running-gui-apps-with-docker/
Accessing the X server requires 2 things:
1. The `$DISPLAY` variable pointing to the correct display (usually set to `:0`) 
2. Proper authentication information (`$XAUTHORITY` or `xauth`)
	- `$XAUTHORITY` should point to `~/.Xauthority`. 
		- In Debian, if this environemnt variable is not set, just do `export XAUTHORITY=~/.Xauthority` 
	- also do `xauth list` to find authentication information.
	
You might need to install `xauth` so that the container can access the X server. On your host machine do  
```
xauth list | grep `uname -n`
```
and copy the hex key. Then add this display with 
```
xauth add $DISPLAY . hexkey
```


> Note: Other ways to run a GUI inside a docker container is to use SSH with X11 forwarding, or VNC (Virtual Network Computin). See e.g. https://blog.mkari.de/posts/glx-on-mac/
- `--volume="/tmp/.X11-unix:/tmp/.X11-unix"` is a bind mount of the X server directory to the container.
- `--volume="$HOME/.Xauthority:/root/.Xauthority:rw"` is providing your host's X socket to the docker container - **it gives the container the required credentials** .The X socket can be found in `/tmp/.X11-unix` on your host.

- `--env="DISPLAY"`  is providing the container with a `DISPLAY` environment variable (so that a gui, i.e. an X client, can can connect to the X server.) 
	- Do `echo $DISPLAY` to see 
	- We are setting the `DISPLAY` variable in the container to the value of `$DISPLAY` on the host. This is usually set to `:0`. The number is just to distinguish with different displays. For example the socket file `/etc/.X11-unix/X0` or `/tmp/.X11-unix/X0` uses the `:0` display.
	- `-e DISPLAY=$DISPLAY` is equivalent to `--env="DISPLAY"`
- - `--net=host` makes the programs inside the docker container look like they are running on the host itself, from the perspective of the network.

----

### A bit of discussion of what programs are installed in the docker: 
- oracle-instantClient 
- python3.7
- `sqlite3`  
-  `cx-Oracle==7.0.0` which uses the installed `oracle-instantClient` with their versions corresponding to those that host `int2r`. cx_oracle documentation: https://cx-oracle.readthedocs.io/
- jupyter-lab
- a bunch of base software like wget, git, openssl, etc. 
The Oracle Instant Client libraries provide the necessary network connectivity, as well as Oracle Database client-side files to create and run Oracle Call Interface (OCI), Oracle C++ Call Interface (OCCI), ODBC, and JDBC OCI applications to make full use of Oracle Database.

Installation instructions: https://docs.oracle.com/en/database/oracle/oracle-database/21/lacli/install-instant-client-using-zip.html#GUID-D3DCB4FB-D3CA-4C25-BE48-3A1FB5A22E84

### A bit of discussion of what files are inside the docker


After you  `docker pull` and `docker run -it ...` as described above, your working directory is `/home`. Do
```
tree
```
- Tutorials (Docker, Django, SQL, Docker run, ssh)
- Other docs/tutorials: I don't want to overwhelm the user with many docs, so I only include a handful that I think are the most useful to the user. These are:
	- Aivarus presentation
	- My presentation from Dec. 13 2022
	- Umesh document on DB layout/templates
- tunnel.sh
- tns.ora
- Pascal_Tutorial1_V1.ipynb

-----
----

## SQL Tutorial in Context of HGCAL DB 

A Quick Tutorial on SQL Queries for HGCAL Database; Most of These are Included in the [PASCAL Docker Image](https://hub.docker.com/repository/docker/alialkadhim/pascal/general). Currently a few basic ones are included based on what should be included by Alex and Ludivine.
<!-- USE BIND VARIABLES IN QUERIES 
https://cx-oracle.readthedocs.io/en/latest/user_guide/bind.html
see https://cx-oracle.readthedocs.io/en/latest/user_guide/tracing_sql.html for connection class
-->

SQL is the universal way to read data from relational databases. In a nutshell, for reading data, the SQL command is 

```sql
SELECT column_name1, column_name2 FROM table_name WHERE condition1;
```

Where in the above example, we made a query to display columns `column_name1` and `column_name2` from a table called `table_name` subject to `condition1`. 

In the HGCAL database, we have many schemas where our tables exist. See [this page](https://readthedocs.web.cern.ch/display/HGCLogic/HGCAL+DB+tables+-+documentation+for+assembly) for more information on the structure of the HGCAL database.

For the HGCAL data we sometimes need to use some `Inner join` commands. Basically `inner join` lets you join your initial table with another table, at a particular field that is the same in both tables. Think of what the following SQL query would do:

```sql
SELECT StudentName, ClassName FROM Student INNER JOIN Class ON Class.ClassId = Student.ClassId WHERE Class.ClassId = 1
```


You should think of the `CMS_HGC_CORE_COND.COND_DATA_SETS` table as the master table that has a record of everything that was uploaded, and the `CONDITION_DATA_SET_ID` as the successful upload ID that relates schemas and tables.

- See all attempts to upload and their success/failure status and their logs. Replace "Ali" with the name of the user who aploaded something, and you should see it, whether it was uploaded successfully and a log file associated with it!

```
select * from CMS_HGC_CORE_MANAGEMNT.CONDITIONS_DATA_AUDITLOG where RECORD_LASTUPDATE_USER LIKE 'Ali%';
```

- See Everything uploaded by Chaochen:
```
- QUERY_EVA="select * from CMS_HGC_CORE_MANAGEMNT.CONDITIONS_DATA_AUDITLOG where RECORD_LASTUPDATE_USER LIKE 'Chao%'"
execute_query(QUERY_EVA)
```

- See any upload to the database by the user whose name starts with "Ali". Explanation: the `CONDITIONS_DATA_AUDITLOG` has a record and log file of uploads/attempt to upload. Replace "Ali" with the name of the user who aploaded something, and you should see it, whether it was uploaded successfully and a log file associated with it!
```
select * from CMS_HGC_CORE_MANAGEMNT.CONDITIONS_DATA_AUDITLOG where RECORD_LASTUPDATE_USER LIKE 'Ali%';
```

- See the names of all the tables in the `CMS_HGC_HGCAL_COND` account (and the number of rows in each)  
```
select table_name, num_rows
from all_tables
  where owner='CMS_HGC_HGCAL_COND';
  ```
  
- see everythong in the `hcg_cern_sensor_ivl` table:
```
select * from CMS_HGC_HGCAL_COND.hgc_cern_sensor_iv;
```
- See the uploaded registered parts (wafers), ordered by the time they were uploaded to the database:
```
select * from CMS_HGC_CORE_CONSTRUCT.PARTS order by RECORD_INSERTION_TIME ASC;
```

- See the registered wafer that has serial number "100113":
```
select * from CMS_HGC_CORE_CONSTRUCT.PARTS where SERIAL_NUMBER='100113'; 
```
- See the uploaded wafer kind of part ID that was uploaded by the user "`Alex%`" (i.e. it matches any user name that starts with "Alex").
```
select  KIND_OF_PART_ID, NAME_LABEL
from CMS_HGC_CORE_CONSTRUCT.PARTS Where RECORD_INSERTION_USER LIKE 'Alex%';
```

For the HGCAL data we sometimes need to use some `Inner join` commands in our SQL query. Basically `inner join` lets you join your initial table with another table, at a particular field that is the same in both tables.

- stupid way to see the first CV table that I uploaded.
```
select * from CMS_HGC_HGCAL_COND.HGC_CERN_SENSOR_CV
INNER JOIN CMS_HGC_CORE_COND.COND_DATA_SETS
ON CMS_HGC_HGCAL_COND.HGC_CERN_SENSOR_CV.CONDITION_DATA_SET_ID = CMS_HGC_CORE_COND.COND_DATA_SETS.CONDITION_DATA_SET_ID
where CMS_HGC_CORE_COND.COND_DATA_SETS.RECORD_INSERTION_USER LIKE '%Ali%'
ORDER BY CELL_NR;
```

- Original CV SQL query from Umesh:

```
SELECT SNSRPRT.SERIAL_NUMBER CERNSNSR, SNSRCEL.SERIAL_NUMBER SNSR_CELL, HGCSNSRCV.VOLTS, HGCSNSRCV.CPCTNCE_PFRD,  HGCSNSRCV.ERR_CPCTNC_PFRD, HGCSNSRCV.TOT_CURNT_NANOAMP, HGCSNSRCV.ACTUAL_VOLTS, HGCSNSRCV.ORG_CPCTNC_PFRD, HGCSNSRCV.TEMP_DEGC, HGCSNSRCV.HUMIDITY_PRCNT, HGCSNSRCV.IMP_OHM, HGCSNSRCV.PHS_RAD, HGCSNSRCV.TIME_SECS, HGCSNSRCV.CELL_NR  
FROM CMS_HGC_CORE_CONSTRUCT.KINDS_OF_PARTS SNSRKOP
INNER JOIN CMS_HGC_CORE_CONSTRUCT.PARTS SNSRPRT
ON SNSRKOP.KIND_OF_PART_ID = SNSRPRT.KIND_OF_PART_ID
INNER JOIN CMS_HGC_CORE_CONSTRUCT.PHYSICAL_PARTS_TREE SNSRPHPRT
ON SNSRPRT.PART_ID = SNSRPHPRT.PART_PARENT_ID
INNER JOIN CMS_HGC_CORE_CONSTRUCT.PARTS SNSRCEL
ON SNSRPHPRT.PART_ID = SNSRCEL.PART_ID
INNER JOIN CMS_HGC_CORE_CONSTRUCT.KINDS_OF_PARTS CELLKOP
ON SNSRCEL.KIND_OF_PART_ID = CELLKOP.KIND_OF_PART_ID
INNER JOIN CMS_HGC_CORE_COND.COND_DATA_SETS CONDS
ON SNSRCEL.PART_ID = CONDS.PART_ID
INNER JOIN CMS_HGC_CORE_COND.KINDS_OF_CONDITIONS SNSRCVKOC
ON CONDS.KIND_OF_CONDITION_ID = SNSRCVKOC.KIND_OF_CONDITION_ID
INNER JOIN CMS_HGC_HGCAL_COND.HGC_CERN_SENSOR_CV HGCSNSRCV
ON CONDS.CONDITION_DATA_SET_ID = HGCSNSRCV.CONDITION_DATA_SET_ID
WHERE SNSRKOP.DISPLAY_NAME = 'HGC Sensor Wafer'
AND SNSRPRT.IS_RECORD_DELETED = 'F'
AND SNSRCEL.IS_RECORD_DELETED = 'F'
AND CELLKOP.IS_RECORD_DELETED= 'F'
AND CELLKOP.DISPLAY_NAME = 'HGC Sensor'
AND CONDS.IS_RECORD_DELETED = 'F'
AND SNSRCVKOC.NAME = 'HGC CERN Sensor CV'
AND SNSRCVKOC.IS_RECORD_DELETED = 'F'
ORDER BY CERNSNSR, SNSR_CELL, VOLTS;
```
In the query above, `AS` is implicit, so `SELECT SNSRPRT.SERIAL_NUMBER CERNSNSR` is the same as `SELECT SNSRPRT.SERIAL_NUMBER AS CERNSNSR`

- Query CV table by scratchpad by me influenced from the Umesh one above. This shows all the columns that we uplokaded data for in our XML template, for the sensor with  serial number (scratchpad ID) `200144`:
```
SELECT SNSRPRT.SERIAL_NUMBER SCRATCHPAD_ID, 
SNSRPRT.NAME_LABEL SENSOR_ID,
SNSRCEL.SERIAL_NUMBER SCRATCHPAD_ID_CELL, 
HGCSNSRCV.VOLTS, 
HGCSNSRCV.CPCTNCE_PFRD,  
HGCSNSRCV.ERR_CPCTNC_PFRD, 
HGCSNSRCV.TOT_CURNT_NANOAMP, 
HGCSNSRCV.ACTUAL_VOLTS, 
HGCSNSRCV.ORG_CPCTNC_PFRD, 
HGCSNSRCV.TEMP_DEGC, 
HGCSNSRCV.HUMIDITY_PRCNT, 
HGCSNSRCV.IMP_OHM, 
HGCSNSRCV.PHS_RAD, 
HGCSNSRCV.TIME_SECS, 
HGCSNSRCV.CELL_NR  
FROM CMS_HGC_CORE_CONSTRUCT.KINDS_OF_PARTS SNSRKOP
INNER JOIN CMS_HGC_CORE_CONSTRUCT.PARTS SNSRPRT
ON SNSRKOP.KIND_OF_PART_ID = SNSRPRT.KIND_OF_PART_ID
INNER JOIN CMS_HGC_CORE_CONSTRUCT.PHYSICAL_PARTS_TREE SNSRPHPRT
ON SNSRPRT.PART_ID = SNSRPHPRT.PART_PARENT_ID
INNER JOIN CMS_HGC_CORE_CONSTRUCT.PARTS SNSRCEL
ON SNSRPHPRT.PART_ID = SNSRCEL.PART_ID
INNER JOIN CMS_HGC_CORE_CONSTRUCT.KINDS_OF_PARTS CELLKOP
ON SNSRCEL.KIND_OF_PART_ID = CELLKOP.KIND_OF_PART_ID
INNER JOIN CMS_HGC_CORE_COND.COND_DATA_SETS CONDS
ON SNSRCEL.PART_ID = CONDS.PART_ID
INNER JOIN CMS_HGC_CORE_COND.KINDS_OF_CONDITIONS SNSRCVKOC
ON CONDS.KIND_OF_CONDITION_ID = SNSRCVKOC.KIND_OF_CONDITION_ID
INNER JOIN CMS_HGC_HGCAL_COND.HGC_CERN_SENSOR_CV HGCSNSRCV
ON CONDS.CONDITION_DATA_SET_ID = HGCSNSRCV.CONDITION_DATA_SET_ID

WHERE CONDS.IS_RECORD_DELETED = 'F'
AND SNSRCVKOC.NAME = 'HGC CERN Sensor CV'
AND SNSRCVKOC.IS_RECORD_DELETED = 'F'
AND SNSRPRT.SERIAL_NUMBER = '200144'
ORDER BY CELL_NR, VOLTS;
```


------
________

# Docker_Tutorials 

<!-- <a name="docker_tutorial"></a> -->


I am a huge fan of [docker](https://www.docker.com/), and I think now is the time that we all should use and embrace it in HEP, just like we've used and embraced other revolutionary tools such as git. I hope this first version of these simple tutorials help in this aim.


## Explore Docker on a web playground

Go to https://labs.play-with-docker.com/ where you play with docker and its commands, and pull images, etc.

----
## Essential commands: 

- `docker pull <image_name>:<tag>` (download a docker image from [dockerhub](https://hub.docker.com/) , which is a registry maintained by Docker, Inc.)
- `docker image ls` (see list of installed images)
	- This is equivalent to `docker images`. You can also view all intermediate images with `docker images -a` , since each image is made up of many intermediate images.
		- You can see the dangling images by `docker images --filter "dangling=true"` which will have `<none>` for name and tag. You can remove them, of course, by doing `docker rmi -f $(docker images -q --filter "dangling=true")`
			- Hint: why don't you just put it as `alias remove_dangling='docker rmi -f $(docker images -q --filter "dangling=true")'` in your `~/.bashrc`?
- `docker run -it <image_name>:<tag>` (run a docker image interactively)
	- Although I tend to use the interactive running of docker images, sometimes it is much more powerful to run it for a single command. See `CMD` in the [Dockerfile_Tutorials_V1-Ali](Dockerfile_Tutorials_V1-Ali.md) tutorial.
- `docker rmi -f <image_name>:<tag>` (force remove an installed image)
- `docker ps -a` (see list of running docker containers)
- `docker rm <container_id>` (remove a running docker container)

----

## Docker Installation (linux)

To install, see [this link](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-debian-10). Just follow **Step #1**.

To **see the status of the daemon** you can either do 

```bash
sudo service docker status
```

If you get an error message like "service command supports only basic LSB actions..." you have a `systemd` based startup system. Do

```bash
sudo systemctl status docker
```

or best for debian apparently is `sudo systemctl start docker.service` or `sudo /etc/init.d/docker start`

**start the daemon**

```bash
sudo service docker start
```

or

```bash
sudo systemctl start docker
```


## Docker Client and Daemon

Docker is made of 2 parts: a docker daemon and a docker client:
- A daemon with a RESTFUL API. This is a server that receives requests and returns responses from the client using HTTP protocol. 
- A client that talks to the daemon. This is the interface between you (your host machine) and the daemon. Your docker commands are instructions that are managed by the client and relayed to the daemon. 


	- As such, the `docker` command is a client, which takes commands and relays them to the docker daemon, which is a server that processes your commands and talks to the outside world.
> But what's a daemon? it is a process that runs in the background rather than under direct control of the user. A server is a process that takes requests from a client and performs the actions necessary to fulfil the requests. Daemons are sometimes also servers.

You can run the container as a daemon with the `-d` flag. You can also specify the name of the container at runtime with the `--name` flag. Example
```
docker run -d --name <container-name (specified here)> <image-name>
```


---
## Docker Uninstall Everything 

To completely remove everything docker do

```bash
sudo apt-get purge -y docker-engine docker docker.io docker-ce docker-ce-cli docker-compose-plugin
sudo apt-get autoremove -y --purge docker-engine docker docker.io docker-ce docker-compose-plugin
```
The above commands will not remove images, containers, volumes, or user created configuration files on your host. 

If you wish to delete all images, containers, and volumes run the following commands:

```bash
sudo rm -rf /var/lib/docker /etc/docker
sudo rm /etc/apparmor.d/docker
sudo groupdel docker
sudo rm -rf /var/run/docker.sock
```

## Docker pull
```
docker pull <image_name>:<tag>
```
(download a docker image from [dockerhub](https://hub.docker.com/) , which is a registry maintained by Docker, Inc.)
The tag "`latest`" often appears, since it is the default for tagging and pulling. It doesn't necessarily mean that this is the last tag set for an image.
	You can use the `search` command to search for an image, if you don't want to visit [dockerhub](https://hub.docker.com/) 
```
docker search <image-name>
```

----
## Docker run
The most essential docker command. Run an image with `docker run <image-name>`. See https://docs.docker.com/engine/reference/run/

suppose we have a `flag` with shortcut `f` , then `--flag="options"` is equivalent to `-f options` .

For most use cases, the image is much more useful when run interactively with

```bash
docker run -it <image-name>
```
But there are many flags which can be set (see [Docker_run_tutorials_V2](Docker_run_tutorials_V2.md)). 

You can assign a name for the running contained, `<container-name>`, with

```bash
docker run --name <container_name> -d <image-name>
```
Now, doing

```bash
docker ps -a
```

Should display the container whose name you assigned as running.

----
## Docker inspect

```bash
docker run --name onstance <image-name>
docker inspect instance
```
This will display a bunch of information about the running docker container, such as its environemnts, hostname, mounted volumes, etc. You can filter one of them with `-f`, e.g.:

```
docker inspect -f "{{ .NetworkSettings.IPAddress }}" <container-name>
```

----
## Docker exec

```
docker run -d --name mycontainer <image-name>
docker exec -it mycontainer /bin/bash
```
The command above starts a container "mycontainer" from the image, and the exec command starts a `/bin/bash` in the running container. The `-it` have the same interactive terminal functionality.

-----
 ## Commit Docker Changes 
 Commit changes to image after you use it, see: https://phoenixnap.com/kb/how-to-commit-changes-to-docker-image
 `docker run -it ... bash` and then `exit`, then `docker ps -a` then `sudo docker commit [CONTAINER_ID] [new_image_name]`
 or just `sudo docker commit latest_container_id`


 Summary: to save results in a docker image, always commit changes from the latest container to the image, i.e. 
**Example 1: commit using container ID and image name**

 ```
 docker run -it myimage:latest
... 

Then `exit`

now you're outside the container. You can view the container or commit your image.

```
docker ps -a 
docker commit <latest_container_id> <myimage>:latest
 ```


NOTE that committing a comntainer does not store the processes of the container, it only stores the state of the filesystem.

**Example 2: commit using a named container**
```
docker run -d --name container1 <image-name>
docker exec -it container1 /bin/bash
~ do a bunch of bash commands ~
docker commit container1
```


----

## Running docker containers: To keep or to `rm` ?

Once you exit a particular container than you used with just, say, `docker run -it <image-name>` , and `exit` that container, the container will be still running. You can check this by doing `docker ps -a` after you `exit`. If you keep doing this, a bunch of containers will be running in the background, so it's good to tell docker to remove the container after you stop it. This can be done with the `--rm` flag, e.g.

```bash
docker run --rm -it <image-name>
```

You can instead just remove all these dangling containers every once in a while by doing

```bash
docker rm -f $(docker ps -a -q)
```



-------
## Remove all images 

```bash
docker rmi $(docker images -a -q)
```


---
## Prune docker "garbage"
https://docs.docker.com/config/pruning/

Docker provides a single command that will clean up any resources — images, containers, volumes, and networks — that are dangling (not tagged or associated with a container):

`docker system prune` : very useful. To additionally remove any stopped containers and all unused images (not just dangling images), add the -a flag to the command:

```bash
docker system prune -a
```


To include the volumes as well, do

```bash
docker system prune --volumes
```



---------
## More Useful Commands
useful link for image/container commands
 https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes



-----
## Making a Docker Group

By default only root can execute docker commands, or someone in the docker group. To avoid having to type sudo everytime you want to run a docker command, make a group called `docker` 

```bash
sudo groupadd docker
```

and add your username to the docker group

```
sudo usermod -aG docker ${USER}
```

This adds your user account (`${USER}`) to the docker group (since any command you run from a machine not in the user group will trigger a permission denied error.)

To apply the change in the same shell, do `su - ${USER}`. To confirm that you've been added to the docker group do `id -nG` 

-----
## Permission Denied Errors

See 
- https://www.redhat.com/sysadmin/container-permission-denied-errors
- https://wiki.gentoo.org/wiki/SELinux/Tutorials/Permissive_versus_enforcing
- https://docs.docker.com/storage/bind-mounts/#configure-the-selinux-label
- https://adamtheautomator.com/docker-permission-denied/

- Permission denied errors outside the container, i.e. inside the client when running `docker run ...`: do `sudo docker <command> ` before each docker command, or `su -u` then all the docker commands. Alternatively add a docker group like in the previous section.
- Permission errors inside the container:
	1. add `--privleged` to `docker run`
	2. Check your `SELinux` configurations im `/etc/selinux/config` (or  `/etc/selinux/semanage.conf`) and comment out `SELINUX=permissive`
		- If a system is `SELinux`-enabled then the policiy will be active and will be in "enforcing" mode. Disable with "permissive" mode.
	3. `sudo setenforce 0`.
  
  -------
  

 
  ## Example: runnning madminer with jupyter and docker

We'll use the concepts we learned so far to run [madminer](https://github.com/madminer-tool/madminer). Put something like the following in a `docker_command_madminer.sh` file

```bash
#!/bin/bash
sudo docker run \
    -p 8888:8888 \
    -v /media/ali/DATA/LR_MADMINDER_STUDIES/madminer_shared:/home/shared \
    -it madminertool/madminer-jupyter-env:0.3.3 \
    /bin/bash
```


to start a jupyter inside the container, make sure that you're using the same port forwarding (8888 in this case) and do
```bash
jupyter-lab --ip 0.0.0.0 --port 8888 --allow-root &
```

the ""&" is so that you dont lose that terminal! (press enter in terminal to use it) 
Now in your host machine, go to `localhost:8888` in a browser and type the password from the docker image after `?=""`. Note: some versions of jupyterlab use token instead of password, the token will be after `lab?token=` once you start jupyter-lab. 

------
## Docker on WSL

On WSL you can get "System has not been booted with systemd as init system (PID 1). Can't operate. Failed to connect to bus: Host is down" as in https://www.linuxtopic.com/2021/11/system-has-not-been-booted-with-systemd.html . Solve with

```bash
sudo dpkg --configure -a
```


```bash
sudo apt-get install -yqq daemonize dbus-user-session fontconfig
```

```bash
sudo systemctl start docker && sudo systemctl enable docker && sudo systemctl restart docker
```

```bash
sudo dpkg --configure -a
sudo apt-get update && sudo apt-get install -yqq daemonize dbus-user-session fontconfig

sudo daemonize /usr/bin/unshare --fork --pid --mount-proc /lib/systemd/systemd --system-unit=basic.target

exec sudo nsenter -t $(pidof systemd) -a su - $LOGNAME

snap version
```
por just with `sudo dockerd` 

also see https://www.youtube.com/watch?v=iIYw0Z0AI1c

----------

## Supported (CPU) architectures (multi-arch images)
CPUs are constructed with a certain type of architecture. Software that's compiled with a certain architecture can't be executed on another.

- Intel chips are built on the `x86` architecture 
	- at 64 bits, called "**x86_64**" or  the oldest being 32 bits,.
	- **amd64 platforms means x86 architectures at 64 bits** 
- Apple's M1 chip (Apple Silicon MX somrhing-C) uses `Arm`-based architecure.
	- **64 bits** (**armv8**) or **32 bits** (**armhf**, **armv6**…) or the most popular one **arm64**.
		- **aarch64** is the 64 bit state introduced in the Armv8-A architecture. "arm64" represents the AArch64 state of the ARMv8-A architecture
- Do `lscpu` to find your architecture information.
	
- docker images often have several tags, each supported on a different architecture. docker images can only be executed if the docker image's architecture matches that of the host machine. If an image has multiple tags, each supporting a different architecture, the correct image is pulled automatically by docker. 
	- E.g. when running an image on an `x86_64` / `amd64` machine, the `amd64` variant (tag) of the image is pulled and run.

- To make things worse, the Apple software end-user license agreement (EULA) only permits OS X on Apple hardware. This means you can't test things out on some cloud computing service such as Google Cloud Platform or AWS. There is for example https://www.macstadium.com/ but it costs money.

The good thing is that [Docker Official Images](https://docs.docker.com/docker-hub/official_images/) (on dockerhub [here](https://hub.docker.com/search?q=&type=image&image_filter=official)) support multiple architectures for their images.

### buildx
To see your architecture, do
```bash
docker buildx ls
```

> (by the way, you could do that in with something way fancy like `docker run python:2 python -c "import platform; print 'Python running on arch: %s' %platform.machine()"`
)
                                                             

The output of this for me is
```
NAME/NODE DRIVER/ENDPOINT STATUS  BUILDKIT PLATFORMS
default * docker                           
  default default         running 20.10.18 linux/amd64, linux/386
```



```bash
docker buildx inspect
```
Gives
![](Pasted%20image%2020230308210411.png)

Now do 
```bash
docker buildx create --name mybuilder --driver docker-container --bootstrap
mybuilder
```

```bash
docker buildx use mybuilder
```

Now `docker buildx inspect` gives
![](Pasted%20image%2020230308210808.png)

- Checkout https://hub.docker.com/r/sickcodes/docker-osx to test Mac architectures in docker.




### mplatform
```bash
docker run --rm mplatform/mquery <image_nae>:<tag>"
```

Or, to see the supported architectures for an image:

```bash
docker buildx imagetools inspect image_name
```



- See e.g. https://github.com/docker-library/official-images#multiple-architectures for more in depth info.

### manifest
A **manifest** is a JSON file containing all the image layers and their descroption (including the architecutre). You can fine the manifest by doing
```bash
docker manifest inspect --verbose username/<image-name>:<tag>
```


<!--There are two ways to use Docker to build a multiarch image: using `docker manifest` or using `docker buildx`. -->


-----
## push docker image to dockerhub

```bash
docker login
```
(enter your docker username and password)
Then 
```bash
docker tag <image>:<tag> <username>/<image>:<tag>
```


```bash
docker push <username>/<image>:<tag>
```
(without the tag)
Now anyone can pull your image from dockerhub and use it.

------------
## CERN-related docker stuff
- ATLAS ARM arch: https://gitlab.cern.ch/atlas-tdaq-software/tdaq-arm
- [[systemd quick intro - Ali]] enabled centos image: https://github.com/docker-library/docs/tree/master/centos#systemd-integration
- Docker HATS https://indico.cern.ch/event/957654/
- Cern CentOS  http://linuxsoft.cern.ch/
----
## Using Cached Images
Building images can take time. Using cached images (decribed, e.g. [here](https://cloud.google.com/build/docs/optimize-builds/speeding-up-builds#:~:text=The%20easiest%20way%20to%20increase,image%20as%20a%20cache%20source.)) can speed it up and use less dangling images.

-----

## Enabling ssh in docker container
https://goteleport.com/blog/shell-access-docker-container-with-ssh-and-docker-exec/
The image must be preconfigured with Openssh to allow ssh service.

---
## Using Docker in a browser: Docker Terminal
github.com/aidanhs/Docker-Terminal.git
----
## Converting a VM to a docker image
This can be done by creating a TAR file of your VM filesystem, using e.g. `qemu-nbd` or `tar` over `ssh`. Then use the `ADD` command in your dockerfile on yout TAR to create your image.





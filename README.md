## *PASCAL=Python+SQL*, or, if you like *Python Analysis and SQL Computation and Logic*.

### The CERN gitlab command line interface version can be found on https://gitlab.cern.ch/aalkadhi/pascal
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

### 5. **Now in your host (local) machine**. Connect to the remote jupyter server by going to the url that is given to you in the docker terminal (either click it or copy and paste it into your local machine's browser). 

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

### 1. The option to run the docker queries non-interactively - i.e. a user will be able to do a simple query anywhere in the local machine terminal. (The issue here is the tunnel command, I'll have to figure out a way that the lxplus password can be passed to docker run securely without having to type it).  

### 2. Containerize the queries into functions with one variable, the sensor ID. The user can run the program from anywhere in the terminal by calling e.g.

```
docker run pascal whereis Sensor ID 24958
```

But allow the possibility for people to enter SQL commands themselves. These commands can be inserted in the command line or called on by typing the command in .txt` or `.sql` file.

> Each query is saved in a .sql file, and the function just opens and grabs these
> **DONE**

### 3. Get input from HGCAL community on what data they would like to retrieve -> containarize into `.sql` templates. E.g. HPK data, tables other than Si sensors.

### 4. Make the feature to expert the results of the query into a csv file or a json file. Maybe also ROOT, Yaml
> **DONE FOR CSV/JSON**


### 5. Make "query helpers" being a GUI query-builder
> **BASICALLY DONE FOR JUPYTER**



### 6. See if I can use [OpenShift](OpenShift.md) for it somehow. I think this thing should be a web application hosted on [[PaaS or OpenShift]]. Or API. The application would  be a browser, s SQL query, or a SQL query helper with voice, etc. It will also have the possibility of just starting a jupyter notebook.

> Related: see if it can talk to Phillip's Module assembly API on Openshift

### 7. Incorporate AI speech recognition feature like AI assistant that you can talk to.  e.g. https://www.ai2sql.io/
Example: saying

> "What baseplates and detector parts at what locations?"

Which would be translated to the correct SQL command and executed with output.

### 8. Make the use of the program improve the program itself, especially for your needs, such that it learns from your queries, like a recommender system. such that the AI tool is able to self-correct  its prediction for what you want.
Related:

> Query History/log. Maybe every time you run `execute_query()`

> Option to Save query if you like it, or put your own query in the queries directory as a .sql  Queries.
> Collect info from users on how they liked it and what can be improved.

### 9. More help for particular queries that you type support autocompletion by tab.


### 10. more support arm64 architectures. (it already works but it's not arm-based)

### 11. have one page on readthedocs be my jupyter notebook, maybe it can be opened in Swan like Olia suggested. It will have a button (open in swan).
  
### 12. Support uploading results as well with dbloader.


### 13. hgcweb?

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
 
 

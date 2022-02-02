<p align="center">
  <i><font size="3">
  	Systems and Methods for Big and Unstructured Data - Delivery #2 - AA 2021/2022 - Prof. Marco Brambilla
  </i>
</p>
<h1 align="center">
	<strong>
	📄 Covid certificates-oriented MongoDB Database
	</strong>
	<br>
</h1>
<p align="center">
<font size="3">
		<a href="https://www.mongodb.com">MongoDB</a>		 
		•		
		<a href="report.pdf">Report</a>   
	</font>
</p>

This project's purpose is to keep track of **COVID-19 pandemic** data about people, authorized bodies, 
vaccines, tests and, most of all, Covid certificates of vaccination or testing by designing and implementing a document-based 
**MongoDB** database. The primary objective is to support a fast tool that checks the validity of the certificate. 
The data stored allows to extract actionable insights concerning various statistical purposes, involving information such as health services, 
vaccination & testing hubs and vaccine lots, even though the database is not optimized for these tasks, since the already mentioned main goal 
regards certificates validity check.


# Contents

- ⚙  [System requirements️](#system-requirements)
- 🚀 [Setup instructions](#-setup-instructions)
- 📜 [Report](report.pdf)
- 👨‍💻 [Usage](#-usage)
	- [Load DB Dump](#load-db-dump) 
	- [Load from CSV](#load-from-csv)
- 🗄️ [Database dump](https://1drv.ms/u/s!Ahq9yFCnfdZEjuoh3BmchG2HiwhAIg?e=zPUwxa)
- 📊 [Diagrams](#-diagrams)
- 📷 [Screenshots](#-screenshots)  
- 📝 [License](#-license)

# System requirements

## Required software

- [Python](https://www.python.org/) 3.8 or higher (only if you want to perform manual load from CSVs)
- [MongoDB](https://www.mongodb.com) database
- Python modules in [requirements.txt](requirements.txt) (only if you want to perform manual load from CSVs)


# 🚀 Setup instructions

## Clone the repo

    git clone https://github.com/pablogiaccaglia/mongodb-covid-certificates
    cd mongodb-covid-certificates/

## Install required packages

From the project's directory run the following commands:

    pip install -r requirements.txt
    
# 👨‍💻 Usage

## Load DB Dump

Download the [database dump](https://1drv.ms/u/s!Ahq9yFCnfdZEjuoh3BmchG2HiwhAIg?e=zPUwxa) and navigate to the folder where it is located, then from the command line run something like this:

```
mongorestore -h host.com:port -d covid_certificates -u username -p password downloads/dumps/
```

Assuming that you want to put the contents of the database into a new database called covid_certificates. 


## Load from CSV

To populate the database from the provided CSVs and Python scripts (from which further customizations of the generated data can be performed), the first step to accomplish is to establish a connection to a MongoDB Server. 
The provided code relies on a **MongoDB Atlas** based connection, but it can easly customized to connect to a MongoDB Server on your local machine, as shown <a href="https://docs.mongodb.com/drivers/pymongo/#connect-to-a-mongodb-server-on-your-local-machine">here</a>.

As you can see in the <a href="scripts/main.py#L289">main</a>  method of the <a href="scripts/main.py">main.py</a> file, a <code>MongoDB</code> object is created in the following way:

```python
    uri = "MONGODB_URI"
    mongoDB = MongoDB(connectionURI = uri)
```

the data passed to the class' constructor is used in the init method to establish a connection through a driver:

```python
   class MongoDB(MongoClient):

    def __init__(self, connectionURI) -> None:
        super(MongoDB, self).__init__(connectionURI, connect = False)
```

After this step all you need to do is execute the main method and wait the routine to complete. 

The Python code manipulates several CSV files which can be found in different versions inside the <a href="datasets">datasets</a> folders.
Detailed information of the manipulation process which lead to the final state of the database can be found in the <a href="report.pdf">Report</a>.

# 📊 Diagrams

<h2><p align="center"><b>ER Diagram</b></></h2>

 <p align= "center">
 <kbd> 
 <img src="report/latex/mongodb-er.png" align="center" />
 </kbd>
 </>
	 
---
	 
<h2><p align="center"><b>Document Diagram</b></></h2>

 <p align= "center">
 <kbd> 
 <img src="report/latex/mongodb-docdiagram.png" align="center" />
 </kbd>
 </>
	 
---

# 📷 Screenshots


# 📝 License

This file is part of "Covid certificates-oriented MongoDB Database".

"Covid certificates-oriented MongoDB Database" is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

"Covid certificates-oriented MongoDB Database" is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program (LICENSE.txt).  If not, see <http://www.gnu.org/licenses/>

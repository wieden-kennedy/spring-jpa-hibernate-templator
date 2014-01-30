##spring+jpa+hibernate+rdbms

Take your modeling needs into account, then skip worrying about setting up your Spring Data JPA persistence layer. All you need is one or more models, and the details for your POM.xml file defined in a JSON file, and a few command-line flags.

#####Licensing
This repository is licensed under the BSD 3-Clause license, which you can find [here](LICENSE)

##Table of Contents

- [What gets included in the templator output?](#what-gets-included-when-the-templator-is-run?)
- [Usage](#usage)
    - [Running the templator](#running-the-templator)
    - [Required fields](#required-fields)
    - [Optional fields](#optional-fields)
    - [Sample configuration file](#sample-configuration-file)
- [Additional repository methods](#additional-repository-methods)
- [Related entities (one-to-one, one-to-many)](#related-entities)
- [Sample build](#sample-build)
- [Known issues](#known-issues)
- [To do](#to-do)



##What gets included when the templator is run?
The templator builds the configuration files, the model class files, the service class files, and the repository class files based on your JSON document. A typical output directory would look like this, using the below 'Car' model as an example:

	src
	|---main
		|---java
		|	|---com
		|		|---package
		|			|---identifier
		|				|---config
		|				|   |---AbstractAppConfig.java (Abstract parent class)
		|				|   |---ApplicationConfig.java
		|				|---model
		|				|   |---Car.java
		|				|---repository
		|				|   |---CarRepository.java
		|				|   |---ModelRepository.java (base interface)
		|				|---service
		|				|   |---CarService.java
		|				|   |---CarServiceImpl.java
		|				|   |---ModelService (base interface)
		|---resources
			|---application.properties
							

##Usage
 
###Running the templator
First, clone this repo down to your machine.

Secondly, you'll need is a JSON file that defines the POM.xml and model attributes for your persistence layer. A sample is included in the repo at the root level, so just edit that one if you'd like.

####Required fields:
 - basepackage
 - properties_file_name
 - group_id
 - artifact_id
 - package_name
 - application_properties
 	- database_username
 	- database_password
 	- database_url
 	- database_databasename
 	- database_flavor
 	- hibernate_dialect
 - models
 	(for each model)
 	- model_name
 	- id_type
 	- member_variables
 		(for each member variable)
 		- field_name
 		- type
 		- column
 
####Optional fields (under models)
Currently the only optional fields that you need to know about are for adding [additional repository methods](#additional-repository-methods)
		
####Sample configuration file 		

    {
        "basepackage":"com.wk.lodge.spring.jpatemplate",
        "group_id":"com.wk.lodge",
        "artifact_id":"com.wk.lodge.spring.jpatemplate",
        "package_name":"spring-jpa-hibernate-rdbms",
        "properties_file_name":"application.properties",
        "application_properties":{
        	"database_username":"db_user",
        	"database_password":"********",
        	"database_url":"db.host.url",
        	"database_databasename":"DATABASE",
        	"database_flavor":"mysql",
        	"hibernate_dialect":"MySQL5Dialect"
    	},
        "models": [
             {
                 "model_name":"Car",
                 "id_type": "Long",
                 "member_variables":[
                    {
                         "field_name": "inserted",
                         "type": "long",
                         "column": "INSERTED_AT"
                    },
                    {
                        "field_name":"model",
                        "type":"String",
                        "column":"MODEL"
                    },
                    {
                        "field_name":"make",
                        "type":"String",
                        "column":"MAKE"
                    },
                    {
                        "field_name":"color",
                        "type":"String",
                        "column":"COLOR"
                    },
                    {
                        "field_name": "year",
                        "type": "int",
                        "column": "YEAR"
                    }
                 ],
                 "additional_query_methods":[
                    {
                        "name":"findMadeEarlierThan",
                        "returns":"List<Car>",
                        "query":"SELECT c FROM Car c WHERE c.year < :year",
                        "params":[
                            {
                                "name":"year",
                                "type":"int"
                            }
                        ]
                    }
                 ]
             }
         ]
    }

Lastly, just run the templator.py file found in the base path of this project, using command-line flags:
    
    python main.py

and don't forget those command line options (none required, but all useful):

    -f path to the file (defaults to './model.json')
    -o outpath where the source directory should be saved (defaults to current working directory)
    -j create a jar package
    -i install the jar package locally instead of outputting to [out_path]/target/
    -l path to license file to be added to top of each generated class


And shazzam! You've got the source and jar files for wiring up a persistence layer built on Spring Data JPA using Hibernate.

###Additional repository methods
Defining additional query methods in the model JSON file is shown above. To define queries in addition to the standard JPA Repository interface's queries, you will want to add the property "additional_query_methods" to each model that requires them. Here's a more detailed look at the structure:

	"name": "the name of the query method",
	"returns": "the return type you expect from the query",
	"query": "the JPA Query used to query the database",
	"params": [ //array of parameters used in the query
		{
			"name":"the name of your parameter",
			"type":"the Java parameter type"
		}
	 ]

If you would prefer to not add in query methods before you run templator, you can still add queries later in one of two ways:

1. Run the templator, but don't include the -j flag. This will just output the source to a directory, where you can add in the custom methods to your repository and service classes before you package the jar up. After you've added the methods you need, navigate to the root of the source directory and run 

	```
    mvn clean package 
    -or-
    mvn clean install
	```

2. You can build the jar as is by passing the -j flag to the run. After you bring in the jar, just extend the repository and service classes, adding in your own query methods as you wish.

###Related Entities
While adding support is in the works for related entities by OneToOne or OneToMany relationships, eager/lazy loading, et al, at present it is best to render the templated persistence layer, then add your own relationship annotations and markup after outputting the source directory to an output path of your choosing:

1. Run the templator as described above, making sure to add an output path using the -o parameter.
2. Open your new persistence source and add your relationships/annotations and/or additional query methods you will need to relate and query them.
3. Run a maven install from the root directory of your persistence layer.


###Sample Build
To see what happens when you run the templator, clone this repo down, cd into it, and run:

    python main.py -f ./templates/_samples/sample_model.json -l ./templates/_samples/sample_license.txt -o /tmp/sample-persistence-layer

###Known Issues
Error handling for required properties that are not included in the models JSON file has not yet been added. Omitting any of the above-listed required properties will throw an error in the build process.

###To-do
 - write tests
 - add in exception handling and error checking
 - add (better) support for additional service/repository methods with @Query
 - add in support for relating entities


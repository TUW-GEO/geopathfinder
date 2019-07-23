=============
geopathfinder
=============


A package for creating, quering, and searching in data structures holding geo data sets.


Description
===========

This packages aims to provide a rich toolbox for efficient, quick, and precise handling of filenames and folder structures for geo-data, most conviniently when combined with grid objects as e.g. the https://github.com/TUW-GEO/Equi7Grid.

With pre-defined sets comprising string-definitions, folder path logics, and filename en-/decoders, a variety of file/folder naming conventions can be implemented.

The base classes SmartPath() and SmartTree() comprise also functions for file search and folder(-tree) volume determination.


Adding a new filenaming convention
--------------------------------
In general, please follow the code and test guidelines of existing naming conventions.
The following description aims to show how to implement a new naming convention:

- Create a new .py file in the folder "geopathfinder/naming_conventions/". The filename should be an abbreviation of the new naming convention separated from "naming" with an underscore, e.g., "sgrt_naming.py" ot "eodr_naming.py".

- Inside this file, write a new class, which inherits from *SmartFilename*. In this class you can define how the filename structure should look like. For each field you can define the length of the field ('len', integer), if a delimiter should be in between the current and the previous part of the filename ('delim', boolean) and finally, if desired, a decoding and encoding function ('decoder', 'encoder'). The latter parameters should point via a lambda function to a decoding or encoding method defined in the same class.

- Finally, the parent class *SmartFilename* can be initiated with the given fields, fields definitions, a padding, a delimiter and a boolean value if en-/decoding should be applied or not.

- Sometimes one needs information from the filename, which can be directly derived from one or multiple filename entries. An example would be a mean date derived from the start and end date specified in the filename.
  To allow this, one can define methods tagged with *property* in the current class. *SmartFilename* then handles the properties of the inherited class equally to a common filename entry given in the field definition.
  
- The second important part is the functionality of parsing a string following the new filenaming convention. To do so,
  create a new function below the class definition. It should be named "create_[]_filename", where "[]" should be replaced by the abbreviation of the new naming convention.
  This function should split the filename string into parts needed for initialising a fields dictionary. As a result, the function returns a class instance of the class defined before.
  
- Add tests to "tests" and name the test file "test_[]_naming.py", where "[]" should be replaced by the abbreviation of the new naming convention.


Note
====

This project has been set up using PyScaffold 2.5.11. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.

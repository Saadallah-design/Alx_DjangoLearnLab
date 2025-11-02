# Update a created instance like the Book in bookshelf

Modify an attribute of the retrieved object and save the change.
Here we can use the following command

* ==> So if we used book1 = (title="1984", author="Goerge Orwell", publication_year="1945")
* and we want to change the title. We select the variable book1.title and change it
    <!-- like accessing it with dot notation  -->
    - book1.title = "Nineteen Eighty-Four"
    - book1.save() 
    <!-- then we save it. -->
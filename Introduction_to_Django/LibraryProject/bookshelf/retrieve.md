# Retrieving or printing the created book

<!-- See this example  -->
>>> book1 = Book.objects.create(title="The Grapes of Wrath", author="John Steinbeck", publication_year=1939)
>>> book1.save()
**Retrieve** Read (query) the created instance back from the database.	
>>> retrieved_book = Book.objects.get(pk=book1.pk)

## We can also retrieve these instances using python format

>>> # Assuming 'book1' still holds the book instance
>>> print(f"Title: {rbook1.title}")
Title: Animal Farm
>>> print(f"Author: {book.author1}")
Author: George Orwell
>>> print(f"Year: {book1.publication_year}")
Year: 1945
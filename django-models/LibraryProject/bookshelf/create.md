# Creating a new Book instance using Django shell and save it to database

## First thing before accessing the shell
1. Start the bookshelf using:
    - python3 manage.py startapp bookshelf
    - add this newly app inside the settings.py (found inside the bookshelf)
    - python3 manage.py makemigrations // Output: Migrations for 'bookshelf':
                                        bookshelf/migrations/0001_initial.py
                                        + Create model Book
    - python3 manage.py migrate
    """ Output
        Operations to perform:
        Apply all migrations: admin, auth, bookshelf, contenttypes, sessions
        Running migrations:
        Applying contenttypes.0001_initial... OK
    """

## Accessing the Django Shell (Interactive Console)
1. python3 manage.py shell
when shell is access you would see: 
>>> 
these prompts you for commands.
<!-- Now we need to import the instance Book from our app bookshelf -->
<!-- This step is IMPORTANT -->
2. from bookshelf.models import Book

### Command to create a book is
- >>> book1 = Book.objects.create(title="Animal Farm", author="Goerge Orwell", publication_year="1945")
<!-- now we need to save our created book1 -->
- >>> book1.save()

<!-- to see / retrieve our created book -->
>>> print(book1.title)
>>> Book.objects.all()


<!-- For retrieving a readable output when trying to view all attributes you need to included the __str__ method in bookshelf/models.py, the output will be readable. If not, it will just show Book object (1)) -->
>>> print(f"Book Details: Title: {retrieved_book.title} | Author: {retrieved_book.author} | Year: {retrieved_book.publication_year}")
Book Details: Title: 1984 | Author: George Orwell | Year: 1949

>>> exit()
now exiting InteractiveConsole...
## Casino Application

## Application URL's
1. / - For home page
2. start/ - Start with the application by filling details
3. roll/ - Rolling blocks and get the results
4. stop/ - For cash out

## Steps for Application set up

# Create python 3.10 virtual environment
```
python -m venv <environment_name>
```

# Activate virtual environment
```
<environment_name>\Scripts\activate (Windows)
source <environment_name>/Scripts/activate (Ubuntu)
```

# Install dependencies from requirements.txt file
```
pip install -r requirements.txt
```

# Run Makemigrations
```
python manage.py makemigrations
```

# Apply migrations
``` 
python manage.py migrate
```

# Run Django server
```
python manage.py runserver
```
1. Clone project on GitHub: **[publik rep. on GiTHub](https://github.com/FireSwami/Park)**
2. Install virtual environment in your sources root directory:

    >#### python -m venv venv

3. Activate virtual environment in your sources root directory:<br>
   on Windows:

    >#### venv\scripts\activate
    
    on macOS & Ubuntu:

    >#### source venv/bin/activate

4. Install libs in your sources root directory:

    >#### pip install -r requirements.txt

5. Create DB:

    >#### python manage.py migrate

6. Load fixtures into DB: 

    >#### python manage.py loaddata db.json
   
   - *if you need create dump:* 
    >###### *python manage.py dumpdata cars.driver cars.vehicle --indent 2 > db.json*

7. Creat superuser if you need: 

    >#### python manage.py createsuperuser

8. Start server (you mast have password keies ***.env*** file 
   in sources root directory ): 

    >#### python manage.py runserver

9. Go to **[localhost](http://127.0.0.1:8000/swagger/)** 
    (for default) and get info from swagger
     - *Also you can use direct links from task (more in ***README)***.*

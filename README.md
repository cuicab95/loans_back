# Gestión de préstamos

#### Configurar ambiente
- ```docker-compose up --build```

#### Crear usuario
- ```docker-compose run web python manage.py createsuperuser```

#### Correr los tests
- ```docker-compose run web python manage.py test```

#### Documentación api
- ```http://localhost:8000/api/doc/```

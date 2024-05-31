# TP Guerra Suave


### Pasos necesarios para la ejecución del trabajo práctico

0. Prerequisitos
```sh
Python
Docker
```

1. Instalar las dependencias
```sh
./init.sh
```

2. Crear la base de datos
```sh 
cd db
docker-compose up --build -d
```

3. Ejecutar backend y frontend
```sh
# Desde el principal directorio del proyecto

# En una terminal
cd backend
flask run

# En otra terminal
cd frontend
flask run
```

### Testeo de APIs
https://www.postman.com/julengaumard/workspace/guerra-suave-tp/overview
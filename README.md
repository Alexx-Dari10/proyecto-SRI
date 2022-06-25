# proyecto-SRI
implementacion de un sistema de recuperacion de la informacion

# Creacion del ejecutable (Carpeta exe)

-Lo primero que debemos hacer es instalar pyinstaller con

	pip3 install pyinstaller

-Para crear el ejecutable hacemos lo siguiente:

Linux: 
	
	pyinstaller -F -i ./1.ico --add-data "templates:templates" --add-data "static:static" main.py
	
Windows: 

	pyinstaller -F -i ./1.ico --add-data "templates;templates" --add-data "static;static" main.py

-Luego debemos modificar el archivo main.spec:

Agregamos lo siguiente para poder trabajar con sklearn:

	from PyInstaller.utils.hooks import collect_data_files, eval_statement, collect_submodules

Luego en

     a = Analysis(...
          hiddenimports = collect_submodules('sklearn'),
                  ...
                  )
establecer la propiedad *hiddenimports* como se indicó anteriormente
	
	
Ejecutamos en la consola 
	
	pyinstaller main.spec

-Una vez hecho esto tenemos en la carpeta "dist" el ejecutable. Este ejecutable siempre debe estar en la misma carpeta del "main.py" para que funcione. (estar en la raíz)

Nota: En Windows para cerrar la aplicacion y que no se quede corriendo en el puerto debemos salir presionando Ctrl+c. En Linux escribiendo en consola 

	sudo kill $(sudo lsof -t -i:3000)

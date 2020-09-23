Asistente inteligente.

pasos para Ubuntu:
# 1. Instalación de librerías y dependencias
> sudo apt-get install libpulse-dev
> sudo apt-get install libasound2-dev
> sudo apt install portaudio19-dev
> sudo apt install swig
> pip3 install -r requirements.txt
> pulseaudio --start
# 2. Descarga de modelo e instalación (para el uso de sphinx)
> Descargar el modelo de idioma para Sphinx, para este caso "Español". URL de modelos: https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/
> Descomprimir el .zip descargado (modelo) y copiar lo que este dentro de la carpeta "models" en el "get_model_path"
> Para sacar el directorio del modelo ejecutar: 
- from pocketsphinx import get_model_path
- model_path = get_model_path()
> Renombrar la carpeta "581HCDCONT10000SPA" por "acoustic-model"
> Renombrar "581HCDCONT10000SPA.dic" por "pronounciation-dictionary.dict"
> Renombrar "581HCDCONT10000SPA.lm.bin" por "language-model.lm.bin"
# 3. Ejecutar
> python3 main.py

pasos para Mac:
# 1. Instalación de librerías y dependencias
> Instalar homebrew: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
> brew install pulseaudio
> brew install portaudio
> brew install swig
> sudo apt install libespeak1
> sudo apt-get install mpg321
> Para solucionar el error "fatal error: 'al.h' file not found":
    1. git clone --recursive https://github.com/bambocher/pocketsphinx-python
    2. cd pocketsphinx-python
    3. Edit file pocketsphinx-python/deps/sphinxbase/src/libsphinxad/ad_openal.c
    4. Change
    #include <al.h>
    #include <alc.h>
    to
    #include <OpenAL/al.h>
    #include <OpenAL/alc.h>
    5. python setup.py install
# Para AppKit
> brew install pkg-config
> brew install cairo
> brew install gobject-introspection
> pip3 install -r requirements.txt
# 2. Descarga de modelo e instalación
> Descargar el modelo de idioma para Sphinx, para este caso "Español". URL de modelos: https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/
> Descomprimir el .zip descargado (modelo) y copiar lo que este dentro de la carpeta "models" 
> Consultar el "get_model_path"
> Para sacar el directorio del modelo ejecutar: 
- from pocketsphinx import get_model_path
- model_path = get_model_path()
> crear el folder "es" en el model path y pegar el contenido
> Renombrar la carpeta "581HCDCONT10000SPA" por "acoustic-model"
> Renombrar "581HCDCONT10000SPA.dic" por "pronounciation-dictionary.dict"
> Renombrar "581HCDCONT10000SPA.lm.bin" por "language-model.lm.bin"
# 3. Ejecutar
> python3 voicex.py
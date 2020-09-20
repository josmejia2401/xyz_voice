Asistente inteligente.

pasos:
# 1. Instalación de librerías y dependencias
> sudo apt-get install libpulse-dev
> sudo apt-get install libasound2-dev
> sudo apt install portaudio19-dev
> sudo apt install swig
> pip3 install -r requirements.txt
> pulseaudio --start
# 2. Descarga de modelo e instalación
> Descargar el modelo de idioma para Sphinx, para este caso "Español". URL de modelos: https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/
> Descomprimir el .zip descargado (modelo) y copiar lo que este dentro de la carpeta "models" en el "get_model_path"
> Para sacar el directorio del modelo ejecutar: 
- from pocketsphinx import get_model_path
- model_path = get_model_path()
> Renombrar la carpeta "581HCDCONT10000SPA" por "acoustic-model"
> Renombrar "581HCDCONT10000SPA.dic" por "pronounciation-dictionary.dict"
> Renombrar "581HCDCONT10000SPA.lm.bin" por "language-model.lm.bin"
# 3. Ejecutar
> python3 voicex.py



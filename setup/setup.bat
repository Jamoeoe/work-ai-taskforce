cd %~dp0
cd ..

REM create .env file
IF NOT EXIST ".env" (
    echo GENAI_KEY=your_api_key > ".env"
)

REM install python
winget install -e --id Python.Python.3.12

REM create venv, and install required packages
py -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org
.venv\Scripts\python.exe -m pip install dotenv --trusted-host pypi.org --trusted-host files.pythonhosted.org
.venv\Scripts\python.exe -m pip install matplotlib --trusted-host pypi.org --trusted-host files.pythonhosted.org 
.venv\Scripts\python.exe -m pip install pandas --trusted-host pypi.org --trusted-host files.pythonhosted.org
.venv\Scripts\python.exe -m pip install openpyxl --trusted-host pypi.org --trusted-host files.pythonhosted.org  
.venv\Scripts\python.exe -m pip install openai --trusted-host pypi.org --trusted-host files.pythonhosted.org  

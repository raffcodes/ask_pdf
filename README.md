To run it on you machine, you need following steps:
1. Create an OpenAI API Key and save it to your environment variable as OPENAI_KEY = "<you key>"
2. Create an environment variable with your choosen login credentials, ASK_PDF_CREDENTIALS="<username>:<password>".
   On windows, open cmd as an admin and type: setx ASK_PDF_CREDENTIALS "<username>:<password>".
   Restart the machine and check on cmd with echo %ASK_PDF_CREDENTIALS%
3. Create a new virtual environment for this project and activate it
4. pip install -r requirements.txt
5. To run the app: streamlit run app.py (not: python app.py)
 

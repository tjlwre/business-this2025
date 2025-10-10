@echo off
echo Setting up BusinessThis Streamlit App...
echo.

REM Try to use Python 3.13 with proper dependency management
py -3.13 -m pip install --upgrade pip
py -3.13 -m pip install streamlit==1.45.1 pandas==2.2.2

echo.
echo Starting BusinessThis app...
echo Open your browser to: http://localhost:8501
echo.

py -3.13 -m streamlit run app.py --server.headless=true --server.address=0.0.0.0 --server.port=8501 --server.enableCORS=false --server.enableXsrfProtection=false

pause

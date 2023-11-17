# FastAPI

## Main Steps
1. **Create an environment:**

    **Windows:**
    ```
    python -m venv env
    ```
    **MacOS:**
    ```
    python3 -m venv env
    ```

2. **Environment activate:**

    **Windows:**
    ```
    .\env\Scripts\activate
    ```
    **MacOS:**
    ```
    source env/bin/activate
    ```

3. **Install FastAPI:**

    **Windows:**
    ```
    pip install fastapi[all]
    ```
    **MacOS:**
    ```
    pip3 install fastapi
    ```

    **Install Requirements:**
    ```
    pip install -r requirements.txt
    ```

3. **Install Uvicron:**

    **Windows:**
    ```
    pip install uvicorn[standar]
    ```
    **MacOS:**
    ```
    pip3 install uvicorn
    ```

6. **Run Server:**

    ```
    uvicorn app.main:app --reload
    ```
    or
    ```
    uvicorn <folder>.main:app --reload
    ```

7. **Deactive Environment:**

    ```
    deactivate
    ```

8. **Install Pycopg2:**

    ```
    pip install psycopg2-binary
    ```


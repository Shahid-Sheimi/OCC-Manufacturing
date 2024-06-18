# Manufacturing Backend

This is a backend server for manufacturing processes using Django. It includes a REST API with endpoints for authentication, process occurrence, and payments.

## Installation

### Prerequisites


### Setting up the Environment
Clone the repository 

```git clone https://github.com/Shahid-Sheimi/OCC-Manufacturing.git```

Navigate to the project directory

``` cd manufacturing_backend ```

1. Open your favorite shell (that has conda in its path), and run the following three commands:

```conda create -n pyocct python=3.8```

2. Activate the environment
```conda activate pyocct```

3. Install pythonocc-core
``` conda install -c conda-forge pythonocc-core ```

4. Check pythonocc-core 
```python -c "import OCC; print(OCC.VERSION)" ```

5. Install Dependpencies (requirements)

``` pip install -r requirements.txt```

6. Run migrations and migrate

``` python manage.py makemigrations ```

``` python manage.py migrate ```

7.  Start the development server

```  python manage.py runserver  ```

You can now access the API documentation by visiting

``` http://127.0.0.1:8000/swagger/ ```


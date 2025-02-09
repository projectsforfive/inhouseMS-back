## Installation
Step-by-step instructions on how to install your project.

### Clone project from repository
```bash
git clone https://github.com/projectsforfive/inhouseMS-back.git
```

### Create Virtual Environment for Django Project
```bash
python -m venv myenv
```

### Entering to virtual environment
```bash
myenv\Scripts\activate
```

### Install required python modules
```bash
pip install django firebase-admin django-rest-framework django-cors-headers python-decouple
```

### Launch project
```bash
cd server
python manage.py runserver
```
## Important - Authorization:
All views should be wrapped with firebase_auth_required wrapper

How to do it?

### 1. You can create new app related to your section

```bash
python manage.py startapp [app-name (e.g: payment. etc )]
```

### 2. After define views, and it should be wrapped with firebase_auth_required wrapper.
```python
# views.py

...
from firebase_auth.auth_middleware import firebase_auth_required
...

class MyView(APIView):
    @firebase_auth_required   # It is crucial for authorization of all request.
    def get(self):
        ...
        return Response({ ... })
```

## payment routes

### create new payment
```text
post localhost:8000/payment/paid/ 
```

### get all payments
```text
get localhost:8000/payment/paid-all/<uid>/
```

### get one payment
```text
get localhost:8000/payment/paid/<uid>/<id>/
```

### update one payment
```text
put localhost:8000/payment/paid/<uid>/<id>/
```

### delete one payment
```text
delete localhost:8000/payment/paid/<uid>/<id>/
```
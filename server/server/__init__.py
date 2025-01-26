import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("C:/Users/master-0823/Documents/work/task/server/server/inhousems-aee24-firebase-adminsdk-fbsvc-68aee5da0f.json")
firebase_admin.initialize_app(cred)
# DiabetesPredict

## Enviroment

- Ubuntu20.04
- Docker
- Python3
- Firebase
- Windows10

## Introduction

We use Python PyQt5 library to to build a GUI plaform to predict users diabetes status from a pretrained multi-class classification model. This model is trainned by using Keras library with the [diatabetes data](https://www.kaggle.com/datasets/kumargh/pimaindiansdiabetescsv). Users need to register and login in the GUI platform. The authentication is provided by firebase authentication system.  Users input their the diabetes status, and they are stored in firebase realdatabase. Users could export their diabetes history into csv. The firebase administration account could also edit their users information. Finally, we use pyinstaller to make the GUI library to be executed in windows environment.

## Installation

- Download repository to **your-path** 

### Data Setting

- Sign in Kaggle and save [pima-indians-diabetes.csv](https://www.kaggle.com/datasets/kumargh/pimaindiansdiabetescsv) to the folder **your-path**/**repository**/docker/GUI

### Firebase Setting

- Create a json file to path **your-path**/**repository**/docker/GUI/config.json

- Signin firebase and create project **your-project**

- create admin account **"admin@gmail.com"** in Authentication page (you may also want to create other user accounts)

- Go to realtime database rule page and set the rule

```
{
    "rules": 
    {
        "users": 
        {
            ".read": "auth.uid == '<admin-account-user-id>'",
            ".write": "auth.uid == '<admin-account-user-id>'",
                "$uid": 
                {
                // Allow only authenticated content owners access to their data
                ".read": "auth.uid == $uid",
                ".write": "auth.uid == $uid"
                }
        },
    }
}
```

- Go to project setting, create an application. Copy and paste the firebaseConfig from your application config to your config.json

- config.json
```
{
    "apiKey": "<your-apiKey>"
    "authDomain": "<your-authDomain>"
    "databaseURL": "<your-databaseURL>"
    ...
}
```

### Run locally in Linux

- In **Linux OS**

- Go to docker directory
```
$ cd <your-path>/<repository>/docker
```

- Build docker image and container
```
$ docker build -t diabetes_predict_image .
```

```
$ docker run -it -d diabetes_predict_container
```

- Enter container and run GUI in virtualenv

```
$ docker exec -it diabetes_predict_container bash
```

```
$ source ./GUI/venv/bin/activate
```

```
$ python3 ./GUI/main.py
```

- Quit program and container
```
$ deactivate
```

```
exit
```

### Exports to exe in Windows

- In **Windows OS**

- Download repository to **your-path**

- Go to docker directory

```
cd <your-path>/<repository>/docker
```

- Install virtualenv

```
pip3 install virtualenv
```

- Create virtual environment and enter the virtualenvironment

```
virtualenv venv
```

```
.\venv\Scripts\activate.bat
```

- Install dependencies and export EXE

```
pyinstaller main.spec
```

- Move main.exe to GUI directory

```
mv dist/main.exe GUI/main.exe
```

- Double clik GUI/main.exe for run the program

## Program tutorial

- login up and sign up platform

- create more auth user in firebase

- login in with admin account "admin@gmail.com" 

- admin could view, add, edit, save any user info

- input the data info in add or edit page to predict diabetes. Please reference pima-indians-diabetes.csv

- users diabetes info is saved in GUI directory as **output.csv**

## Reference

- [Python - PyQt5](http://13.231.129.69/2021/02/03/python-qt-designer-%E5%AE%89%E8%A3%9D%E7%AF%87/)
- [Qt Designer](https://clay-atlas.com/blog/2020/01/04/linux-chinese-tutorial-qt-designer-python-gui/)
- [Code First with Hala](https://www.youtube.com/c/CodeFirstio)
- [pima-indians-diabetes.csv](https://www.kaggle.com/datasets/kumargh/pimaindiansdiabetescsv)
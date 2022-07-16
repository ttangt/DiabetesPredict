# DiabetesPredict

## Enviroment

- Linux
- Docker
- Python3
- Firebase
- Colab

## Introduction

We use Python PyQt5 library to to build a GUI plaform to predict users diabetes status from a pretrained multi-class classification model. This model is trainned by using Keras library with the [diatabetes data](). Users need to register and login in the GUI platform. The authentication is provided by firebase authentication system.  Users input their the diabetes status, and they are stored in firebase realdatabase. Users could export their diabetes history into csv. The firebase administration account could also edit their users information. Finally, we use pyinstaller to make the GUI library to be executed in windows environment.

## Tutorial: Execute the GUI platform with Firebase in windows environment




## Reference

- (Python - PyQt5)[http://13.231.129.69/2021/02/03/python-qt-designer-%E5%AE%89%E8%A3%9D%E7%AF%87/]
- (Qt Designer)[https://clay-atlas.com/blog/2020/01/04/linux-chinese-tutorial-qt-designer-python-gui/]
- (Code First with Hala)[https://www.youtube.com/c/CodeFirstio]
- (Diabetes Data)[https://www.kaggle.com/datasets/kumargh/pimaindiansdiabetescsv]
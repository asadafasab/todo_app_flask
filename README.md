# ToDo Web App
This is dummy to do web app written in flask 

![ss](https://raw.githubusercontent.com/6malphas/todo_app_flask/master/ss.png "Screnshot")

## Setup
```bash
pip install --user -r requirements.txt
```

### Docker

```bash
eval $(minikube docker-env) # minikube - k8s
docker build -t todoflask:latest .
docker run -p 8080:8080 -t -i todoflask
```

### K8s
```bash
kubectl
```

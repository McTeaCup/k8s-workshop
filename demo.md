# Demo / Lab

- [Förberedelser](#förberedelser)
- [CLI DEMO](#kubernetes-cli-demo)
- [YAML DEMO](#kubernetes-yaml-demo)
  
## Förberedelser
Innan vi börjar med demon måste du genomföra föreberedelserna från [README](./README.md).

### Terminal 1 (Display terminal)

I denna terminal, kör följande kommando: 
```bash
$ watch kubectl get all -n default -o wide
```
![image](https://github.com/user-attachments/assets/78ab7ffd-1726-4865-bf8d-5d2b915e0cab)
> [!NOTE]
> Detta kommando visar alla resurser som ligger uppe namespace `default`, vilket är där vi kommer att skapa våra resurser i klustret. Efter att du har kört detta kommando, låt detta fönster vara lättilljängligt eller på en separat skärm. Detta kommer ge dig en överblik av vad som är live och nuvarande status på alla resurser.

### Terminal 2 (Kommando terminal)
Dehär är terminalen som du kommer att skriva alla kommandon i.

---

## KUBERNETES CLI DEMO
Nu är det dags att skapa ett kluster med vår Docker kubernetes instans.

### Skapa deployment, pods och replikasett
Vi börjar med att skapa en deployment resurs som vi kallar demo-pods. Detta kommer skapa:
```
kubectl create deployment demo-pod --image=feighty7/nginx-podname --replicas=3
```
![image](https://github.com/user-attachments/assets/3d52ba0f-4f9d-418c-b4de-e938749b1e9e)
- 3 Pods (`pod/demo-pod-<template-hash>-<podID>`)
- 1 Deployment (`deployment.apps/demo-pod`)
- 1 Replica set (`replicaset.apps/demo-pod-<template-hash>`)

### Skapa service
Nu har vi skapat allt vi behöver för att få vår applikation att fungera i klustret, problemet nu är att ingen kan komma åt vår app. Därför behöver vi skapa en service som hanterar portarna mellan applikationen i kontainern och en service load balancer.
```
kubectl expose deployment demo-pod --port=80 --target-port=5000 --type=LoadBalancer
```
![image](https://github.com/user-attachments/assets/7e0e3803-477c-4559-8a3b-7e72ed4a4c4d)
> [!NOTE]
> Som du kan se här så har vi en ny service som heter `service/demo-pod`.  Just denna image använder sig av Flask som använder sig av den intärna porten `5000` och vi vill lägga över den till port `80` på localhost. Det är detta som `--port=80` och `--target-port=5000` hanterar.

Detta gör det möjligt att nå applikationen från vår webläsare på [localhost:80](http://localhost:80).

### Patching
Nu har vi fått upp vår service och applikation som vi har deployat i vår kubernetes kluster, men just nu så kan vi inte se vilken pod vi läser från just nu. Detta är för att vår image behöver komma åt en environment variabel som vi glömde lägga in när vi byggde våra pods.

Detta är ett perfekt exempel där vi kan använda oss av `kubectl patch`
```
kubectl patch deployment demo-pod --type='json' -p='[
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/env",
    "value": [
      {
        "name": "POD_NAME",
        "valueFrom": {
          "fieldRef": {
            "fieldPath": "metadata.name"
          }
        }
      }
    ]
  }
]'
```
> [!NOTE]
> Detta kommer att stänga ner dina pods du har haft tidigare och starta upp nya som ersätter dem med den uppdaterade veritionen.

Om du nu går in på [localhost:80](http://localhost:80) igen och uppdaterar sidan så kommer du se att den refererar till en av de tre pods som ligger i ditt kluster. Om du fortsätter refresh:a hemsidan så kommer du se att namnet byts ut till en annan pod som du har i dit kluster.
![image](https://github.com/user-attachments/assets/148a0421-7edb-4e6b-925a-e635a26db308)![image](https://github.com/user-attachments/assets/46ea1fe6-2b51-4061-b84b-9285b856e179)

Grattis! Du har nu skapat ett kubernetes kluster för en applikation som utnyttjar loadbalancing!
> [!WARNING]
> Detta är ett labb exempel, detta simulerar hur det skulle se ut. Docker's distro av Kubernetes är inte gjort för att drivas i produktion utan för labb/demo.

### Ta bort kluster
När du är klar med demon så är det en bra idé att ta bort klustret eftersom podar/service/depoyment använder din dators resurser för att driva detta och kan ta upp mycket prestanta om det inte rensas.

Kör dessa kommandon för att ta bort ditt kluster:
```
kubectl delete deployment demo-pod
kubectl delete service demo-pod
```
Detta kan ta en liten stund.


### **1️⃣ Skapa Deployment**  
```sh
kubectl create deployment k8s-workshop --image=feighty7/k8s-workshop --replicas=3
```

### **2️⃣ Injicera Pod-namn**  
```sh
kubectl patch deployment k8s-workshop --type='json' -p='[
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

### **3️⃣ Exponera Deployment**  
```sh
kubectl expose deployment k8s-workshop --type=LoadBalancer --port=80 --target-port=5000
```

### **4️⃣ Öppna ett nytt terminalfönster och kör:**  
```sh
watch -n 1 kubectl get all
```
Detta uppdaterar alla resurser i realtid och visar förändringar när nya pods skapas eller tas bort.

### **5️⃣ Testa tjänsten**  
#### **Kontrollera tjänstens detaljer**  
```sh
https://localhost:80
```

---

## **🔵 Del 2: Deployering med YAML**  
### **1️⃣ Skapa Deployment & Service YAML**  
📌 **Spara som `k8s-workshop.yaml`**  
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: k8s-workshop
spec:
  replicas: 3
  selector:
    matchLabels:
      app: k8s-workshop
  template:
    metadata:
      labels:
        app: k8s-workshop
    spec:
      containers:
      - name: k8s-workshop
        image: feighty7/k8s-workshop
        ports:
        - containerPort: 5000
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name

---

apiVersion: v1
kind: Service
metadata:
  name: k8s-workshop
spec:
  selector:
    app: k8s-workshop
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: LoadBalancer
```

---

### **2️⃣ Applicera Deployment & Service**  
```sh
kubectl apply -f k8s-workshop.yaml
```

### **3️⃣ Verifiera Deployment**  
```sh
https://localhost:80
```

---

## **🔄 Uppdatering av Image**  
Om du pushar en ny bild, **uppdatera Kubernetes med:**  
```sh
kubectl rollout restart deployment k8s-workshop
```
Eller uppdatera bilden manuellt:  
```sh
kubectl set image deployment/k8s-workshop k8s-workshop=feighty7/k8s-workshop:v2
```

---

## **🔼 Skala upp eller ner Deployment**  
Om du vill **ändra antal pods** kan du skala upp eller ner:

### **Öka antalet pods**  
```sh
kubectl scale deployment k8s-workshop --replicas=5
```

### **Minska antalet pods**  
```sh
kubectl scale deployment k8s-workshop --replicas=2
```

---

## **🗑 Radera Deployment & Service**  
När du är klar och vill ta bort allt:

### **Ta bort deployment**  
```sh
kubectl delete deployment k8s-workshop
```

### **Ta bort service**  
```sh
kubectl delete svc k8s-workshop
```

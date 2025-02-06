# Kubernetes workshop 

## Förbredelser 
- [WSL](#wsl)
- [Docker Desktop](#docker-desktop)
- [Starta Kubernetes kluster](#starta-kubernetes-kluster)
- [Verifiera](#verifiera)
- [Trubbleshooting](#trubbleshooting)

### WSL 
Öppna PowerShell som Admin och kör: 
`wsl --install` 

Skapa användarnamn och lösenord.  

---

### Docker Desktop 
Docker Desktop är programmet som kommer hantera vår kubernetes miljö på en lokal nivå. Detta kommer installera alla nödvändiga verktyg och system automatiskt och tillåta oss att labba med kubernetes. 
Börja med att ladda ner Docker desktop och följ instruktioerna enligt [hemsidan](https://docs.docker.com/desktop/setup/install/windows-install/).

Efter nedladdning och öppnat applikationen bör du se detta: 
![image](https://github.com/user-attachments/assets/97568590-d928-4be5-89b8-a2da9b9b1275) 

Ni kan behöva aktivera WSL2 -plugin: 

![image](https://github.com/user-attachments/assets/51ec4182-17b6-4369-9157-f6353fe235f1)

---

### Starta Kubernetes klustret
Efter att WSL är installerat och konfigurerat kan du starta ditt kubernetes kluster genom att gå till `Settings > Kuberentes` och bocka i `Show system containers (advanced)` och `Enable Kubernetes`.

För att starta kubernetes klustret tryck på `Apply & restart`. 
Det kan ta någon minut för docker att starta alla processer, så låt den stå ett tag. I vänstra botten hörnet kommer det stå `Kubernetes running` när allt är uppe. 

*Såhär borde din docker Desktop se ut i container fliken*
![image](https://github.com/user-attachments/assets/e30f53b2-1187-4030-9acf-315691561e88)

Öppna WSL terminalen och kör `snap install kubectl --classic`. Detta installerar ett pluggin som tillåter oss att prata med Kubernetes klustret senare. Efter att kubectl har installerats vill vi koppla det till docker desktop instansen. I WSL-terminalen kör dessa kommandon: 
```bash
export KUBECONFIG=$HOME/.kube/config 

mkdir -p $HOME/.kube 

cp /mnt/c/Users/<your-user>/.kube/config $HOME/.kube/config 

```
> [!IMPORTANT]
> Kom ihåg att `<your-name>` ska ersättas av användaren som din dator är skriven på.

---

### Verifiera
För att verifiera att allt är uppe och fungerar som det ska så kör detta kommando i WSL-terminalen:
```
kubectl get pods --all-namespaces
``` 

Om du får upp något som liknar detta så fungerar allt som det ska. 
![image](https://github.com/user-attachments/assets/f38c4abe-0643-4a40-b6fe-58819800e9ca)

---

### Trubbleshooting 

#### Jag kan inte få upp kubernetes (Kubernetes failed to start) 
Ibland kan docker försöka använda fel image för att starta klustret. För att lösa detta: 
1. Stäng av Docker 
2. Kör dessa kommandon i Powershell/WSL 
  `docker pull k8s.gcr.io/coredns/coredns:v1.9.3 `
  `docker tag k8s.gcr.io/coredns/coredns:v1.9.3 k8s.gcr.io/coredns:v1.9.3` 

Detta kommer hämta rätt images för kubernetes. Starta om Docker Desktop och försök starta kubernetes igen. 
Om detta inte hjälper starta om datorn och försök igen. 

 

 

## Example Ingress 
These are the artifactes necessary to evaluate the installation of NGINX.

1. kubectl apply -f nginx-ws-deployment.yaml
2. kubectl apply -f nginx-ws-service.yaml
3. kubectl apply -f nginx-ws-ingress.yaml

The hostname *nginx.local* will need to be added to the '/etc/hosts' file. For WSL2, one can edit C:\Windows\System32\drivers\etc\host using a powershell with administrative privledges.

### Reference
OpenAI. 2023. "ChatGPT Conversation on [Example Ingree/Craft an Example Ingress setup with ]." OpenAI.
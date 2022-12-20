ansible-playbook:
	ansible-playbook -i src/ansible/inventory src/ansible/playbook.yaml

image:
	podman build -t registry.mb.lab/squirrel-serve:latest -f src/Dockerfile .

run:
	podman run -rm -it -p 8081:8080 registry.mb.lab/squirrel-serve:latest

publish:
	podman push registry.mb.lab/squirrel-serve:latest --tls-verify=false

ansible-playbook:
	ansible-playbook -i src/ansible/inventory src/ansible/playbook.yaml

image:
	podman build -t squirrel-serve:latest -f src/Dockerfile .

run:
	podman run -it -p 8081:8080 squirrel-serve:latest

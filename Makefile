ansible-playbook:
	ansible-playbook -i src/ansible/inventory src/ansible/playbook.yaml

docker:
	docker build -t squirrel-serve:latest -f src/Dockerfile .

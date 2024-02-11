ansible-playbook:
	ansible-playbook -i src/ansible/inventory src/ansible/playbook.yaml

image:
	docker build -t registry.mb.lab/tflite-serve:latest -f src/Dockerfile .

run:
	docker run -it -p 8081:8080 registry.mb.lab/tflite-serve:latest

publish:
	docker push registry.mb.lab/tflite-serve:latest

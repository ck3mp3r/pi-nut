ansible-playbook:
	ansible-playbook -i src/ansible/inventory src/ansible/playbook.yaml

image:
	podman build -t registry.mb.lab/tflite-serve:latest -f src/Dockerfile .

run:
	podman run -it -p 8081:8080 registry.mb.lab/tflite-serve:latest

publish:
	podman push registry.mb.lab/tflite-serve:latest --tls-verify=false

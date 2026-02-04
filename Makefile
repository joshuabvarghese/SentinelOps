# --- Configuration ---
IMAGE_NAME = techops-monitoring
VERSION = latest
NAMESPACE = techops

# --- Local Development ---
.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: run-local
run-local:
	python3 server.py & python3 monitor.py

# --- Docker Commands ---
.PHONY: docker-build
docker-build:
	docker build -t $(IMAGE_NAME):$(VERSION) .

.PHONY: docker-run
docker-run:
	docker run -p 8080:8080 $(IMAGE_NAME):$(VERSION)

# --- Kubernetes Commands ---
.PHONY: k8s-deploy
k8s-deploy:
	@echo "🚀 Creating Namespace and Deploying Resources..."
	kubectl apply -f kubernetes.yaml
	@echo "⏳ Waiting for pods to stabilize..."
	kubectl rollout status deployment/techops-monitoring -n $(NAMESPACE)

.PHONY: dashboard
dashboard:
	@echo "🔗 Dashboard: http://localhost:8080"
	kubectl port-forward -n $(NAMESPACE) svc/monitoring-service 8080:80

.PHONY: k8s-logs
k8s-logs:
	kubectl logs -l app=monitoring -n $(NAMESPACE) -f

# --- Cleanup ---
.PHONY: clean
clean:
	@echo "🧹 Cleaning up Kubernetes resources..."
	kubectl delete -f kubernetes.yaml || true
	@echo "✨ Cleanup complete."

.PHONY: clean-docker
clean-docker:
	docker rmi $(IMAGE_NAME):$(VERSION)
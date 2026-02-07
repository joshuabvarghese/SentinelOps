# 🚀 SentinelLens: Cloud-Native Health Monitoring

[![SentinelLens CI/CD](https://github.com/joshuabvarghese/SentinelLens/actions/workflows/deploy.yml/badge.svg)](https://github.com/joshuabvarghese/SentinelLens/actions)
![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=flat&logo=kubernetes&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)

**SentinelLens** is a professional-grade observability suite designed to monitor system health in containerized environments. It features an asynchronous monitoring engine, a Flask API, and a real-time web dashboard, all orchestrated via Kubernetes.

---

## 🏗 System Architecture

The project demonstrates a full-stack DevOps lifecycle:

* **Asynchronous Monitoring**: `monitor.py` utilizes Python's `asyncio` to perform non-blocking system checks.
* **RESTful API**: `server.py` provides a Flask-based backend to serve metrics.
* **Containerization**: A multi-stage `Dockerfile` optimizes the image for production.
* **Orchestration**: `kubernetes.yaml` defines a self-healing infrastructure using Deployments, Services, and ConfigMaps.
* **Automation**: A robust CI/CD pipeline in GitHub Actions handles linting, building, and validation.

---

## 🛠 Tech Stack

| Component | Technology |
|:---|:---|
| **Language** | Python 3.11 (Asyncio, Flask) |
| **Containerization** | Docker |
| **Orchestration** | Kubernetes |
| **CI/CD** | GitHub Actions |
| **Infrastructure** | YAML (K8s Manifests), Makefile |

---

## 🚀 Getting Started

### 1. Prerequisites

* [Docker Desktop](https://www.docker.com/products/docker-desktop/) or [Minikube](https://minikube.sigs.k8s.io/docs/start/)
* `kubectl` CLI
* Python 3.11+

### 2. Automated Deployment

This project uses a `Makefile` to simplify complex operations. To deploy the entire stack to your Kubernetes cluster:

```bash
# Clone the repository
git clone https://github.com/joshuabvarghese/SentinelLens.git
cd SentinelLens

# Deploy to Kubernetes
make k8s-deploy
```

### 3. Accessing the Dashboard

Once the pods are running, use the built-in shortcut to access the UI:

```bash
make dashboard
```

Then open your browser to:

```
http://localhost:8080
```

---

## 🤖 CI/CD Pipeline

The integrated GitHub Actions workflow ensures code quality and deployment stability:

* **Code Linting**: Uses flake8 to enforce PEP8 standards.
* **Container Audit**: Validates that the Dockerfile builds a functional image.
* **Manifest Validation**: Uses static analysis to verify kubernetes.yaml structure without requiring a live cluster.

---

## ⚙️ Configuration

The system behavior can be modified without rebuilding the Docker image by editing the ConfigMap section in `kubernetes.yaml`:

```yaml
data:
  config.json: |
    {
      "check_interval": 30,
      "services": {
        "api": "http://api-service.default.svc.cluster.local/health"
      }
    }
```

---

## 🧹 Cleanup

To remove all resources and the dedicated techops namespace:

```bash
make clean
```
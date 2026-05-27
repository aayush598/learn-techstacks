# Chapter 02: Kubernetes Cluster Architecture

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [K3s/K8s Cluster Setup](sec-01-k3s-k8s-cluster-setup.md) | K3s installation for edge/lightweight, full K8s for production, node configuration, HA control plane |
| 02 | [Node Configuration & Management](sec-02-node-configuration-management.md) | Node pools, taints and tolerations, node affinity, spot instance handling, node auto-repair |
| 03 | [Namespace Strategy](sec-03-namespace-strategy.md) | Namespace per environment, per-team isolation, RBAC per namespace, resource quotas |
| 04 | [Resource Quotas & Limits](sec-04-resource-quotas-limits.md) | Namespace quotas, container resource requests/limits, LimitRange policies, priority classes |
| 05 | [Pod Auto-Scaling](sec-05-pod-auto-scaling.md) | HPA configuration, custom metrics scaling, VPA recommendations, cluster autoscaler |
| 06 | [Affinity & Scheduling Rules](sec-06-affinity-scheduling-rules.md) | Node affinity, pod affinity/anti-affinity, topology spread constraints, taints and tolerations |
| 07 | [Storage & Volume Management](sec-07-storage-volume-management.md) | Persistent volumes, storage classes, StatefulSet storage, CSI drivers, backup volumes |
| 08 | [Ingress & Service Mesh](sec-08-ingress-service-mesh.md) | Ingress controllers (Traefik/NGINX), TLS termination, service mesh (Linkerd/Istio), mTLS |

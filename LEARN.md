# 🧭 Lộ Trình Ôn Tập & Nâng Cao CNTT Toàn Diện

**Mục tiêu:** Củng cố và mở rộng kiến thức CNTT để đạt trình độ kỹ sư hệ thống / backend architect.  
**Ngôn ngữ chính:** Java → mở rộng Go, Rust  
**Thời lượng:** 2 tiếng/ngày · 6 tháng

---

## ✅ Mục lục
1. [Kiến thức nền tảng](#i-kiến-thức-nền-tảng)
2. [Mạng máy tính](#ii-mạng-máy-tính)
3. [Lập trình & Ngôn ngữ](#iii-lập-trình--ngôn-ngữ)
4. [Cơ sở dữ liệu](#iv-cơ-sở-dữ-liệu)
5. [Hạ tầng & DevOps](#v-hạ-tầng--devops)
6. [Bảo mật hệ thống](#vi-bảo-mật-hệ-thống)
7. [Trí tuệ nhân tạo](#vii-trí-tuệ-nhân-tạo)
8. [Thiết kế hệ thống lớn](#viii-thiết-kế-hệ-thống-lớn)

---

## I. 🧠 Kiến thức nền tảng
- [ ] Hiểu kiến trúc máy tính: CPU, RAM, cache, bus  
- [ ] Tìm hiểu process, thread, context switch  
- [ ] Hiểu memory management: stack, heap, paging, segmentation  
- [ ] Hiểu file system (inode, journaling, permissions)  
- [ ] Thành thạo bash & command line (Linux)

**Thực hành:**
- [ ] Viết bash script giám sát CPU/memory  
- [ ] Phân tích performance bằng `top`, `htop`, `vmstat`, `strace`  

---

## II. 🌐 Mạng máy tính
- [ ] Hiểu mô hình OSI và TCP/IP  
- [ ] Phân biệt TCP vs UDP  
- [ ] Tìm hiểu DNS, DHCP, HTTP/HTTPS, TLS handshake  
- [ ] Phân tích gói tin bằng Wireshark / tcpdump  
- [ ] Load balancing (L4 vs L7), reverse proxy, CDN  
- [ ] Hiểu NAT, subnet, routing, VPN  

**Thực hành:**
- [ ] Cấu hình nginx reverse proxy  
- [ ] Viết demo TCP server/client bằng Go hoặc Java  
- [ ] Kiểm tra kết nối mạng bằng traceroute, netstat  

---

## III. ⚙️ Lập trình & Ngôn ngữ

### Java
- [ ] Ôn OOP nâng cao (abstraction, polymorphism, composition)  
- [ ] Hiểu Java Memory Model & Garbage Collector  
- [ ] Concurrency: Executor, CompletableFuture, Locks  
- [ ] Spring Boot, Spring Cloud, Hibernate  
- [ ] Tối ưu hiệu năng, profiling, GC tuning  

### Go
- [ ] Hiểu goroutines, channels, context cancellation  
- [ ] Struct, interface, embedding  
- [ ] Error handling, testing, benchmarking  
- [ ] Viết service nhỏ (REST/gRPC) bằng Go  

### Rust
- [ ] Hiểu ownership, borrowing, lifetime  
- [ ] Trait, generic, async/await  
- [ ] Build CLI tool / Web service demo  

---

## IV. 💾 Cơ sở dữ liệu
- [ ] Ôn lại SQL, transaction, ACID  
- [ ] Hiểu index, query optimization, execution plan  
- [ ] Tìm hiểu MVCC, locking, isolation level  
- [ ] Làm quen với NoSQL: Redis, MongoDB, ElasticSearch  
- [ ] Hiểu replication, sharding, backup strategy  

**Thực hành:**
- [ ] Thiết kế schema cho hệ thống thực tế (E-commerce, blog, v.v.)  
- [ ] So sánh hiệu năng JOIN vs subquery  
- [ ] Viết script backup và restore dữ liệu  

---

## V. 🧱 Hạ tầng & DevOps
- [ ] Thành thạo Docker (image, container, volume, network)  
- [ ] Triển khai ứng dụng bằng Docker Compose  
- [ ] Học Kubernetes: pod, service, deployment, ingress, configmap  
- [ ] CI/CD (GitHub Actions, GitLab CI, Jenkins)  
- [ ] Quan sát hệ thống (Prometheus, Grafana, ELK)  
- [ ] IaC: Terraform, Ansible  
- [ ] Nắm cơ bản cloud (AWS/GCP/Azure – EC2, S3, RDS, IAM)  

**Thực hành:**
- [ ] Triển khai 1 app Spring Boot lên K8s  
- [ ] Cấu hình CI/CD pipeline tự động build & deploy  
- [ ] Theo dõi metrics hệ thống bằng Prometheus  

---

## VI. 🔒 Bảo mật hệ thống
- [ ] Hiểu OWASP Top 10  
- [ ] Authentication & Authorization (JWT, OAuth2)  
- [ ] HTTPS, TLS, HSTS, CSP, CORS  
- [ ] Secrets management (Vault, KMS)  
- [ ] Static & Dynamic scanning (SonarQube, Snyk)  
- [ ] Container & Dependency security  

**Thực hành:**
- [ ] Thực hiện pentest cơ bản với OWASP Juice Shop  
- [ ] Cấu hình HTTPS + TLS certificate cho app backend  
- [ ] Thiết lập kiểm tra bảo mật trong pipeline CI/CD  

---

## VII. 🧠 Trí tuệ nhân tạo
- [ ] Hiểu cơ bản Machine Learning: regression, classification, overfitting  
- [ ] Làm quen Python, NumPy, Pandas  
- [ ] Dùng scikit-learn để train model đơn giản  
- [ ] Hiểu TensorFlow / PyTorch cơ bản  
- [ ] Tích hợp mô hình AI vào backend (REST API hoặc gRPC)  

**Thực hành:**
- [ ] Viết API Flask/FastAPI để serve model  
- [ ] Tạo pipeline training → inference → logging  

---

## VIII. 🏗️ Thiết kế hệ thống lớn
- [ ] Hiểu Scalability, Reliability, Availability, Consistency  
- [ ] Nắm CAP theorem, ACID vs BASE  
- [ ] Kiến trúc: Monolith, Microservices, Event-driven, CQRS  
- [ ] Distributed system concepts: sharding, replication, consensus (Raft, Paxos)  
- [ ] Queue & Messaging: Kafka, RabbitMQ, NATS  
- [ ] Caching strategies: LRU, TTL, write-behind  

**Thực hành:**
- [ ] Thiết kế các hệ thống thực tế:  
  - [ ] URL Shortener  
  - [ ] Chat App real-time  
  - [ ] Recommendation Engine  
  - [ ] Payment System  
  - [ ] Logging Platform  

---

## 🏁 Theo dõi tiến độ
| Tháng | Mục tiêu | Trạng thái |
|-------|-----------|------------|
| Tháng 1 | OS, Network, Algorithm | ☐ |
| Tháng 2 | Database, Backend tối ưu | ☐ |
| Tháng 3 | DevOps, CI/CD, Docker | ☐ |
| Tháng 4 | Security, DevSecOps | ☐ |
| Tháng 5 | AI/ML cơ bản | ☐ |
| Tháng 6 | System Design nâng cao | ☐ |

---

**Ghi chú cá nhân:**  
> Cập nhật tiến độ mỗi tuần (ví dụ: `2025-11-07` – hoàn thành OS + Network cơ bản)  
> Ghi lại điểm mạnh, phần cần ôn thêm và link tài liệu bổ sung.

---

✨ *Hãy commit file này hàng tuần để theo dõi quá trình học tập và phát triển của bạn!*

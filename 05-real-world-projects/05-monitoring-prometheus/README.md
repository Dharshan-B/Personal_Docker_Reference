# 📊 Monitoring Stack (Prometheus + Grafana + Node-Exporter)

A metric collection and alerting system providing complete, real-time observability of your server nodes.

## ⚙️ How It Works
* **Node Exporter:** A Prometheus metrics collector that gathers CPU, memory, network, and disk metrics directly from the host operating system.
* **Prometheus:** A time-series database. Instead of waiting for logs, it **pulls (scrapes)** metric data from designated endpoints at configurable intervals.
* **Grafana:** Queries Prometheus TSDB and renders gorgeous visual monitoring panels.

## 🔄 Data Flow
1. **Node Exporter** gathers host CPU usage and exposes it as text under `/metrics`.
2. **Prometheus** makes an internal HTTP request to `http://node-exporter:9100/metrics` every 15 seconds.
3. Prometheus indexes these time-series statistics.
4. **Grafana** queries Prometheus internally on port `9090` and draws real-time CPU charts.

## 🛠️ Step-by-Step Commands

### 1. Start the Stack
Spin up the Prometheus server, exporter, and Grafana:
```bash
docker compose up -d
```

### 2. Verify Scrape Targets
* Open `http://localhost:9090/targets` in your browser.
* Ensure both `prometheus` and `node-exporter` targets display a status of **UP**.

### 3. Render Dashboards in Grafana
1. Visit `http://localhost:3000` (Default credentials: Admin / Admin, skip password change).
2. Go to **Connections** $ightarrow$ **Data Sources** $ightarrow$ **Add Data Source**.
3. Select **Prometheus** and enter URL: `http://prometheus:9090`. Save and test.
4. Import a pre-built host dashboard: Go to **Dashboards** $ightarrow$ **New** $ightarrow$ **Import**. Enter ID `1860` (Node Exporter Full Dashboard) and select your Prometheus data source.
5. Enjoy looking at your real-time CPU/RAM diagnostic panels!

### 4. Clean Up
```bash
docker compose down -v
```

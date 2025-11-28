# 🌐 Setup Domain Public Access (FREE) - Video AI Analyzer

Panduan lengkap untuk setup domain public access **GRATIS** yang compatible dengan semua dependency project ini.

## 🎯 Rekomendasi: Cloudflare Tunnel (⭐ BEST CHOICE)

**Kenapa Cloudflare Tunnel?**
- ✅ **100% GRATIS** - Tidak ada biaya sama sekali
- ✅ **HTTPS Otomatis** - SSL certificate gratis
- ✅ **Tidak Perlu Port Forwarding** - Tidak perlu akses router
- ✅ **Support WebSocket** - Penting untuk Streamlit (real-time updates)
- ✅ **Compatible 100%** - Tidak ada perubahan di aplikasi
- ✅ **Secure** - Traffic terenkripsi end-to-end
- ✅ **Reliable** - Infrastructure Cloudflare (global CDN)

**Cara Kerja:**
```
Internet → yourname.tunnel.cloudflare.com → Cloudflare Tunnel → Laptop Server:8501
```

---

## 📋 Prerequisites

1. **Domain Gratis** (opsional, bisa pakai subdomain Cloudflare)
   - Atau beli domain murah (~$1-2/tahun dari Cloudflare)
   - Atau pakai subdomain gratis dari Cloudflare

2. **Cloudflare Account** (gratis)
   - Daftar di: https://dash.cloudflare.com/sign-up

3. **Laptop Server** dengan:
   - Docker sudah running
   - Aplikasi sudah running di port 8501
   - Internet connection

---

## 🚀 Setup Cloudflare Tunnel (Step-by-Step)

### Step 1: Daftar Cloudflare Account

1. Buka https://dash.cloudflare.com/sign-up
2. Daftar dengan email (gratis)
3. Verifikasi email

### Step 2: Setup Domain (Opsi A: Pakai Domain Sendiri)

**Jika punya domain:**
1. Login ke Cloudflare Dashboard
2. Klik "Add a Site"
3. Masukkan domain Anda (misalnya: `example.com`)
4. Pilih Free plan
5. Cloudflare akan kasih nameservers
6. Update nameservers di registrar domain Anda
7. Tunggu propagasi DNS (5-30 menit)

**Jika tidak punya domain:**
- Bisa pakai subdomain gratis (lihat Step 2 Opsi B)
- Atau beli domain murah di Cloudflare (~$1-2/tahun)

### Step 2: Setup Domain (Opsi B: Pakai Subdomain Gratis)

Cloudflare Tunnel bisa pakai subdomain gratis:
- Format: `yourname.trycloudflare.com` (temporary, berubah setiap restart)
- Atau setup domain sendiri untuk permanent

### Step 3: Install Cloudflared di Laptop Server

**Mac:**
```bash
brew install cloudflare/cloudflare/cloudflared
```

**Linux (Ubuntu/Debian):**
```bash
# Download binary
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```

**Atau via Docker (Recommended untuk consistency):**
```bash
# Tidak perlu install, langsung pakai Docker image
```

### Step 4: Login Cloudflared

```bash
cloudflared tunnel login
```

Ini akan buka browser untuk authorize. Setelah authorize, token akan tersimpan.

### Step 5: Create Tunnel

```bash
# Create tunnel dengan nama
cloudflared tunnel create video-ai-analyzer

# Output akan kasih Tunnel ID (simpan ID ini!)
```

### Step 6: Setup DNS Route

**Jika pakai domain sendiri:**
```bash
# Route subdomain ke tunnel
cloudflared tunnel route dns video-ai-analyzer video-analyzer.yourdomain.com
```

**Jika pakai subdomain gratis:**
- Langsung ke step 7 (akan auto-generate subdomain)

### Step 7: Create Config File

Buat file `~/.cloudflared/config.yml`:

```yaml
tunnel: <TUNNEL_ID>  # Ganti dengan Tunnel ID dari Step 5
credentials-file: /Users/<username>/.cloudflared/<TUNNEL_ID>.json

ingress:
  # Route untuk aplikasi Streamlit
  - hostname: video-analyzer.yourdomain.com  # Ganti dengan domain Anda
    service: http://localhost:8501
  # Catch-all rule (harus di akhir)
  - service: http_status:404
```

**Untuk subdomain gratis, config lebih simple:**
```yaml
tunnel: <TUNNEL_ID>
credentials-file: /Users/<username>/.cloudflared/<TUNNEL_ID>.json

ingress:
  - service: http://localhost:8501
```

### Step 8: Run Tunnel

**Manual run:**
```bash
cloudflared tunnel run video-ai-analyzer
```

**Atau run sebagai service (auto-start):**

**Mac (LaunchAgent):**
```bash
# Install service
sudo cloudflared service install

# Start service
sudo launchctl load /Library/LaunchDaemons/com.cloudflare.cloudflared.plist
```

**Linux (Systemd):**
```bash
# Install service
sudo cloudflared service install

# Start service
sudo systemctl start cloudflared
sudo systemctl enable cloudflared
```

### Step 9: Test Akses

Buka browser dan akses:
- Domain custom: `https://video-analyzer.yourdomain.com`
- Subdomain gratis: URL akan muncul di terminal saat tunnel start

---

## 🐳 Setup dengan Docker (Recommended)

Lebih mudah dan konsisten dengan setup Docker yang sudah ada!

### Step 1: Update docker-compose.yml

Tambahkan service Cloudflare Tunnel:

```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: video-ai-analyzer
    ports:
      - "8501:8501"
    env_file:
      - .env
    volumes:
      - ./downloads:/app/downloads
      - ./output:/app/output
    restart: unless-stopped
    networks:
      - app-network

  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: cloudflared-tunnel
    command: tunnel run
    environment:
      - TUNNEL_TOKEN=${CLOUDFLARE_TUNNEL_TOKEN}
    restart: unless-stopped
    depends_on:
      - app
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### Step 2: Get Tunnel Token

1. Login ke Cloudflare Dashboard
2. Go to Zero Trust → Networks → Tunnels
3. Klik tunnel yang sudah dibuat
4. Klik "Configure" → "Quick Tunnel"
5. Copy **Tunnel Token**

### Step 3: Update .env

Tambahkan ke file `.env`:
```env
CLOUDFLARE_TUNNEL_TOKEN=your_tunnel_token_here
```

### Step 4: Run dengan Docker Compose

```bash
docker-compose up -d
```

Tunnel akan otomatis connect dan expose aplikasi!

---

## 🔄 Alternatif: DuckDNS (Lebih Simple, Tapi Perlu Port Forwarding)

Jika Cloudflare Tunnel terlalu kompleks, bisa pakai DuckDNS (juga gratis):

### Setup DuckDNS

1. **Daftar di DuckDNS:**
   - Buka https://www.duckdns.org/
   - Login dengan GitHub/Google/Reddit
   - Buat subdomain: `yourname.duckdns.org`

2. **Install DuckDNS Update Client:**

**Mac:**
```bash
# Tidak ada official client, pakai script
```

**Linux:**
```bash
# Install via Docker atau script
```

**Update Script (cron job):**
```bash
#!/bin/bash
# Update DuckDNS IP
curl "https://www.duckdns.org/update?domains=yourname&token=your-token&ip="
```

3. **Setup Port Forwarding di Router:**
   - Login ke router admin panel
   - Forward port 80/443 ke laptop server IP:8501
   - External port: 80 → Internal: 192.168.1.100:8501

4. **Setup Nginx Reverse Proxy (untuk HTTPS):**

Install Nginx dan Let's Encrypt:
```bash
# Install Nginx
sudo apt-get install nginx certbot python3-certbot-nginx

# Setup SSL
sudo certbot --nginx -d yourname.duckdns.org
```

**Kekurangan DuckDNS:**
- ❌ Perlu port forwarding (tidak semua ISP allow)
- ❌ Perlu setup SSL manual
- ❌ Perlu akses router

---

## 📊 Perbandingan Opsi FREE

| Fitur | Cloudflare Tunnel | DuckDNS |
|-------|-------------------|---------|
| **Biaya** | ✅ Gratis | ✅ Gratis |
| **HTTPS** | ✅ Otomatis | ⚠️ Manual (Let's Encrypt) |
| **Port Forwarding** | ✅ Tidak perlu | ❌ Perlu |
| **Setup** | Sedang | Mudah |
| **WebSocket Support** | ✅ Full support | ✅ Full support |
| **Reliability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Domain** | Custom atau subdomain | Subdomain saja |

---

## ✅ Rekomendasi Final

**Untuk project ini, saya rekomendasikan: Cloudflare Tunnel**

**Alasan:**
1. ✅ **Compatible 100%** - Tidak perlu ubah aplikasi
2. ✅ **Support WebSocket** - Penting untuk Streamlit real-time
3. ✅ **HTTPS Otomatis** - Security tanpa setup manual
4. ✅ **Tidak Perlu Port Forwarding** - Bekerja di semua network
5. ✅ **Gratis Total** - Tidak ada hidden cost
6. ✅ **Reliable** - Infrastructure Cloudflare

**Setup Time:** ~15-30 menit
**Maintenance:** Minimal (auto-restart dengan Docker)

---

## 🔧 Troubleshooting

### Tunnel tidak connect

```bash
# Cek logs
cloudflared tunnel info video-ai-analyzer

# Test connection
cloudflared tunnel run video-ai-analyzer --loglevel debug
```

### Aplikasi tidak accessible

1. Pastikan aplikasi running di `localhost:8501`
2. Test local: `curl http://localhost:8501`
3. Cek config file `~/.cloudflared/config.yml`

### WebSocket error

Pastikan config ingress support WebSocket:
```yaml
ingress:
  - hostname: video-analyzer.yourdomain.com
    service: http://localhost:8501
    originRequest:
      noHappyEyeballs: false
      keepAliveConnections: 100
      keepAliveTimeout: 90s
```

---

## 📝 Checklist Setup

- [ ] Cloudflare account sudah dibuat
- [ ] Domain sudah di-setup (atau pakai subdomain gratis)
- [ ] Cloudflared sudah di-install
- [ ] Tunnel sudah dibuat
- [ ] Config file sudah dibuat
- [ ] Tunnel sudah running
- [ ] Aplikasi bisa diakses via domain
- [ ] HTTPS sudah aktif
- [ ] Auto-start sudah dikonfigurasi (opsional)

---

## 🎉 Selesai!

Sekarang aplikasi Anda bisa diakses dari mana saja via domain!

**Contoh URL:**
- `https://video-analyzer.yourdomain.com`
- Atau `https://yourname.trycloudflare.com` (temporary)

**Tips:**
- Monitor tunnel status di Cloudflare Dashboard
- Setup monitoring/alerting untuk tunnel down
- Backup config file `~/.cloudflared/config.yml`

---

**Selamat! 🚀**


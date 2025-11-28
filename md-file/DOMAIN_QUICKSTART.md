# 🚀 Quick Start: Domain Public Access (FREE)

Panduan cepat setup domain public access **GRATIS** untuk Video AI Analyzer.

## ⭐ Rekomendasi: Cloudflare Tunnel

**Kenapa?**
- ✅ 100% GRATIS
- ✅ HTTPS otomatis
- ✅ Tidak perlu port forwarding
- ✅ Support WebSocket (penting untuk Streamlit)
- ✅ Compatible 100% dengan semua dependency

---

## 🎯 Quick Setup (3 Langkah)

### 1. Install Cloudflared

**Mac:**
```bash
brew install cloudflare/cloudflare/cloudflared
```

**Linux:**
```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```

### 2. Run Setup Script

```bash
./setup-cloudflare-tunnel.sh
```

Script akan guide Anda step-by-step!

### 3. Start Tunnel

**Manual:**
```bash
cloudflared tunnel run video-ai-analyzer
```

**Dengan Docker:**
```bash
# Pastikan CLOUDFLARE_TUNNEL_TOKEN sudah di .env
docker-compose -f docker-compose.with-tunnel.yml up -d
```

---

## 📋 Setup Manual (Jika Script Tidak Bisa)

### Step 1: Login
```bash
cloudflared tunnel login
```

### Step 2: Create Tunnel
```bash
cloudflared tunnel create video-ai-analyzer
```

### Step 3: Setup DNS (Opsional - untuk domain custom)
```bash
cloudflared tunnel route dns video-ai-analyzer video-analyzer.yourdomain.com
```

### Step 4: Create Config
Buat file `~/.cloudflared/config.yml`:
```yaml
tunnel: <TUNNEL_ID>
credentials-file: ~/.cloudflared/<TUNNEL_ID>.json

ingress:
  - service: http://localhost:8501
```

### Step 5: Run
```bash
cloudflared tunnel run video-ai-analyzer
```

---

## 🐳 Setup dengan Docker

### 1. Get Tunnel Token

1. Buka: https://one.dash.cloudflare.com/
2. Zero Trust → Networks → Tunnels
3. Klik tunnel Anda → Configure
4. Copy **Tunnel Token**

### 2. Update .env

```env
CLOUDFLARE_TUNNEL_TOKEN=your_tunnel_token_here
```

### 3. Run

```bash
docker-compose -f docker-compose.with-tunnel.yml up -d
```

---

## 🌐 Akses Aplikasi

Setelah tunnel running, akses via:
- **Subdomain gratis**: URL muncul di terminal
- **Domain custom**: `https://video-analyzer.yourdomain.com`

---

## 📚 Dokumentasi Lengkap

Lihat: `md-file/DOMAIN_SETUP_FREE.md` untuk detail lengkap.

---

## ❓ FAQ

**Q: Perlu domain berbayar?**  
A: Tidak! Bisa pakai subdomain gratis dari Cloudflare.

**Q: Perlu port forwarding?**  
A: Tidak! Cloudflare Tunnel tidak perlu port forwarding.

**Q: Compatible dengan Streamlit?**  
A: Ya! Full support WebSocket untuk real-time updates.

**Q: Berapa biaya?**  
A: 100% GRATIS! Tidak ada hidden cost.

---

**Selamat! 🎉**


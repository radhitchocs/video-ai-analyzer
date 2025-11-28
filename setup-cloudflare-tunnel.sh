#!/bin/bash

# Script untuk setup Cloudflare Tunnel dengan mudah
# Usage: ./setup-cloudflare-tunnel.sh

set -e

echo "🌐 Cloudflare Tunnel Setup - Video AI Analyzer"
echo "=============================================="
echo ""

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null; then
    echo "⚠️  cloudflared tidak ditemukan!"
    echo ""
    echo "Install cloudflared:"
    echo "  Mac:    brew install cloudflare/cloudflare/cloudflared"
    echo "  Linux:  wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb && sudo dpkg -i cloudflared-linux-amd64.deb"
    echo ""
    read -p "Tekan Enter setelah install cloudflared, atau Ctrl+C untuk cancel..."
fi

echo "✅ cloudflared ditemukan: $(cloudflared --version | head -n 1)"
echo ""

# Step 1: Login
echo "📝 Step 1: Login ke Cloudflare"
echo "   Browser akan terbuka untuk authorize..."
echo ""
read -p "Tekan Enter untuk melanjutkan login..."

cloudflared tunnel login

echo ""
echo "✅ Login berhasil!"
echo ""

# Step 2: Create tunnel
echo "📝 Step 2: Create Tunnel"
echo ""
read -p "Masukkan nama tunnel (default: video-ai-analyzer): " TUNNEL_NAME
TUNNEL_NAME=${TUNNEL_NAME:-video-ai-analyzer}

echo ""
echo "Creating tunnel: $TUNNEL_NAME"
TUNNEL_OUTPUT=$(cloudflared tunnel create "$TUNNEL_NAME" 2>&1)
echo "$TUNNEL_OUTPUT"

# Extract Tunnel ID
TUNNEL_ID=$(echo "$TUNNEL_OUTPUT" | grep -oP 'Created tunnel \K[^ ]+' || echo "")

if [ -z "$TUNNEL_ID" ]; then
    # Try alternative extraction
    TUNNEL_ID=$(cloudflared tunnel list | grep "$TUNNEL_NAME" | awk '{print $1}' | head -n 1)
fi

if [ -z "$TUNNEL_ID" ]; then
    echo "⚠️  Tidak bisa extract Tunnel ID otomatis"
    echo "   Silakan copy Tunnel ID dari output di atas"
    read -p "Masukkan Tunnel ID: " TUNNEL_ID
fi

echo ""
echo "✅ Tunnel ID: $TUNNEL_ID"
echo ""

# Step 3: Setup domain
echo "📝 Step 3: Setup Domain"
echo ""
echo "Pilih opsi:"
echo "  1) Pakai domain sendiri (sudah di Cloudflare)"
echo "  2) Pakai subdomain gratis (temporary)"
echo ""
read -p "Pilih (1 atau 2): " DOMAIN_OPTION

if [ "$DOMAIN_OPTION" = "1" ]; then
    read -p "Masukkan subdomain (contoh: video-analyzer): " SUBDOMAIN
    read -p "Masukkan domain (contoh: example.com): " DOMAIN
    FULL_DOMAIN="${SUBDOMAIN}.${DOMAIN}"
    
    echo ""
    echo "Setting up DNS route..."
    cloudflared tunnel route dns "$TUNNEL_NAME" "$FULL_DOMAIN"
    echo "✅ DNS route berhasil dibuat: $FULL_DOMAIN"
else
    FULL_DOMAIN=""
    echo "✅ Akan pakai subdomain gratis (akan muncul saat tunnel start)"
fi

# Step 4: Create config file
echo ""
echo "📝 Step 4: Create Config File"
echo ""

CONFIG_DIR="$HOME/.cloudflared"
mkdir -p "$CONFIG_DIR"

CONFIG_FILE="$CONFIG_DIR/config.yml"

# Ask if using Docker
echo ""
read -p "Apakah akan menggunakan Docker? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Config untuk Docker (pakai service name)
    SERVICE_URL="http://app:8501"
else
    # Config untuk local (pakai localhost)
    SERVICE_URL="http://localhost:8501"
fi

if [ -z "$FULL_DOMAIN" ]; then
    # Config untuk subdomain gratis
    cat > "$CONFIG_FILE" << EOF
tunnel: $TUNNEL_ID
credentials-file: $CONFIG_DIR/$TUNNEL_ID.json

ingress:
  - service: $SERVICE_URL
EOF
else
    # Config untuk domain custom
    cat > "$CONFIG_FILE" << EOF
tunnel: $TUNNEL_ID
credentials-file: $CONFIG_DIR/$TUNNEL_ID.json

ingress:
  - hostname: $FULL_DOMAIN
    service: $SERVICE_URL
  - service: http_status:404
EOF
fi

echo "✅ Config file dibuat: $CONFIG_FILE"
echo ""

# Step 5: Get tunnel token (for Docker)
echo "📝 Step 5: Get Tunnel Token untuk Docker"
echo ""
echo "Untuk menggunakan dengan Docker, Anda perlu Tunnel Token."
echo ""
echo "Cara mendapatkan:"
echo "  1. Buka: https://one.dash.cloudflare.com/"
echo "  2. Go to: Zero Trust → Networks → Tunnels"
echo "  3. Klik tunnel: $TUNNEL_NAME"
echo "  4. Klik 'Configure' → Copy 'Tunnel Token'"
echo ""
read -p "Masukkan Tunnel Token (atau Enter untuk skip): " TUNNEL_TOKEN

if [ ! -z "$TUNNEL_TOKEN" ]; then
    # Update .env file
    if [ ! -f .env ]; then
        echo "⚠️  File .env tidak ditemukan, membuat baru..."
        touch .env
    fi
    
    # Check if CLOUDFLARE_TUNNEL_TOKEN already exists
    if grep -q "CLOUDFLARE_TUNNEL_TOKEN" .env; then
        # Update existing
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # Mac
            sed -i '' "s|CLOUDFLARE_TUNNEL_TOKEN=.*|CLOUDFLARE_TUNNEL_TOKEN=$TUNNEL_TOKEN|" .env
        else
            # Linux
            sed -i "s|CLOUDFLARE_TUNNEL_TOKEN=.*|CLOUDFLARE_TUNNEL_TOKEN=$TUNNEL_TOKEN|" .env
        fi
    else
        # Add new
        echo "" >> .env
        echo "# Cloudflare Tunnel" >> .env
        echo "CLOUDFLARE_TUNNEL_TOKEN=$TUNNEL_TOKEN" >> .env
    fi
    
    echo "✅ Tunnel Token sudah ditambahkan ke .env"
    echo ""
    echo "📦 Untuk run dengan Docker:"
    echo "   docker-compose -f docker-compose.with-tunnel.yml up -d"
fi

# Step 6: Test tunnel
echo ""
echo "📝 Step 6: Test Tunnel"
echo ""
read -p "Jalankan tunnel sekarang untuk test? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Starting tunnel..."
    echo "   (Tekan Ctrl+C untuk stop)"
    echo ""
    cloudflared tunnel run "$TUNNEL_NAME"
else
    echo ""
    echo "✅ Setup selesai!"
    echo ""
    echo "📋 Untuk run tunnel:"
    echo "   cloudflared tunnel run $TUNNEL_NAME"
    echo ""
    if [ ! -z "$FULL_DOMAIN" ]; then
        echo "🌐 Akses aplikasi di:"
        echo "   https://$FULL_DOMAIN"
    else
        echo "🌐 URL akan muncul saat tunnel start"
    fi
fi

echo ""
echo "🎉 Setup Cloudflare Tunnel selesai!"
echo ""
echo "📚 Dokumentasi lengkap: md-file/DOMAIN_SETUP_FREE.md"


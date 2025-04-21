#!/bin/bash

# Web Log Analyzer Deployment Script
set -e

# Configuration
DB_USER="web_log_user"
DB_NAME="web_log_analysis"
CONFIG_DIR="/etc/web_log_analyzer"
APP_DIR="/opt/web_log_analyzer"
VENV_DIR="$APP_DIR/venv"
REQUIREMENTS="$APP_DIR/requirements/prod.txt"

# Check for MySQL
if ! command -v mysql &> /dev/null; then
    echo "MySQL is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y mysql-server mysql-client
fi

# Setup database
echo "Setting up database..."
sudo mysql -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"
sudo mysql -e "CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY 'secure_password';"
sudo mysql -e "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# Create app directory
echo "Creating application directory..."
sudo mkdir -p $APP_DIR $CONFIG_DIR
sudo chown -R $USER:$USER $APP_DIR $CONFIG_DIR

# Copy application files (assuming you're running from project root)
echo "Copying application files..."
cp -r . $APP_DIR/

# Setup Python environment
echo "Setting up Python virtual environment..."
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate
pip install --upgrade pip
pip install -r $REQUIREMENTS

# Initialize database schema
echo "Initializing database schema..."
python -c "
from src.storage.models.apache_log import ApacheLog;
from src.storage.models.nginx_log import NginxLog;
ApacheLog().create_table();
NginxLog().create_table();
"

# Setup systemd service
echo "Setting up systemd service..."
sudo tee /etc/systemd/system/web_log_analyzer.service > /dev/null <<EOF
[Unit]
Description=Web Log Analyzer Service
After=network.target mysql.service

[Service]
User=$USER
WorkingDirectory=$APP_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/python -m src.api.main
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable web_log_analyzer.service
sudo systemctl start web_log_analyzer.service

echo "Deployment completed successfully!"
echo "Application is running and will start automatically on boot."
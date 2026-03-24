#!/bin/bash

# Martial World AWS 一键部署脚本
# 使用方法：./deploy_to_aws.sh <AWS公网IP> <密钥文件路径>

set -e

if [ "$#" -ne 2 ]; then
    echo "使用方法: ./deploy_to_aws.sh <AWS公网IP> <密钥文件路径>"
    echo "例如: ./deploy_to_aws.sh 54.123.45.67 ~/Downloads/martial-world.pem"
    exit 1
fi

AWS_IP=$1
KEY_FILE=$2

echo "=========================================="
echo "Martial World AWS 自动部署"
echo "=========================================="
echo "目标服务器: $AWS_IP"
echo "密钥文件: $KEY_FILE"
echo ""

# 1. 打包项目
echo "📦 [1/5] 打包项目文件..."
cd /Users/libing/ai-skills-platform
tar -czf martial-world.tar.gz backend/
echo "✅ 打包完成"
echo ""

# 2. 上传文件
echo "📤 [2/5] 上传文件到AWS..."
scp -i "$KEY_FILE" martial-world.tar.gz ubuntu@$AWS_IP:~/
echo "✅ 上传完成"
echo ""

# 3. 远程安装环境
echo "🔧 [3/5] 安装服务器环境..."
ssh -i "$KEY_FILE" ubuntu@$AWS_IP << 'ENDSSH'
# 解压文件
tar -xzf martial-world.tar.gz

# 安装Python依赖
pip3 install fastapi uvicorn anthropic 2>/dev/null || echo "依赖已安装"
ENDSSH
echo "✅ 环境安装完成"
echo ""

# 4. 创建systemd服务
echo "⚙️  [4/5] 配置系统服务..."
ssh -i "$KEY_FILE" ubuntu@$AWS_IP << 'ENDSSH'
sudo tee /etc/systemd/system/martial-world.service > /dev/null <<EOF
[Unit]
Description=Martial World API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/backend
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 启动服务
sudo systemctl daemon-reload
sudo systemctl enable martial-world
sudo systemctl restart martial-world
ENDSSH
echo "✅ 服务配置完成"
echo ""

# 5. 验证部署
echo "🧪 [5/5] 验证部署..."
sleep 3
if curl -s http://$AWS_IP:8000 | grep -q "Martial World"; then
    echo "✅ 部署成功！"
    echo ""
    echo "=========================================="
    echo "🎉 部署完成！"
    echo "=========================================="
    echo ""
    echo "📍 访问地址："
    echo "   http://$AWS_IP:8000"
    echo ""
    echo "📖 API文档："
    echo "   http://$AWS_IP:8000/docs"
    echo ""
    echo "🔍 查看日志："
    echo "   ssh -i $KEY_FILE ubuntu@$AWS_IP"
    echo "   sudo journalctl -u martial-world -f"
    echo ""
    echo "🛑 停止服务："
    echo "   ssh -i $KEY_FILE ubuntu@$AWS_IP"
    echo "   sudo systemctl stop martial-world"
    echo ""
else
    echo "❌ 部署可能失败，请检查服务状态"
    echo "检查命令："
    echo "   ssh -i $KEY_FILE ubuntu@$AWS_IP"
    echo "   sudo systemctl status martial-world"
fi

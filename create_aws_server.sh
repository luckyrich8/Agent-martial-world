#!/bin/bash

# Martial World - AWS EC2 一键创建脚本
# 使用方法：./create_aws_server.sh

set -e

echo "=========================================="
echo "🚀 Martial World AWS 服务器自动创建"
echo "=========================================="
echo ""

# 检查AWS CLI
if ! command -v aws &> /dev/null; then
    echo "❌ 请先安装AWS CLI："
    echo "   brew install awscli"
    exit 1
fi

echo "📋 [1/6] 创建密钥对..."
KEY_NAME="martial-world-key"
aws ec2 create-key-pair \
    --key-name $KEY_NAME \
    --query 'KeyMaterial' \
    --output text > ~/martial-world-key.pem

chmod 400 ~/martial-world-key.pem
echo "✅ 密钥已保存到：~/martial-world-key.pem"
echo ""

echo "🔐 [2/6] 创建安全组..."
SG_ID=$(aws ec2 create-security-group \
    --group-name martial-world-sg \
    --description "Security group for Martial World API" \
    --query 'GroupId' \
    --output text)

echo "✅ 安全组ID: $SG_ID"
echo ""

echo "🔓 [3/6] 配置安全组规则..."
# 允许SSH (端口22)
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0

# 允许HTTP (端口80)
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0

# 允许API端口 (端口8000)
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 8000 \
    --cidr 0.0.0.0/0

echo "✅ 安全组规则配置完成"
echo ""

echo "🖥️  [4/6] 启动EC2实例（t2.micro免费套餐）..."
# 获取最新Ubuntu AMI ID
AMI_ID=$(aws ec2 describe-images \
    --owners 099720109477 \
    --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" \
    --query 'sort_by(Images, &CreationDate)[-1].ImageId' \
    --output text)

echo "   使用AMI: $AMI_ID"

INSTANCE_ID=$(aws ec2 run-instances \
    --image-id $AMI_ID \
    --count 1 \
    --instance-type t2.micro \
    --key-name $KEY_NAME \
    --security-group-ids $SG_ID \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=Martial-World-API}]' \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "✅ 实例ID: $INSTANCE_ID"
echo ""

echo "⏳ [5/6] 等待实例启动（约30秒）..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID
echo "✅ 实例已启动"
echo ""

echo "🌐 [6/6] 获取公网IP..."
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

echo "✅ 公网IP: $PUBLIC_IP"
echo ""

echo "=========================================="
echo "🎉 AWS服务器创建成功！"
echo "=========================================="
echo ""
echo "📋 服务器信息："
echo "   实例ID: $INSTANCE_ID"
echo "   公网IP: $PUBLIC_IP"
echo "   密钥文件: ~/martial-world-key.pem"
echo ""
echo "🚀 下一步："
echo ""
echo "1️⃣  等待1分钟让服务器完全启动"
echo ""
echo "2️⃣  运行部署脚本："
echo "   cd /Users/libing/ai-skills-platform"
echo "   ./deploy_to_aws.sh $PUBLIC_IP ~/martial-world-key.pem"
echo ""
echo "3️⃣  访问你的API："
echo "   http://$PUBLIC_IP:8000"
echo ""
echo "💾 保存信息到文件..."
cat > ~/martial-world-server-info.txt <<EOF
Martial World AWS 服务器信息
==============================

实例ID: $INSTANCE_ID
公网IP: $PUBLIC_IP
密钥文件: ~/martial-world-key.pem
创建时间: $(date)

访问地址: http://$PUBLIC_IP:8000
API文档: http://$PUBLIC_IP:8000/docs

SSH连接命令:
ssh -i ~/martial-world-key.pem ubuntu@$PUBLIC_IP

部署命令:
cd /Users/libing/ai-skills-platform
./deploy_to_aws.sh $PUBLIC_IP ~/martial-world-key.pem
EOF

echo "✅ 信息已保存到：~/martial-world-server-info.txt"
echo ""

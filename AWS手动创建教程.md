# AWS EC2 手动创建教程（图文版）

## 步骤1：登录AWS控制台

1. 访问：https://console.aws.amazon.com
2. 登录你的AWS账号

---

## 步骤2：进入EC2服务

1. 在顶部搜索框输入：**EC2**
2. 点击 **EC2**（虚拟服务器）

---

## 步骤3：启动实例

1. 点击橙色按钮：**Launch Instance**（启动实例）

---

## 步骤4：配置实例（重要）

### 4.1 名称和标签
```
Name: Martial-World-API
```

### 4.2 选择AMI（操作系统镜像）
```
✅ 选择：Ubuntu Server 22.04 LTS
   确保有 "Free tier eligible" 标签（免费套餐）
```

### 4.3 选择实例类型
```
✅ 选择：t2.micro
   （显示 "Free tier eligible"）
```

### 4.4 密钥对（Key pair）
```
1. 点击 "Create new key pair"
2. Key pair name: martial-world-key
3. Key pair type: RSA
4. Private key file format: .pem
5. 点击 "Create key pair"
6. 浏览器会自动下载文件：martial-world-key.pem
7. 把这个文件保存到：~/Downloads/martial-world-key.pem
```

### 4.5 网络设置（Network settings）- 非常重要！

点击 **Edit**（编辑），然后配置：

```
✅ Allow SSH traffic from: Anywhere (0.0.0.0/0)
✅ Allow HTTP traffic from the internet: 勾选
✅ 点击 "Add security group rule" 添加自定义规则：
   - Type: Custom TCP
   - Port range: 8000
   - Source: Anywhere (0.0.0.0/0)
```

### 4.6 配置存储
```
保持默认：8 GiB gp3
（已包含在免费套餐中）
```

---

## 步骤5：启动实例

1. 右侧查看配置摘要
2. 确认是 **Free tier** 和 **t2.micro**
3. 点击橙色按钮：**Launch instance**

---

## 步骤6：查看实例信息

1. 等待30秒-1分钟
2. 点击实例ID（蓝色链接）
3. 找到并复制 **Public IPv4 address**（例如：54.123.45.67）
4. 记下这个IP地址！

---

## 步骤7：测试连接

打开终端（Terminal）：

```bash
# 修改密钥文件权限
chmod 400 ~/Downloads/martial-world-key.pem

# 测试SSH连接
ssh -i ~/Downloads/martial-world-key.pem ubuntu@你的公网IP

# 例如：
# ssh -i ~/Downloads/martial-world-key.pem ubuntu@54.123.45.67
```

如果能连接上，说明创建成功！

---

## 步骤8：部署Martial World

```bash
# 退出SSH（如果还在连接中）
exit

# 运行部署脚本
cd /Users/libing/ai-skills-platform
./deploy_to_aws.sh 你的公网IP ~/Downloads/martial-world-key.pem

# 例如：
# ./deploy_to_aws.sh 54.123.45.67 ~/Downloads/martial-world-key.pem
```

---

## 完成！

访问：`http://你的公网IP:8000`

查看API文档：`http://你的公网IP:8000/docs`

---

## ⚠️ 重要提醒

1. **保管好密钥文件**（martial-world-key.pem），丢了就无法连接服务器
2. **记住公网IP**，这是你的服务访问地址
3. **免费套餐限制**：每月750小时（够用）

---

## 🆘 如果遇到问题

### 问题1：无法SSH连接

**解决方案：**
1. 检查安全组是否开放了端口22（SSH）
2. 检查密钥文件权限：`chmod 400 ~/Downloads/martial-world-key.pem`
3. 确认使用的是正确的用户名：`ubuntu`

### 问题2：无法访问API（http://IP:8000）

**解决方案：**
1. 确认安全组开放了端口8000
2. SSH连接到服务器，检查服务状态：
   ```bash
   sudo systemctl status martial-world
   ```

### 问题3：服务器启动失败

**解决方案：**
查看日志：
```bash
ssh -i ~/Downloads/martial-world-key.pem ubuntu@你的IP
sudo journalctl -u martial-world -n 50
```

---

## 📞 需要帮助？

记录以下信息后联系技术支持：
- 实例ID
- 公网IP
- 错误信息截图

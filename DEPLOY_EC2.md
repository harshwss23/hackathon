# Deploy StoryLens AI to Amazon EC2

This guide deploys the container directly on one Amazon Linux 2023 EC2 instance. It is appropriate for a hackathon/demo deployment. For a production service, place the instance behind an Application Load Balancer with HTTPS, or move the same image to ECS.

## 1. Launch the instance

Create an EC2 instance with:

- AMI: Amazon Linux 2023
- Size: `t3.small` or larger (recommended for pandas and Docker builds)
- Storage: 16 GB gp3
- Public IPv4 address or Elastic IP
- Security group inbound rules:
  - HTTP TCP 80 from `0.0.0.0/0`
  - SSH TCP 22 from **your IP only**, or omit SSH and use AWS Systems Manager Session Manager

Do not expose port 8080 publicly when Docker maps the application to port 80.

## 2. Connect and install Docker

```bash
sudo yum update -y
sudo yum install -y docker git
sudo service docker start
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user
```

Log out and reconnect so the Docker group membership takes effect, then verify:

```bash
docker info
```

## 3. Copy the application

Clone the repository:

```bash
git clone https://github.com/harshwss23/hackathon.git
cd hackathon
```

The repository is private, so authenticate with a repository-scoped GitHub deploy key or GitHub's supported credential flow. Never place a personal access token directly in the clone URL or shell history.

## 4. Configure the Groq secret

Create the environment file on the instance. Do not commit it:

```bash
cp .env.example .env
chmod 600 .env
nano .env
```

Set `GROQ_API_KEY` to a newly rotated Groq key. Keep `GROQ_MODEL=openai/gpt-oss-20b` unless you intentionally select another supported model.

For a production deployment, store this value in AWS Systems Manager Parameter Store or AWS Secrets Manager and inject it at runtime instead of keeping a long-lived plaintext file.

## 5. Build and run

```bash
docker build --tag storylens-ai:2.1 .
docker run --detach \
  --name storylens \
  --restart unless-stopped \
  --env-file .env \
  --publish 80:8080 \
  storylens-ai:2.1
```

Verify on the instance:

```bash
curl http://127.0.0.1/api/health
docker ps
docker logs --tail 100 storylens
```

Open `http://EC2_PUBLIC_IP` in a browser.

## 6. Update the deployment

```bash
cd hackathon
git pull --ff-only
docker build --tag storylens-ai:2.1 .
docker stop storylens
docker rm storylens
docker run --detach \
  --name storylens \
  --restart unless-stopped \
  --env-file .env \
  --publish 80:8080 \
  storylens-ai:2.1
```

## HTTPS and a domain

For a durable public deployment:

1. Allocate an Elastic IP or put the instance in an Application Load Balancer target group.
2. Point a Route 53 DNS record at the Elastic IP or load balancer.
3. Use AWS Certificate Manager on the load balancer for HTTPS.
4. Allow inbound 443 from the internet and restrict the instance's application port to the load balancer security group.

## Useful operations

```bash
docker inspect --format='{{json .State.Health}}' storylens
docker logs --follow storylens
docker restart storylens
docker stop storylens
```

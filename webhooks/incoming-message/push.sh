docker buildx build --platform linux/amd64 -t dev-airtext-incoming-message .
docker tag dev-airtext-incoming-message:latest 312590578399.dkr.ecr.us-east-1.amazonaws.com/dev-airtext-incoming-message:latest
docker push 312590578399.dkr.ecr.us-east-1.amazonaws.com/dev-airtext-incoming-message:latest

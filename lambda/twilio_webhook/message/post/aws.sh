export ENVIRONMENT=prod
echo "Using '${ENVIRONMENT}' environment..."
echo "Creating ECR service role..."
aws iam create-role --role-name codebuild-${ENVIRONMENT}-twilio-webhook-messages-post-ecr-service-role --assume-role-policy-document '{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"Service": "codebuild.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
echo "Attaching role policies..."
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess --role-name codebuild-${ENVIRONMENT}-twilio-webhook-messages-post-ecr-service-role
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AWSLambda_FullAccess --role-name codebuild-${ENVIRONMENT}-twilio-webhook-messages-post-ecr-service-role
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AWSCodeArtifactReadOnlyAccess --role-name codebuild-${ENVIRONMENT}-twilio-webhook-messages-post-ecr-service-role
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess --role-name codebuild-${ENVIRONMENT}-twilio-webhook-messages-post-ecr-service-role
echo "Creating Lambda service role..."
aws iam create-role --role-name lambda-${ENVIRONMENT}-twilio-webhook-messages-post-cloudwatch-service-role --assume-role-policy-document '{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
echo "Attaching role policies..."
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess --role-name lambda-${ENVIRONMENT}-twilio-webhook-messages-post-cloudwatch-service-role
echo "Creating ECR repository"
aws ecr create-repository --repository-name ${ENVIRONMENT}-twilio-webhook-messages-post-lambda
echo "Configuring roles..."
sleep 10s
echo "Creating Lambda function"
aws lambda create-function \
--function-name ${ENVIRONMENT}-twilio-webhook-messages-post \
--role arn:aws:iam::312590578399:role/lambda-${ENVIRONMENT}-twilio-webhook-messages-post-cloudwatch-service-role \
--code ImageUri=312590578399.dkr.ecr.us-east-1.amazonaws.com/base:latest \
--package-type Image
echo "Creating CodeBuild project..."
aws codebuild create-project \
--name ${ENVIRONMENT}-twilio-webhook-messages-post-ecr \
--source '{"type": "GITHUB", "location": "https://github.com/mitchbregs/airtext", "buildspec": "lambda/twilio_webhook/message/post/buildspec.'${ENVIRONMENT}'.yml"}' \
--artifacts '{"type": "NO_ARTIFACTS"}' \
--environment '{"type": "LINUX_CONTAINER", "image": "aws/codebuild/standard:6.0", "privilegedMode": true, "computeType": "BUILD_GENERAL1_SMALL"}' \
--service-role codebuild-${ENVIRONMENT}-twilio-webhook-messages-post-ecr-service-role \
--logs-config '{"cloudWatchLogs": {"status": "ENABLED"}}'

export ENVIRONMENT=prod
echo "Using '${ENVIRONMENT}' environment..."
echo "Creating ECR service role..."
aws iam create-role --role-name codebuild-${ENVIRONMENT}-airtext-api-group-contacts-post-ecr-service --assume-role-policy-document '{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"Service": "codebuild.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
echo "Attaching role policies..."
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess --role-name codebuild-${ENVIRONMENT}-airtext-api-group-contacts-post-ecr-service
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AWSLambda_FullAccess --role-name codebuild-${ENVIRONMENT}-airtext-api-group-contacts-post-ecr-service
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AWSCodeArtifactReadOnlyAccess --role-name codebuild-${ENVIRONMENT}-airtext-api-group-contacts-post-ecr-service
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess --role-name codebuild-${ENVIRONMENT}-airtext-api-group-contacts-post-ecr-service
echo "Creating Lambda service role..."
aws iam create-role --role-name lambda-${ENVIRONMENT}-airtext-api-group-contacts-post-cloudwatch-service --assume-role-policy-document '{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
echo "Attaching role policies..."
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess --role-name lambda-${ENVIRONMENT}-airtext-api-group-contacts-post-cloudwatch-service
echo "Creating ECR repository"
aws ecr create-repository --repository-name ${ENVIRONMENT}-airtext-api-group-contacts-post-lambda
echo "Configuring roles..."
sleep 10s
echo "Creating Lambda function"
aws lambda create-function \
--function-name ${ENVIRONMENT}-airtext-api-group-contacts-post \
--role arn:aws:iam::312590578399:role/lambda-${ENVIRONMENT}-airtext-api-group-contacts-post-cloudwatch-service \
--code ImageUri=312590578399.dkr.ecr.us-east-1.amazonaws.com/base:latest \
--package-type Image
echo "Creating CodeBuild project..."
aws codebuild create-project \
--name ${ENVIRONMENT}-airtext-api-group-contacts-post-ecr \
--source '{"type": "GITHUB", "location": "https://github.com/mitchbregs/airtext", "buildspec": "airtext_api/group_contacts/post/buildspec.'${ENVIRONMENT}'.yml"}' \
--artifacts '{"type": "NO_ARTIFACTS"}' \
--environment '{"type": "LINUX_CONTAINER", "image": "aws/codebuild/standard:6.0", "privilegedMode": true, "computeType": "BUILD_GENERAL1_SMALL"}' \
--service-role codebuild-${ENVIRONMENT}-airtext-api-group-contacts-post-ecr-service \
--logs-config '{"cloudWatchLogs": {"status": "ENABLED"}}'

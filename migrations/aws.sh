export ENVIRONMENT=dev
echo "Using '${ENVIRONMENT}' environment..."
echo "Creating role..."
aws iam create-role --role-name codebuild-${ENVIRONMENT}-alembic-migrations-rds-service-role --assume-role-policy-document '{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"Service": "codebuild.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
echo "Attaching role policies..."
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly --role-name codebuild-${ENVIRONMENT}-alembic-migrations-rds-service-role
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AWSCodeArtifactAdminAccess --role-name codebuild-${ENVIRONMENT}-alembic-migrations-rds-service-role
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess --role-name codebuild-${ENVIRONMENT}-alembic-migrations-rds-service-role
echo "Creating CodeBuild project..."
sleep 10s
aws codebuild \
create-project \
--name airtext-database-migrations \
--source '{"type": "GITHUB", "location": "https://github.com/mitchbregs/airtext", "buildspec": "migrations/buildspec.'${ENVIRONMENT}'.yml"}' \
--artifacts '{"type": "NO_ARTIFACTS"}' \
--environment '{"type": "LINUX_CONTAINER", "image": "aws/codebuild/standard:6.0", "privilegedMode": true, "computeType": "BUILD_GENERAL1_SMALL"}' \
--service-role codebuild-${ENVIRONMENT}-alembic-migrations-rds-service-role \
--logs-config '{"cloudWatchLogs": {"status": "ENABLED"}}'

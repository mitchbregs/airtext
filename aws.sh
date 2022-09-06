echo "Creating role..."
aws iam create-role --role-name codebuild-airtext-pypi-codeartifact-service-role --assume-role-policy-document '{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"Service": "codebuild.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
echo "Attaching role policies..."
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly --role-name codebuild-airtext-pypi-codeartifact-service-role
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AWSCodeArtifactAdminAccess --role-name codebuild-airtext-pypi-codeartifact-service-role
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess --role-name codebuild-airtext-pypi-codeartifact-service-role
echo "Creating CodeBuild project..."
sleep 10s
aws codebuild create-project \
    --name airtext-pypi-package \
    --source '{"type": "GITHUB", "location": "https://github.com/mitchbregs/airtext", "buildspec": "buildspec.yml"}' \
    --artifacts '{"type": "NO_ARTIFACTS"}' \
    --environment '{"type": "LINUX_CONTAINER", "image": "aws/codebuild/standard:6.0", "computeType": "BUILD_GENERAL1_SMALL"}' \
    --service-role codebuild-airtext-pypi-codeartifact-service-role \
    --logs-config '{"cloudWatchLogs": {"status": "ENABLED"}}'

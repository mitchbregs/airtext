echo "Creating role..."
aws iam create-role --role-name codebuild-airtext-api-dev-group-contacts-get-service-role --assume-role-policy-document '{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"Service": "codebuild.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
echo "Attaching role policies..."
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess --role-name codebuild-airtext-api-dev-group-contacts-get-service-role
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AWSLambda_FullAccess --role-name codebuild-airtext-api-dev-group-contacts-get-service-role
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AWSCodeArtifactReadOnlyAccess --role-name codebuild-airtext-api-dev-group-contacts-get-service-role
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess --role-name codebuild-airtext-api-dev-group-contacts-get-service-role
echo "Creating CodeBuild project..."
sleep 10s
aws codebuild \
create-project \
--name dev-airtext-api-group-contacts-get \
--source '{"type": "GITHUB", "location": "https://github.com/mitchbregs/airtext", "buildspec": "api/group_contacts/get/buildspec.yml"}' \
--artifacts '{"type": "NO_ARTIFACTS"}' \
--environment '{"type": "LINUX_CONTAINER", "image": "aws/codebuild/standard:6.0", "privilegedMode": true, "computeType": "BUILD_GENERAL1_SMALL"}' \
--service-role codebuild-airtext-api-dev-group-contacts-get-service-role \
--logs-config '{"cloudWatchLogs": {"status": "ENABLED"}}'

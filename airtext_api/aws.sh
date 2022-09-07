# aws lambda update-function-configuration --function-name dev-airtext-api-contacts-delete --environment "Variables={TWILIO_ACCOUNT_SID='${TWILIO_ACCOUNT_SID}', TWILIO_AUTH_TOKEN='${TWILIO_AUTH_TOKEN}', MESSAGES_DATABASE_URL='${MESSAGES_DATABASE_URL}'}" --timeout 10
# aws lambda update-function-configuration --function-name dev-airtext-api-contacts-get --environment "Variables={TWILIO_ACCOUNT_SID='${TWILIO_ACCOUNT_SID}', TWILIO_AUTH_TOKEN='${TWILIO_AUTH_TOKEN}', MESSAGES_DATABASE_URL='${MESSAGES_DATABASE_URL}'}" --timeout 10
# aws lambda update-function-configuration --function-name dev-airtext-api-contacts-post --environment "Variables={TWILIO_ACCOUNT_SID='${TWILIO_ACCOUNT_SID}', TWILIO_AUTH_TOKEN='${TWILIO_AUTH_TOKEN}', MESSAGES_DATABASE_URL='${MESSAGES_DATABASE_URL}'}" --timeout 10
# aws lambda update-function-configuration --function-name dev-airtext-api-contacts-put --environment "Variables={TWILIO_ACCOUNT_SID='${TWILIO_ACCOUNT_SID}', TWILIO_AUTH_TOKEN='${TWILIO_AUTH_TOKEN}', MESSAGES_DATABASE_URL='${MESSAGES_DATABASE_URL}'}" --timeout 10
# aws lambda update-function-configuration --function-name dev-airtext-api-group-contacts-delete --environment "Variables={TWILIO_ACCOUNT_SID='${TWILIO_ACCOUNT_SID}', TWILIO_AUTH_TOKEN='${TWILIO_AUTH_TOKEN}', MESSAGES_DATABASE_URL='${MESSAGES_DATABASE_URL}'}" --timeout 10
# aws lambda update-function-configuration --function-name dev-airtext-api-group-contacts-get --environment "Variables={TWILIO_ACCOUNT_SID='${TWILIO_ACCOUNT_SID}', TWILIO_AUTH_TOKEN='${TWILIO_AUTH_TOKEN}', MESSAGES_DATABASE_URL='${MESSAGES_DATABASE_URL}'}" --timeout 10
# aws lambda update-function-configuration --function-name dev-airtext-api-group-contacts-post --environment "Variables={TWILIO_ACCOUNT_SID='${TWILIO_ACCOUNT_SID}', TWILIO_AUTH_TOKEN='${TWILIO_AUTH_TOKEN}', MESSAGES_DATABASE_URL='${MESSAGES_DATABASE_URL}'}" --timeout 10
# aws lambda update-function-configuration --function-name dev-airtext-api-groups-delete --environment "Variables={TWILIO_ACCOUNT_SID='${TWILIO_ACCOUNT_SID}', TWILIO_AUTH_TOKEN='${TWILIO_AUTH_TOKEN}', MESSAGES_DATABASE_URL='${MESSAGES_DATABASE_URL}'}" --timeout 10
# aws lambda update-function-configuration --function-name dev-airtext-api-groups-get --environment "Variables={TWILIO_ACCOUNT_SID='${TWILIO_ACCOUNT_SID}', TWILIO_AUTH_TOKEN='${TWILIO_AUTH_TOKEN}', MESSAGES_DATABASE_URL='${MESSAGES_DATABASE_URL}'}" --timeout 10
# aws lambda update-function-configuration --function-name dev-airtext-api-groups-post --environment "Variables={TWILIO_ACCOUNT_SID='${TWILIO_ACCOUNT_SID}', TWILIO_AUTH_TOKEN='${TWILIO_AUTH_TOKEN}', MESSAGES_DATABASE_URL='${MESSAGES_DATABASE_URL}'}" --timeout 10
# aws lambda update-function-configuration --function-name dev-airtext-api-members-get --environment "Variables={TWILIO_ACCOUNT_SID='${TWILIO_ACCOUNT_SID}', TWILIO_AUTH_TOKEN='${TWILIO_AUTH_TOKEN}', MESSAGES_DATABASE_URL='${MESSAGES_DATABASE_URL}'}" --timeout 10
# aws lambda update-function-configuration --function-name dev-airtext-api-members-post --environment "Variables={TWILIO_ACCOUNT_SID='${TWILIO_ACCOUNT_SID}', TWILIO_AUTH_TOKEN='${TWILIO_AUTH_TOKEN}', MESSAGES_DATABASE_URL='${MESSAGES_DATABASE_URL}'}" --timeout 10
# aws lambda update-function-configuration --function-name dev-airtext-api-messages-get --environment "Variables={TWILIO_ACCOUNT_SID='${TWILIO_ACCOUNT_SID}', TWILIO_AUTH_TOKEN='${TWILIO_AUTH_TOKEN}', MESSAGES_DATABASE_URL='${MESSAGES_DATABASE_URL}'}" --timeout 10
aws codebuild start-build --project-name dev-airtext-api-contacts-delete-ecr
aws codebuild start-build --project-name dev-airtext-api-contacts-get-ecr
aws codebuild start-build --project-name dev-airtext-api-contacts-post-ecr
aws codebuild start-build --project-name dev-airtext-api-contacts-put-ecr
aws codebuild start-build --project-name dev-airtext-api-group-contacts-delete-ecr
aws codebuild start-build --project-name dev-airtext-api-group-contacts-get-ecr
aws codebuild start-build --project-name dev-airtext-api-group-contacts-post-ecr
aws codebuild start-build --project-name dev-airtext-api-groups-delete-ecr
aws codebuild start-build --project-name dev-airtext-api-groups-get-ecr
aws codebuild start-build --project-name dev-airtext-api-groups-post-ecr
aws codebuild start-build --project-name dev-airtext-api-members-get-ecr
aws codebuild start-build --project-name dev-airtext-api-members-post-ecr
aws codebuild start-build --project-name dev-airtext-api-messages-get-ecr
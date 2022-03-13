FROM public.ecr.aws/lambda/python:3.8

ARG SLACK_WEBHOOK_URL
ENV SLACK_WEBHOOK_URL=$SLACK_WEBHOOK_URL

CMD ["lambda_function.lambda_handler"]

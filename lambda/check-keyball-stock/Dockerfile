FROM public.ecr.aws/lambda/python:3.8

ARG URL
ENV URL=$URL

ARG LINE_NOTIFY_TOKEN
ENV LINE_NOTIFY_TOKEN=$LINE_NOTIFY_TOKEN

CMD ["lambda_function.lambda_handler"]

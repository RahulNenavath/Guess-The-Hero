FROM public.ecr.aws/lambda/python:3.8

RUN yum install -y gcc gcc-c++ build-essential mono-mcs

# extra lines to install the agent here
RUN curl -O https://lambda-insights-extension.s3-ap-northeast-1.amazonaws.com/amazon_linux/lambda-insights-extension.rpm && \
    rpm -U lambda-insights-extension.rpm && \
    rm -f lambda-insights-extension.rpm

COPY Code/requirements.txt .

RUN /var/lang/bin/python3.8 -m pip install --upgrade pip

RUN pip install --upgrade -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY Code/src/ .
COPY Artifacts/ .
COPY Data/ .

COPY Code/src/app.py ${LAMBDA_TASK_ROOT}

CMD ["app.handler"]
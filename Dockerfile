FROM public.ecr.aws/lambda/python:3.8

RUN yum install -y gcc gcc-c++ build-essential mono-mcs

COPY Code/requirements.txt .

RUN /var/lang/bin/python3.8 -m pip install --upgrade pip

RUN pip install --upgrade -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

RUN python3 -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('all-mpnet-base-v2')" --target "${LAMBDA_TASK_ROOT}"

COPY Code/src/ ${LAMBDA_TASK_ROOT}
COPY Artifacts/ ${LAMBDA_TASK_ROOT}
COPY Data/ ${LAMBDA_TASK_ROOT}

CMD ["app.handler"]
FROM python:3

COPY infava/ pyproject.toml setup.cfg ./

RUN pip install tensorflow keras numpy pandas

CMD [ "python", "-m", "infava" ]
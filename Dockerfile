FROM python:3

COPY favapy/ pyproject.toml setup.cfg ./

RUN pip install tensorflow keras numpy pandas

CMD [ "python", "-m", "favapy" ]
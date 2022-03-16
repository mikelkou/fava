FROM python:3

COPY fava_tool/ pyproject.toml setup.cfg ./

RUN pip install tensorflow keras numpy pandas

CMD [ "python", "-m", "fava_tool" ]
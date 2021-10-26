FROM tensorflow/tensorflow:1.13.2-py3 
COPY . .
COPY ./code .
COPY ./data .
RUN pip install scipy
RUN apt update 
RUN apt install -y git
RUN apt install -yq curl wget jq vim zip
#RUN wget http://modelnet.cs.princeton.edu/ModelNet40.zip
#RUN unzip ModelNet40.zip
#ADD <data_file_name.tar.xz> ./
CMD ["/bin/bash"]

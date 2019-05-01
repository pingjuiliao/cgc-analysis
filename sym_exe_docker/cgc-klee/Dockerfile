FROM klee/klee:latest
RUN apt update
RUN apt install -y git python-pip
RUN apt install -y libc6-dev libc6-dev-i386 gcc-multilib g++-multilib clang cmake
RUN pip install -U pip
RUN pip install xlsxwriter pycrypto
RUN mkdir -p /workdir/angr-workspace
WORKDIR /workdir/angr-workspace
COPY . /workdir/angr-workspace
RUN git clone https://github.com/trailofbits/cb-multios
RUN ./cb-multios/build.sh

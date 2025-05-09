FROM ubuntu:24.04
RUN apt-get update && apt-get install -y curl git
WORKDIR /workspace
RUN curl https://elan.lean-lang.org/elan-init.sh -sSf > install.sh
RUN chmod +x install.sh
RUN ./install.sh -y
ENV PATH="$PATH:/root/.elan/bin/"
RUN git clone https://github.com/leanprover-community/mathematics_in_lean.git
WORKDIR /workspace/mathematics_in_lean
RUN git checkout 6db6c0608c5935d52a8a7f8ac5391e40d517262a
RUN lake exe cache get
RUN lake build

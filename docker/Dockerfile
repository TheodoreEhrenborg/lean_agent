FROM ubuntu:24.04
RUN apt-get update && apt-get install -y curl git
WORKDIR /workspace
RUN curl https://elan.lean-lang.org/elan-init.sh -sSf > install.sh
RUN chmod +x install.sh
RUN ./install.sh -y
RUN git clone https://github.com/leanprover-community/mathematics_in_lean.git
WORKDIR /workspace/mathematics_in_lean
RUN /root/.elan/bin/lake exe cache get
RUN /root/.elan/bin/lake build

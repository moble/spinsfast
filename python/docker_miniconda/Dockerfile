## This container is similar to the official miniconda container, but is based on centos6 so that we
## can use the same commands as in the (centos-based) manylinux1 container, while also supporting
## conda builds on the oldest platform conda supports (centos6).

#FROM continuumio/miniconda

FROM krallin/centos-tini:6

#FROM centos:6

# ### Install tini <https://hub.docker.com/r/krallin/centos-tini/~/dockerfile/>
# RUN TINI_VERSION="v0.13.2" && \
#     TINI_REAL_VERSION="0.13.2" && \
#     TINI_BUILD="/tmp/tini" && \
#     echo "Installing build dependencies" && \
#     TINI_DEPS="gcc cmake make git rpm-build glibc-static curl tar libcap-devel python-devel" && \
#     yum history new || \
#     yum history new && \
#     mv /sbin/weak-modules /sbin/weak-modules.tmp && \
#     yum install --assumeyes ${TINI_DEPS} && \
#     echo "Building Tini" && \
#     git clone https://github.com/krallin/tini.git "${TINI_BUILD}" && \
#     cd "${TINI_BUILD}" && \
#     curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-13.1.2.tar.gz && \
#     tar -xf virtualenv-13.1.2.tar.gz && \
#     mv virtualenv-13.1.2/virtualenv.py virtualenv-13.1.2/virtualenv && \
#     export PATH="${TINI_BUILD}/virtualenv-13.1.2:${PATH}" && \
#     HARDENING_CHECK_PLACEHOLDER="${TINI_BUILD}/hardening-check/hardening-check" && \
#     HARDENING_CHECK_PLACEHOLDER_DIR="$(dirname "${HARDENING_CHECK_PLACEHOLDER}")" && \
#     mkdir "${HARDENING_CHECK_PLACEHOLDER_DIR}" && \
#     echo  "#/bin/sh" > "${HARDENING_CHECK_PLACEHOLDER}" && \
#     chmod +x "${HARDENING_CHECK_PLACEHOLDER}" && \
#     export PATH="${PATH}:${HARDENING_CHECK_PLACEHOLDER_DIR}" && \
#     git checkout "${TINI_VERSION}" && \
#     export SOURCE_DIR="${TINI_BUILD}" && \
#     export BUILD_DIR="${TINI_BUILD}" && \
#     export ARCH_NATIVE=1 && \
#     "${TINI_BUILD}/ci/run_build.sh" && \
#     echo "Installing Tini" && \
#     yum install -y "${TINI_BUILD}/tini_${TINI_REAL_VERSION}.rpm" && \
#     echo "Cleaning up" && \
#     cd / && \
#     rm -rf "${TINI_BUILD}" && \
#     yum --assumeyes history undo 1 && \
#     yum clean all && \
#     mv /sbin/weak-modules.tmp /sbin/weak-modules && \
#     echo "Symlinkng to /usr/local/bin" && \
#     ln -s /usr/bin/tini        /usr/local/bin/tini && \
#     ln -s /usr/bin/tini-static /usr/local/bin/tini-static && \
#     echo "Running Smoke Test" && \
#     /usr/bin/tini -- ls && \
#     /usr/bin/tini-static -- ls && \
#     /usr/local/bin/tini -- ls && \
#     /usr/local/bin/tini-static -- ls && \
#     echo "Done"


### Install miniconda2 <https://hub.docker.com/r/continuumio/miniconda/~/dockerfile/>
RUN yum install -y wget bzip2 git curl grep sed dpkg && \
    echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh
ENV PATH /opt/conda/bin:$PATH


### Create several basic conda envs
ENV PYTHON_VERSIONS="2.7 3.4 3.5 3.6"
RUN for PYTHON_VERSION in ${PYTHON_VERSIONS}; do \
        conda create -y -q -n "py${PYTHON_VERSION}" python="${PYTHON_VERSION}" ${conda_packages}; \
        done && \
    conda clean -y -a && \
    mkdir -p /code && \
    conda install -y -q -n root conda-build anaconda-client
COPY build.sh /root/


### Start up as in miniconda2
ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]

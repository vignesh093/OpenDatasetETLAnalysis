
FROM ubuntu:latest AS trino-builder
ARG TRINO_VERSION=460
RUN apt update -y 
RUN apt -y install wget && apt-get install -y curl
RUN wget https://repo1.maven.org/maven2/io/trino/trino-server/460/trino-server-${TRINO_VERSION}.tar.gz 
RUN tar -zxf trino-* -C /opt&& \
    rm trino-*.tar.gz
RUN mv /opt/trino-server-${TRINO_VERSION} /opt/trino


FROM ubuntu:latest 
ARG TRINO_VERSION=460
RUN apt update -y && apt-get install -y python3 && apt-get install -y net-tools && apt -y install wget
RUN wget https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz && \
tar -xzf openjdk-22.0.2_linux-x64_bin.tar.gz -C /opt/ && \
    rm openjdk-22.0.2_linux-x64_bin.tar.gz

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/opt/jdk-22.0.2
ENV PATH="${JAVA_HOME}/bin:${PATH}"

RUN ln -s /usr/bin/python3 /usr/bin/python
COPY --from=trino-builder /opt/trino /opt/trino


RUN wget https://repo1.maven.org/maven2/io/trino/trino-cli/${TRINO_VERSION}/trino-cli-${TRINO_VERSION}-executable.jar
RUN mv trino-cli-${TRINO_VERSION}-executable.jar /usr/local/bin/trino-cli.jar
RUN chmod +x /usr/local/bin/trino-cli.jar
RUN ln -s /usr/local/bin/trino-cli.jar /usr/local/bin/trino

RUN mkdir -p /var/trino/data
RUN mkdir -p /var/trino/etc
RUN mkdir -p /etc/trino

#COPY coordinator-config.properties /opt/trino/etc/config.properties
#COPY jvm.config /opt/trino/etc/jvm.config
#COPY node.properties /opt/trino/etc/node.properties

WORKDIR /opt/trino
RUN useradd -m -U -u 1001 user
#RUN chown -R user:user /opt/trino
RUN chmod 755 /opt/trino
RUN chown -R user:user /var/trino
RUN chmod 755 /var/trino
RUN chown -R user:user /etc/trino
RUN chmod 755 /etc/trino
USER user

CMD ["sh", "-c", "bin/launcher run && tail -f /dev/null"]
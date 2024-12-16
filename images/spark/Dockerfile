# taking a Linux OS like Ubuntu or Alpine as the base image

FROM maven:3.8-eclipse-temurin-17-alpine AS dependency-builder
COPY pom.xml pom.xml
RUN mvn dependency:copy-dependencies -DoutputDirectory=/tmp/dependencies


FROM ubuntu:latest AS spark-builder
ARG SPARK_VERSION=3.5.1
RUN apt update -y
RUN apt -y install wget
# install Spark dependencies
# installing the Spark binaries, untar and move them
RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz 
RUN tar -zxf spark-* -C /opt&& \
    rm spark-*.tgz
RUN mv /opt/spark-3.5.1-bin-hadoop3 /opt/spark



FROM ubuntu:latest 
RUN apt update -y && apt-get install -y python3-pip
RUN apt -y install openjdk-11-jdk 
RUN apt -y install scala

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      sudo \
      curl \
      vim \
      unzip

ARG SPARK_MAJOR_VERSION=3.5
ARG ICEBERG_VERSION=1.7.1
ARG ICEBERG_SPARK_SCALA="iceberg-spark-runtime-${SPARK_MAJOR_VERSION}_2.12"
ARG JAR_PACKAGE="${ICEBERG_SPARK_SCALA}-${ICEBERG_VERSION}.jar"

COPY --from=spark-builder /opt/spark /opt/spark

RUN chmod 755 /opt/spark

# Download the Iceberg Spark runtime JAR
RUN curl -Lo /opt/spark/jars/${JAR_PACKAGE} \
    https://repo1.maven.org/maven2/org/apache/iceberg/${ICEBERG_SPARK_SCALA}/${ICEBERG_VERSION}/${JAR_PACKAGE}

# Download the Iceberg AWS bundle JAR
RUN curl -s -Lo /opt/spark/jars/iceberg-aws-bundle-${ICEBERG_VERSION}.jar \
    https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-aws-bundle/${ICEBERG_VERSION}/iceberg-aws-bundle-${ICEBERG_VERSION}.jar

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
 && unzip awscliv2.zip \
 && sudo ./aws/install \
 && rm awscliv2.zip \
 && rm -rf aws/


# Install PostgreSQL JDBC Driver
RUN curl "https://jdbc.postgresql.org/download/postgresql-42.6.0.jar" -o "postgresql-42.6.0.jar" \
    && mv postgresql-42.6.0.jar "/opt/spark/jars/postgresql-42.6.0.jar"


COPY --from=dependency-builder /tmp/dependencies/* /opt/spark/jars/

RUN mkdir -p /opt/spark/conf
RUN mkdir -p /user/hive/warehouse
COPY spark-defaults.conf /opt/spark/conf/

RUN mkdir -p /opt/spark/log/app_log/
RUN mkdir -p /opt/spark/logs/

WORKDIR /opt/spark
ENV SPARK_HOME=/opt/spark
# define environmental variables
RUN useradd -m -U -u 1001 user
RUN chown -R user:user /opt/spark
RUN chmod 755 /opt/spark
RUN chmod +x /opt/spark/bin/spark-class
USER user
CMD ["sh", "-c", "tail -f /dev/null"]

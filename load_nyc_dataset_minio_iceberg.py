from pyspark.sql import SparkSession
import logging
from pyspark.sql.functions import col, to_date
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, TimestampType, DoubleType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

spark = SparkSession.builder.appName("LoadNYCTaxiData").getOrCreate()


schema = StructType([
        StructField("vendorid", IntegerType(), True),
        StructField("tpep_pickup_datetime", TimestampType(), True),
        StructField("tpep_dropoff_datetime", TimestampType(), True),
        StructField("passenger_count", IntegerType(), True),
        StructField("trip_distance", DoubleType(), True),
        StructField("pickup_longitude", DoubleType(), True),
        StructField("pickup_latitude", DoubleType(), True),
        StructField("ratecodeid", IntegerType(), True),
        StructField("store_and_fwd_flag", StringType(), True),
        StructField("dropoff_longitude", DoubleType(), True),
        StructField("dropoff_latitude", DoubleType(), True),
        StructField("payment_type", IntegerType(), True),
        StructField("fare_amount", DoubleType(), True),
        StructField("extra", DoubleType(), True),
        StructField("mta_tax", DoubleType(), True),
        StructField("tip_amount", DoubleType(), True),
        StructField("tolls_amount", DoubleType(), True),
        StructField("improvement_surcharge", DoubleType(), True),
        StructField("total_amount", DoubleType(), True)
])

minio_input_path = "s3a://nyc/yellow_tripdata_2016-01.csv"
try:
    input_df = spark.read.format("csv").option("header","true").schema(schema).load(minio_input_path)

    input_df = input_df.withColumn("tpep_date", to_date(col("tpep_pickup_datetime")))
    input_df.show()
    logger.info(f"Reading from CSV file in minio bucket {minio_input_path}")

    sort_df = input_df.sort("tpep_date")
    sort_df.write.partitionBy("tpep_date").mode("overwrite").saveAsTable("nyc.yellow_taxi_trips")


except Exception as e:
    logger.error("An occur occurred during the read from minio and write to iceberg etl pipeline: {e}", exc_info=True)

finally:
    spark.stop()


import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StringType, TimestampType

spark_version = pyspark.__version__
kafka_package = f"org.apache.spark:spark-sql-kafka-0-10_2.13:{spark_version}"

spark = (
    SparkSession.builder.
    appName('AdTech_SpeedLayer').
    config("spark.jars.packages", kafka_package).
    getOrCreate()
)

schema = (
    StructType().
    add("event_id", StringType()).
    add("campaign_id", StringType()).
    add("event_type", StringType()).
    add("timestamp", TimestampType())
)

raw_stream = (
    spark.readStream.
    format("kafka").
    option("kafka.bootstrap.servers", "localhost:9092").
    option("subscribe", "ad_events_topic").
    load()
)

parsed_stream = raw_stream.select(
    from_json(col('value').cast("string"), schema).alias('data')
    ).select("data.*")

watermarked_stream = parsed_stream.withWatermark("timestamp", "1 minute")

realtime_agg = (
    watermarked_stream.
    groupBy(
        window(col("timestamp"), "5 minutes", "1 minute"),
        col("campaign_id"),
        col("event_type")
    ).count()
)

query = realtime_agg.writeStream.outputMode("update").format("console").start()
query.awaitTermination()

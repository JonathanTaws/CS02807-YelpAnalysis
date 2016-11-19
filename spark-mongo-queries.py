from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession.builder.master("local").appName("YelpQueries").getOrCreate()

    # Load the data
    df = spark.read.format("com.mongodb.spark.sql").load()
    df.registerTempTable("business")

    collection_businesses = spark.sql(
        "SELECT stars, review_count, name FROM business ORDER BY stars DESC, review_count DESC LIMIT 10"
    )
    print("TOP 10 business:")
    collection_businesses.show()

    collection_states = spark.sql(
        "SELECT AVG(stars) AS stars, state FROM business GROUP BY state ORDER BY stars DESC"
    )

    print("Average of stars by state:")
    collection_states.show()

    spark.stop()
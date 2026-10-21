# PySpark Interview Questions and Answers

## Q1: What is PySpark?
**A:** PySpark is the Python API for Apache Spark, a unified analytics engine for large-scale distributed data processing. It provides Python bindings for Spark's core functionality: Spark SQL (DataFrames), Spark Streaming, MLlib (machine learning), and GraphX (graph processing). PySpark enables Python developers to write distributed data processing applications using familiar Pandas-like syntax.

## Q2: What is Apache Spark?
**A:** Apache Spark is an open-source, distributed computing system for big data processing. It provides in-memory computation (much faster than MapReduce), supports multiple languages (Python, Scala, Java, R), and offers libraries for SQL, streaming, ML, and graph processing. Spark runs on clusters managed by YARN, Kubernetes, Mesos, or in standalone mode.

## Q3: What is the difference between Spark and Hadoop MapReduce?
**A:** Spark processes data in-memory (with disk spill when needed), while MapReduce writes intermediate results to disk between each stage. Spark can be 10-100x faster for iterative algorithms and interactive queries. Spark provides higher-level APIs (DataFrames, Datasets) and unified libraries, while MapReduce is lower-level and harder to use.

## Q4: What are the key components of Spark?
**A:** Core components: 1) Spark Core — task scheduling, memory management, fault recovery, 2) Spark SQL — structured data processing with DataFrames/Datasets, 3) Spark Streaming — real-time stream processing, 4) MLlib — distributed machine learning, 5) GraphX — graph computation, 6) Structured Streaming — stream processing on DataFrames.

## Q5: What is a SparkSession?
**A:** SparkSession is the unified entry point for all Spark functionality (replaced SparkContext, SQLContext, HiveContext in Spark 2.0+). Created via: spark = SparkSession.builder.appName("MyApp").config("spark.some.config", "value").getOrCreate(). It provides access to DataFrame API, SQL queries, streaming, and catalog operations.

## Q6: What is a SparkContext?
**A:** SparkContext is the original entry point (Spark 1.x) for Spark functionality. In Spark 2.0+, SparkSession wraps SparkContext. Access via spark.sparkContext. It handles: cluster connection, resource allocation, job scheduling, and configuration. Still used for RDD operations and accumulator/broadcast variables.

## Q7: What is the difference between RDD, DataFrame, and Dataset?
**A:** RDD (Resilient Distributed Dataset): low-level, untyped, no schema, no optimization (Catalyst/Tungsten). DataFrame: structured, schema-based, optimized via Catalyst optimizer, distributed collection of Row objects. Dataset: type-safe (JVM only), combines RDD's type safety with DataFrame's optimization. PySpark uses DataFrames (RDDs are legacy).

## Q8: What is an RDD?
**A:** RDD (Resilient Distributed Dataset) is the fundamental data structure in Spark — an immutable, partitioned collection of records that can be processed in parallel. Characteristics: resilient (can be rebuilt from lineage on failure), distributed (partitioned across cluster), and lazy (transformations are deferred). Created from data sources or by transforming existing RDDs.

## Q9: What are the two types of RDD operations?
**A:** Transformations (lazy): return a new RDD — map, filter, flatMap, distinct, reduceByKey, sortByKey, join, union. Actions (eager): return a result or write to storage — collect, count, take, reduce, foreach, saveAsTextFile, countByKey. Transformations are lazy (computed only when an action triggers them).

## Q10: What is lazy evaluation in Spark?
**A:** Lazy evaluation means transformations are not executed immediately — Spark builds a DAG (Directed Acyclic Graph) of transformations. Execution happens only when an action is called (count, collect, save). Benefits: Spark can optimize the execution plan (query optimization, pipelining), reduce shuffles, and prune unnecessary computations.

## Q11: What is a Spark DataFrame?
**A:** A DataFrame is a distributed collection of rows organized into named columns, similar to a Pandas DataFrame or SQL table. Built on top of RDDs with schema information. Supports: SQL queries, built-in optimizations (Catalyst optimizer), efficient storage (Tungsten binary format), and rich API (select, filter, groupBy, join, agg).

## Q12: How do you create a DataFrame in PySpark?
**A:** From CSV: spark.read.csv("file.csv", header=True, inferSchema=True). From JSON: spark.read.json("file.json"). From Parquet: spark.read.parquet("file.parquet"). From list: spark.createDataFrame([(1, "a"), (2, "b")], ["id", "name"]). From SQL: spark.sql("SELECT * FROM table"). From Pandas: spark.createDataFrame(pd_df).

## Q13: What is the difference between Spark DataFrame and Pandas DataFrame?
**A:** Spark DataFrames: distributed across cluster, lazy evaluation, immutable, optimized via Catalyst, handles terabytes, limited mutability (no in-place operations). Pandas DataFrames: single machine, eager evaluation, mutable, no optimizer, handles memory-sized data, rich in-place operations. Convert via toPandas() and createDataFrame().

## Q14: What is the Catalyst optimizer?
**A:** Catalyst is Spark SQL's query optimizer that transforms a logical plan into an optimized physical plan. Phases: 1) Analysis (resolve column references), 2) Logical optimization (predicate pushdown, constant folding), 3) Physical planning (select join strategy), 4) Code generation (generate efficient Java bytecode). Enables performance comparable to hand-optimized code.

## Q15: What is Tungsten?
**A:** Tungsten is Spark's performance engine that improves CPU and memory efficiency. Features: 1) Off-heap memory management (binary format, cache-aware), 2) Cache-aware computation (optimize for L1/L2/L3 caches), 3) Whole-stage code generation (eliminate virtual function calls), 4) Fast hash-based shuffles. Tungsten makes Spark competitive with C++/C# speeds.

## Q16: What are partitions in Spark?
**A:** Partitions are the unit of parallelism in Spark — each partition is processed by one task on one core. DataFrames/RDDs are split across partitions. Default: number of CPU cores * ~2-4. Repartitioning: df.repartition(n) (full shuffle, increase/decrease), df.coalesce(n) (merge, no full shuffle). Optimal partitioning improves parallelism and reduces skew.

## Q17: What is a shuffle in Spark?
**A:** A shuffle is the process of redistributing data across partitions, causing data to move between executors. Triggered by: groupBy, reduceByKey, join, distinct, repartition, coalesce (some cases). Shuffles are expensive (network I/O, disk I/O, serialization). Minimize shuffles by: using reduceByKey over groupByKey, appropriate partitioning, and broadcast joins.

## Q18: What is the difference between groupByKey and reduceByKey?
**A:** reduceByKey(f) merges values per key before shuffling (combines locally, then shuffles partial results). groupByKey shuffles ALL key-value pairs without pre-aggregation. reduceByKey has much less network traffic. Always prefer reduceByKey over groupByKey for associative/reductive operations. Use aggregateByKey or combineByKey for different result types.

## Q19: What is a broadcast variable?
**A:** A broadcast variable caches a read-only value on each executor rather than shipping it with tasks. Used for: lookup tables, small reference datasets, ML models. Created: broadcast_var = spark.sparkContext.broadcast(large_dict). Accessed: broadcast_var.value. Benefits: eliminates sending the same data multiple times, reduces serialization overhead.

## Q20: What is an accumulator?
**A:** An accumulator is a shared variable that only supports addition (aggregation). Used for counters and sums across tasks. Created: counter = spark.sparkContext.accumulator(0). Updated in tasks: counter.add(1). Read in driver: counter.value. Only the driver can read; tasks can only add. Useful for: counting errors, tracking progress.

## Q21: How do you handle missing values in PySpark DataFrames?
**A:** Drop: df.dropna(thresh=3) (rows with at least 3 non-null), df.dropna(subset=["col"]). Fill: df.fillna({"col1": 0, "col2": "unknown"}), df.fillna(method="ffill"). Replace: df.replace(["old"], ["new"]), df.na.replace(). Dropping is simplest; filling is better when data loss is unacceptable.

## Q22: How do you filter data in PySpark?
**A:** df.filter(df.col > 5). df.where(df.col == "value"). df.filter("col > 5 AND col2 = 'x'"). Multiple conditions: df.filter((df.col1 > 5) & (df.col2 == "x")) (use &, |, ~ instead of and, or, not). df.filter(df.col.isin(["a", "b"])). df.filter(df.col.startswith("prefix")).

## Q23: How do you select and rename columns?
**A:** Select: df.select("col1", "col2"), df.select(df.col1, df.col2.alias("new_name")). Rename: df.withColumnRenamed("old", "new"). Multiple: df.selectExpr("col1 as new1", "col2 * 2 as doubled"). Column operations: df.select(df.col.cast("int"), df.col.substr(0, 3)). Column order: df.select("b", "a") reorders.

## Q24: How do you add and modify columns?
**A:** df.withColumn("new_col", df.col1 + df.col2). df.withColumn("category", when(df.age > 18, "adult").otherwise("child")). df.withColumn("price_discounted", df.price * 0.9). df.withColumn("id_str", df.id.cast("string")). Multiple columns: reduce(lambda df, col: df.withColumn(col, ...), ["col1", "col2"], df). Avoid chaining too many withColumn calls (performance).

## Q25: How do you drop columns?
**A:** df.drop("col1"). df.drop("col1", "col2"). df.drop(df.col1). Multiple: df.drop(*["col1", "col2"]). To drop all except: df.select(*[c for c in df.columns if c not in ["drop1", "drop2"]]).

## Q26: How do you aggregate data in PySpark?
**A:** Simple: df.select(avg("col"), sum("col"), count("col"), min("col"), max("col")). Grouped: df.groupBy("category").agg(avg("value"), sum("value"), count("id")). Multi-aggregate: df.groupBy("cat").agg({"val": "mean", "id": "count"}). Named: df.groupBy("cat").agg(avg_val=avg("val"), cnt=count("id")).

## Q27: What aggregate functions are available?
**A:** Built-in: avg, sum, count, min, max, stddev, variance, collect_list, collect_set, countDistinct, approx_count_distinct, skewness, kurtosis, corr, covar_samp, covar_pop. Window function aggregates: row_number, rank, dense_rank, lag, lead, ntile, first_value, last_value.

## Q28: How do you join DataFrames in PySpark?
**A:** df1.join(df2, on="key", how="inner"). df1.join(df2, on=df1.key == df2.key, how="left"). Join types: inner, left, right, outer, left_semi, left_anti, cross. Different keys: df1.join(df2, df1.key1 == df2.key2). Multiple keys: join condition with &.

## Q29: What is a broadcast join?
**A:** A broadcast join sends a small DataFrame to all executors, avoiding a full shuffle. Use when one DataFrame is small (< 10MB default, configurable via spark.sql.autoBroadcastJoinThreshold). Enable: df1.join(broadcast(df2), "key"). Benefits: significantly faster than sort-merge joins for small/large table joins.

## Q30: What is the difference between sort-merge join and hash join?
**A:** Sort-merge join: sorts both sides by join key, then merges. Used for large-large joins. Hash join: builds a hash table of one side, probes with the other. Used when one side fits in memory. Spark automatically chooses the join strategy based on data size estimates. Broadcast join is a specialized hash join for small tables.

## Q31: How do you handle data skew in joins?
**A:** Skew occurs when some keys have significantly more data, causing executor overload. Solutions: 1) Salting — add random prefix to skewed keys, 2) Broadcast join — if one side is small, 3) Increase shuffle partitions — spark.sql.shuffle.partitions, 4) Skew join optimization — spark.sql.adaptive.skewJoin.enabled (Spark 3.0+), 5) Filter skewed keys and handle separately.

## Q32: What is Adaptive Query Execution (AQE)?
**A:** AQE (Spark 3.0+) re-optimizes the query plan at runtime based on intermediate results. Features: 1) Dynamic partition coalescing — reduce partitions after filtering, 2) Dynamic join selection — switch to broadcast join if table is smaller than expected, 3) Dynamic skew join optimization — handle skewed keys. Enable: spark.sql.adaptive.enabled=true.

## Q33: What is Spark SQL?
**A:** Spark SQL allows querying structured data using SQL queries. Tables can be registered as temporary views: df.createOrReplaceTempView("my_table"). Query: spark.sql("SELECT category, AVG(value) FROM my_table GROUP BY category"). Spark SQL supports: joins, subqueries, window functions, UDFs, and SQL:2003 standard.

## Q34: What is the difference between createOrReplaceTempView and createGlobalTempView?
**A:** createOrReplaceTempView creates a temporary view scoped to the current SparkSession — invisible to other sessions. createGlobalTempView creates a global temporary view visible across all SparkSessions within the same application, stored in the global_temp database. Access: spark.sql("SELECT * FROM global_temp.my_view").

## Q35: How do you write UDFs (User Defined Functions) in PySpark?
**A:** from pyspark.sql.functions import udf; from pyspark.sql.types import IntegerType; my_udf = udf(lambda x: len(x), IntegerType()); df.withColumn("len", my_udf(df.col)). For performance: use Pandas UDFs (vectorized) with @pandas_udf decorator. UDFs are slower than built-in functions — avoid when possible.

## Q36: What are Pandas UDFs (Vectorized UDFs)?
**A:** Pandas UDFs (using Apache Arrow) process batches of data instead of individual rows. Decorated with @pandas_udf, they work on Pandas Series/DataFrames. Types: Scalar (Series in, Series out), Grouped Map (groupBy + apply), Grouped Aggregate, Window. Much faster than row-by-row UDFs due to vectorization and Arrow serialization.

## Q37: What is the difference between UDF and Pandas UDF?
**A:** Regular UDF: row-by-row processing, Python serialization per row, slow. Pandas UDF: batch processing via Arrow, vectorized operations, 10-100x faster. Pandas UDFs have higher initialization cost but are better for complex operations on large data. Use built-in Spark functions first, then Pandas UDFs, then regular UDFs.

## Q38: How do you read/write data in different formats?
**A:** CSV: spark.read.csv("path", header=True, inferSchema=True); df.write.csv("path", header=True, mode="overwrite"). JSON: spark.read.json("path"); df.write.json("path"). Parquet: spark.read.parquet("path"); df.write.parquet("path"). Parquet is recommended (columnar, compressed, schema-preserving).

## Q39: What is Parquet and why use it?
**A:** Parquet is a columnar storage format optimized for analytics. Benefits: 1) Columnar storage (reads only needed columns), 2) Compression (snappy, gzip, zstd), 3) Schema preservation, 4) Predicate pushdown (filter at storage level), 5) Splittable for parallel reading. Parquet is the default format for Spark and preferred over CSV/JSON for production.

## Q40: What is Delta Lake?
**A:** Delta Lake is an open-source storage layer that adds ACID transactions, schema enforcement, time travel (data versioning), and unified batch/streaming to data lakes built on Parquet. Features: atomic commits, rollback, schema evolution, vacuum (cleanup old versions), and Delta Sharing. Created by Databricks, now open-source (Linux Foundation).

## Q41: How do you optimize Spark jobs?
**A:** Key optimizations: 1) Proper partitioning (match partition count to cluster resources), 2) Column pruning (select only needed columns), 3) Predicate pushdown (filter early), 4) Broadcast joins for small tables, 5) Avoid shuffles (use reduceByKey over groupByKey), 6) Cache intermediate DataFrames reused multiple times, 7) Serialize with Kryo.

## Q42: What is the spark.sql.shuffle.partitions setting?
**A:** This configures the number of partitions used during shuffles (default 200). Too few: large partitions, memory pressure, slow. Too many: small partitions, task overhead, scheduling latency. Tune based on data size: target 100-200MB per partition after shuffle. For large data: increase (e.g., 500-1000). For streaming: reduce (e.g., 10-50).

## Q43: How do you cache/persist DataFrames?
**A:** df.cache() — default storage level (MEMORY_AND_DISK). df.persist(StorageLevel.MEMORY_ONLY) — various levels. df.unpersist() — remove from cache. Storage levels: MEMORY_ONLY, MEMORY_AND_DISK, DISK_ONLY, MEMORY_ONLY_SER, MEMORY_AND_DISK_SER, OFF_HEAP. Cache when: DataFrame is reused multiple times, computation is expensive.

## Q44: What is the difference between cache and persist?
**A:** cache() is shorthand for persist(StorageLevel.MEMORY_AND_DISK). persist() allows specifying the storage level. Both keep data in memory/disk after the first action. Use persist when you need a specific storage strategy (e.g., MEMORY_ONLY_SER for memory-constrained, DISK_ONLY for spilling).

## Q45: What is checkpointing in Spark?
**A:** Checkpointing saves an RDD/DataFrame to a reliable storage (HDFS, S3) and truncates its lineage graph. Used for: breaking long lineage chains (avoids StackOverflowError), making data fault-tolerant (loss persist safely), and improving recomputation time. Use: spark.sparkContext.setCheckpointDir("/path"); df.checkpoint().

## Q46: How do you handle schema inference?
**A:** When reading CSV: spark.read.csv("file.csv", header=True, inferSchema=True). Inference samples rows to determine data types. For production: define schema explicitly: from pyspark.sql.types import StructType, StructField, StringType, IntegerType; schema = StructType([StructField("name", StringType(), True)]). Explicit schema is faster and more reliable.

## Q47: What is a StructType and StructField?
**A:** StructType defines the schema of a DataFrame — a collection of StructFields. StructField defines a column: name, data type (StringType, IntegerType, FloatType, etc.), nullable (True/False). Nested types: ArrayType, MapType, StructType (for nested columns). Example: StructType([StructField("id", IntegerType()), StructField("name", StringType())]).

## Q48: How do you handle complex nested data (JSON)?
**A:** Read nested JSON: df = spark.read.json("nested.json"); df.printSchema(). Access nested fields: df.select("address.city"), df.select(df["address.zip"]). Explode arrays: df.select(explode(df.items).alias("item")). Nested struct: df.select(struct("col1", "col2").alias("nested")). Use from_json for parsing JSON strings.

## Q49: How do you work with arrays in PySpark?
**A:** Array functions: explode (array to rows), collect_list (rows to array), array_contains, size, array_distinct, array_intersect, array_union, sort_array, reverse, slice. Create: array("col1", "col2"). Index: df.select(df.arr_col[0]). Use arrays for: preserving list structure, reducing join complexity.

## Q50: How do you work with dates and timestamps?
**A:** Functions: current_date(), current_timestamp(), date_add, date_sub, datediff, months_between, add_months, last_day, next_day, trunc, date_trunc, to_date, to_timestamp, year, month, day, hour, minute, second, weekofyear, quarter, dayofweek, dayofyear. Format: date_format(df.date_col, "yyyy-MM-dd").

## Q51: What is Spark Streaming?
**A:** Spark Streaming processes real-time data streams using micro-batching (discretized streams). Data is divided into small batches (e.g., 1 second), processed like batch DataFrames. Sources: Kafka, Kinesis, file systems, sockets. Sinks: console, files, databases, Kafka. Structured Streaming (preferred) provides DataFrame API for streaming.

## Q52: What is Structured Streaming?
**A:** Structured Streaming (Spark 2.0+) provides stream processing using the DataFrame/Dataset API. Key concepts: 1) Input source (readStream), 2) Streaming DataFrame (continuous, unbounded), 3) Output sink (writeStream), 4) Output modes (append, complete, update). Supports exactly-once semantics via checkpointing and WAL (Write-Ahead Log).

## Q53: What are output modes in Structured Streaming?
**A:** Append: only new rows written — no modifications to existing results. Complete: full result written each trigger (required for aggregations without watermark). Update: only updated rows written (since last trigger). Append is most efficient; Complete can be expensive for large aggregations.

## Q54: What is a watermark in Structured Streaming?
**A:** A watermark defines the maximum lateness allowed for late-arriving data. df.withWatermark("timestamp", "10 minutes"). Data older than the watermark is considered too late and dropped. Watermarks enable state cleanup for aggregations and limit state size. Required for handling late data in append/update output modes.

## Q55: How do you connect PySpark to Kafka?
**A:** Read: df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "host:9092").option("subscribe", "topic").load(). Parse: df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)"). Write: df.writeStream.format("kafka").option("topic", "output").option("checkpointLocation", "/checkpoint").start().

## Q56: What is MLlib in Spark?
**A:** MLlib is Spark's distributed machine learning library. It provides: feature engineering (VectorAssembler, StringIndexer, OneHotEncoder), classification (LogisticRegression, RandomForest, GBT), regression, clustering (KMeans, LDA), recommendation (ALS), and pipelines (Pipeline, cross-validation). Algorithms scale to large datasets via distributed computation.

## Q57: What is a Pipeline in MLlib?
**A:** A Pipeline chains multiple Transformers and Estimators into a ML workflow. pipeline = Pipeline(stages=[StringIndexer(inputCol="cat", outputCol="cat_idx"), VectorAssembler(inputCols=["feat1", "feat2"], outputCol="features"), RandomForestClassifier()]). pipeline.fit(train_df). Pipeline ensures consistent preprocessing across train and test.

## Q58: What is a Transformer vs Estimator in MLlib?
**A:** Transformer: transforms one DataFrame into another (has transform() method). Examples: StringIndexerModel, VectorAssembler, trained model. Estimator: learns from data and produces a Transformer (has fit() method). Examples: StringIndexer, RandomForestClassifier, KMeans. Pipeline stages combine both types.

## Q59: How do you evaluate models in MLlib?
**A:** Classification: BinaryClassificationEvaluator (AUC, areaUnderROC), MulticlassClassificationEvaluator (f1, accuracy, precision, recall). Regression: RegressionEvaluator (rmse, mae, r2). Evaluation: evaluator.evaluate(predictions). Cross-validation: CrossValidator(estimator, evaluator, paramGrid, numFolds=3) for hyperparameter tuning.

## Q60: What is ALS in MLlib?
**A:** ALS (Alternating Least Squares) is a collaborative filtering algorithm for recommendation systems. Usage: als = ALS(userCol="userId", itemCol="movieId", ratingCol="rating", coldStartStrategy="drop"); model = als.fit(train); predictions = model.transform(test). Handles implicit feedback, regularization, and cold-start.

## Q61: How do you handle categorical features in MLlib?
**A:** StringIndexer: converts string categories to numeric indices (0, 1, 2...). OneHotEncoder: converts indices to binary vectors (avoids ordinal assumptions). VectorIndexer: identifies categorical features in vector data. Use Pipeline to chain: StringIndexer → OneHotEncoder → VectorAssembler.

## Q62: What is VectorAssembler?
**A:** VectorAssembler combines multiple numeric columns into a single feature vector column. Required before most MLlib algorithms. Example: assembler = VectorAssembler(inputCols=["age", "income", "score"], outputCol="features"). Inputs can be numeric, boolean, or vector columns. Output is a DenseVector or SparseVector.

## Q63: How do you handle imbalanced data in MLlib?
**A:** Techniques: 1) classWeight parameter in classifiers (LogisticRegression, RandomForest), 2) Sampling — sampleBy for stratified sampling, 3) Custom weighting in loss functions, 4) Ensemble methods (RandomForest handles imbalance better), 5) Evaluation with AUC/PR instead of accuracy.

## Q64: What is the difference between Spark MLlib and scikit-learn?
**A:** MLlib: distributed (handles terabytes), integrates with Spark pipeline, limited algorithm selection, less mature feature engineering. scikit-learn: single machine (memory-bound), richer algorithm selection, more feature extraction options, easier prototyping. Use MLlib for large-scale data; scikit-learn for smaller datasets and research.

## Q65: How do you handle large-scale feature engineering in PySpark?
**A:** Use built-in functions: when/otherwise, regexp_extract, split, array functions, date functions. Window functions for rolling features. Bucketing: bucketizer = Bucketizer(splits=[0, 18, 65, 100], inputCol="age", outputCol="age_group"). QuantileDiscretizer for equal-frequency bins. MinMaxScaler, StandardScaler for normalization.

## Q66: What is Spark's execution model?
**A:** 1) Driver program (your PySpark script) creates SparkContext, 2) Driver creates DAG of stages, 3) DAG Scheduler splits into stages (based on shuffle boundaries), 4) Task Scheduler dispatches tasks to executors, 5) Executors run tasks on data partitions, 6) Results returned to driver. Executors are JVM processes on worker nodes.

## Q67: What is a DAG in Spark?
**A:** DAG (Directed Acyclic Graph) represents the logical execution plan. Spark builds a DAG of RDD transformations. When an action is called, the DAG Scheduler: 1) Analyzes the DAG, 2) Identifies stages (groups of transformations without shuffles), 3) Packs stages into tasks, 4) Submits tasks to executors. DAG allows optimizations like pipelining.

## Q68: What is a stage in Spark?
**A:** A stage is a set of parallel tasks that can be executed without shuffling. Stages are separated by shuffle boundaries (wide dependencies). Narrow transformations (map, filter) stay in same stage. Wide transformations (reduceByKey, repartition) create new stages. Each stage has tasks equal to number of partitions.

## Q69: What is a task in Spark?
**A:** A task is the smallest unit of work in Spark — one task processes one partition on one executor core. Tasks run in parallel across cluster. A stage has as many tasks as partitions. Task failure: Spark re-schedules the task on a different executor (up to spark.task.maxFailures times, default 4).

## Q70: How does Spark achieve fault tolerance?
**A:** RDDs track lineage (the sequence of transformations used to build them). If a partition is lost (executor failure), Spark recomputes it from the original source using lineage. Checkpointing truncates lineage for long chains. Data replication (replicate RDDs) provides additional fault tolerance.

## Q71: What is the Spark UI?
**A:** Spark UI is a web interface (default port 4040) for monitoring Spark applications. Tabs: Jobs (DAG visualization, job status), Stages (stage details, task metrics, shuffle read/write), Storage (cached RDDs/DataFrames), Environment (configuration), Executors (resource usage, logs), SQL (SQL query plans, metrics).

## Q72: How do you debug Spark performance issues in the UI?
**A:** Check: 1) Job tab — long-running stages, 2) Stage tab — task time distribution (skew if some tasks much slower), 3) Shuffle Read/Write metrics (excessive shuffle suggests suboptimal join/groupBy), 4) Storage tab — cache usage, 5) Executors tab — GC time, memory usage, 6) SQL tab — physical plan for optimization opportunities.

## Q73: How do you configure Spark memory?
**A:** Key configs: spark.executor.memory (heap per executor, e.g., 4g), spark.driver.memory (driver heap), spark.memory.offHeap.enabled=true + spark.memory.offHeap.size (off-heap), spark.memory.fraction (fraction for execution+storage, default 0.6), spark.memory.storageFraction (storage fraction within memory pool, default 0.5).

## Q74: What is the difference between spark.executor.memory and spark.memory.offHeap.size?
**A:** spark.executor.memory is the JVM heap size for each executor — used by Java objects, execution memory, storage cache. spark.memory.offHeap.size is native memory outside the JVM — used by Tungsten for efficient binary processing, bypassing GC overhead. Off-heap reduces GC pauses and can improve performance.

## Q75: How do you tune Spark for better performance?
**A:** Key areas: 1) Partitioning — match partition count to cluster (2-3x cores), 2) Shuffle — reduce with broadcast joins, pre-aggregation, 3) Memory — allocate sufficient executor memory, enable off-heap, 4) Serialization — use Kryo (spark.serializer=org.apache.spark.serializer.KryoSerializer), 5) Caching — cache reused DataFrames, 6) AQE — enable adaptive optimizations.

## Q76: What is Kryo serialization?
**A:** Kryo is a fast, efficient Java serialization framework. Spark uses it for serializing task data, shuffle data, and RDD storage. Enable: spark.serializer=org.apache.spark.serializer.KryoSerializer. Register classes: spark.kryo.classesToRegister=com.example.MyClass. Kryo is 10x faster than Java serialization with smaller output.

## Q77: How do you use PySpark with Jupyter notebooks?
**A:** Start SparkSession in notebook: import pyspark; spark = SparkSession.builder.appName("Notebook").getOrCreate(). Or use findspark: import findspark; findspark.init(). For managed environments: Databricks notebooks, Google Colab (with spark installation), or EMR notebooks. PySpark in notebooks allows iterative exploration.

## Q78: What are the differences between Spark local mode and cluster mode?
**A:** Local mode: runs on single machine with multiple threads — for development/testing. Cluster mode: runs on multiple machines — for production. Local mode: master("local[*]"), no cluster setup. Cluster mode: master("yarn"), requires cluster manager. Resource allocation, fault tolerance, and parallelism differ significantly.

## Q79: How do you deploy PySpark applications?
**A:** spark-submit script: spark-submit --master yarn --deploy-mode cluster --num-executors 10 --executor-cores 4 --executor-memory 8g app.py. Options: --packages (external JARs), --py-files (additional Python files), --files (config files), --conf (Spark configs). For orchestration: Airflow, Databricks, EMR, Glue.

## Q80: What is the difference between client mode and cluster mode?
**A:** Client mode: driver runs on the machine submitting the application (spark-submit). Cluster mode: driver runs on a worker node in the cluster. Client mode is for interactive/development; cluster mode is for production (driver fails gracefully with cluster). Cluster mode requires the driver program to be submitted as a JAR.

## Q81: How do you handle dependencies in PySpark?
**A:** Python dependencies: --py-files (zip/egg/py files), --archives (conda envs), --conf spark.pyspark.python=/path/to/python. JVM dependencies: --packages (Maven coordinates), --jars (JAR files). For complex dependencies: create a conda environment and ship as archive: --archives my_env.tar.gz#environment.

## Q82: What is Spark on Kubernetes?
**A:** Spark can run on Kubernetes clusters. spark-submit --master k8s://https://<k8s-api>. Benefits: resource isolation, dynamic scaling, integration with K8s ecosystem. Configuration: spark.kubernetes.container.image, spark.kubernetes.driver.pod.name. Spark 3.x has improved K8s support with volumes, secrets, and scheduler backends.

## Q83: What is Spark's interaction with cloud storage (S3, GCS, ADLS)?
**A:** Configure Hadoop filesystem connectors: s3a:// for AWS S3 (hadoop-aws JAR), gs:// for GCS (gcs-connector), wasbs:// for Azure Blob/ADLS. Authentication via access keys, IAM roles, or instance profiles. Performance: use S3A committer for better write performance on S3. Parquet format recommended for cloud storage.

## Q84: How do you read large CSV files efficiently?
**A:** Use Parquet instead (columnar, compressed). If CSV required: 1) Specify schema (avoid inferSchema), 2) Use header=True, 3) Use delimiter, quote, escape as needed, 4) Use multiLine=True for multi-line records, 5) Compress (.gz, .bz2), 6) Partition by date/region for faster reads, 7) Use wholeFile for small files.

## Q85: What is the difference between coalesce and repartition?
**A:** coalesce(n) reduces partitions without full shuffle (merges partitions on same node) — only for decreasing partitions. repartition(n) changes partitions with full shuffle — for both increasing and decreasing. coalesce is more efficient but can create data skew. Use repartition for increasing partitions, coalesce for decreasing.

## Q86: What is data locality in Spark?
**A:** Data locality means processing data on the node where it's stored (no network transfer). Spark tries to schedule tasks as PROCESS_LOCAL (same JVM), NODE_LOCAL (same node), RACK_LOCAL (same rack), or ANY (cross-rack). Good data locality reduces network I/O and improves performance. Impacted by partition placement and resource availability.

## Q87: What is the difference between narrow and wide dependencies?
**A:** Narrow dependency: each parent partition is used by at most one child partition (map, filter, union). No shuffle required. Wide dependency: each parent partition can be used by multiple child partitions (groupByKey, reduceByKey, join). Requires shuffle (data redistribution across cluster). Wide dependencies create stage boundaries.

## Q88: How do you handle small file problem in Spark?
**A:** Many small files cause high task overhead (scheduling, JVM startup for each). Solutions: 1) Coalesce: df.coalesce(n) to write fewer output files, 2) Repartition: df.repartition(n) for even file sizes, 3) Dynamic partition coalescing (AQE feature), 4) File compaction: batch process to merge small files into larger ones, 5) Use Delta Lake for auto-compaction.

## Q89: What is the Tachyon/Alluxio integration?
**A:** Alluxio (formerly Tachyon) is a memory-speed virtual distributed storage system. It caches data across cluster memory, enabling faster access across jobs and users. Spark integration: spark.hadoop.fs.alluxio.impl=alluxio.hadoop.FileSystem. Useful for shared caching across multiple Spark applications.

## Q90: How do you use PySpark with GPUs?
**A:** Spark 3.x supports GPU scheduling via spark.worker.resource.gpu.amount. For GPU-accelerated ML: use RAPIDS Accelerator for Spark (GPU-accelerated SQL operations). For DL: use Spark + TensorFlow/PyTorch via spark-tensorflow-distributor or Horovod. Allocate GPU resources per executor: spark.executor.resource.gpu.amount=1.

## Q91: How do you handle version compatibility in PySpark?
**A:** Key considerations: 1) Spark version matches Scala version (Spark 3.x uses Scala 2.12/2.13), 2) Python version compatibility (3.8+ for recent Spark), 3) Hadoop version for storage connectors, 4) Java version (Java 8/11 for Spark 3.x), 5) Check package compatibility for external libraries.

## Q92: What is Spark 3.x new features?
**A:** Key features in Spark 3.x: 1) AQE (Adaptive Query Execution) — dynamic optimization, 2) Dynamic partition pruning — skip irrelevant partitions, 3) Pandas UDFs (Type-Hinted) — better typing, 4) Accelerator-aware scheduling — GPU support, 5) ANSI SQL compliance, 6) Improved Python error handling, 7) Delta Lake integration, 8) Kubernetes scheduler.

## Q93: How do you use PySpark with MLflow?
**A:** MLflow integrates with PySpark for experiment tracking and model management. Usage: mlflow.spark.autolog() for auto-logging. Log params, metrics, models: with mlflow.start_run(): model.fit(train); mlflow.spark.log_model(model, "model"). Register models in MLflow Registry. Deploy as Spark UDF for batch inference.

## Q94: What is the difference between Spark and Dask?
**A:** Spark: JVM-based, mature, SQL engine, streaming support, larger ecosystem (MLlib, GraphX), prefer for ETL and large-scale SQL. Dask: Python-native, lighter weight, easier to debug, integrates with NumPy/Pandas ecosystem, better for custom Python logic. Spark is better for production big data; Dask for Python-centric data science.

## Q95: How do you read data from multiple paths in PySpark?
**A:** spark.read.csv(["path1", "path2", "path3"]). Use wildcards: spark.read.csv("data/*.csv"). Read directory tree: spark.read.csv("data/**/*.csv"). For partitioned data: spark.read.parquet("base_path") reads all partitions automatically. Union multiple DataFrames: reduce(lambda a, b: a.unionByName(b), [df1, df2, df3]).

## Q96: How do you optimize joins when both tables are large?
**A:** 1) Ensure both tables are partitioned by join key (avoids shuffle for one side), 2) Use sort-merge join (default for large tables), 3) Enable AQE for skew join optimization, 4) Bucket tables by join key for pre-shuffled data, 5) Use bloom filter join (spark.sql.optimizer.bloomFilter.enabled), 6) Increase shuffle partitions.

## Q97: What is bucketing in Spark?
**A:** Bucketing partitions data by hash of a column into a fixed number of files. Similar to Hive bucketing. Write: df.write.bucketBy(10, "key").sortBy("value").saveAsTable("t"). Read: avoids shuffles for joins on the bucketed column when both tables use same buckets. Improves join performance significantly.

## Q98: How do you use PySpark for ETL pipelines?
**A:** Pattern: 1) Read source (SQL, S3, Kafka), 2) Transform (clean, filter, join, aggregate), 3) Write to destination (Parquet, Delta, SQL). Use DataFrame API for transformations. Use SQL for complex transformations. Schedule via Airflow or Databricks jobs. Monitor via Spark UI or Ganglia. Handle late data with watermarks (streaming).

## Q99: What are the best practices for PySpark production?
**A:** 1) Use Parquet/Delta format, 2) Define explicit schemas, 3) Enable AQE, 4) Tune shuffle partitions, 5) Cache appropriately, 6) Use broadcast joins, 7) Monitor Spark UI, 8) Implement retry logic, 9) Use config files for environment-specific settings, 10) Write tests with small data, 11) Log key metrics.

## Q100: What are the common PySpark interview coding patterns?
**A:** Patterns: 1) Word count (groupBy/agg), 2) Top N per group (window functions with rank), 3) Rolling averages (window with rangeBetween), 4) Sessionization (window with lag/lead), 5) Moving from Pandas to PySpark (pandas_udf), 6) Type 2 slowly changing dimensions (merge/upsert with Delta), 7) Cumulative sums (window with rowsBetween), 8) Time series resampling in streaming.

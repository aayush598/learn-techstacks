# Prisma ORM Interview Questions and Answers

## Q1: What is Prisma?
**A:** Prisma is an open-source next-generation ORM for Node.js and TypeScript that provides a type-safe database client, declarative schema modeling, and automated migrations.

## Q2: How does Prisma differ from traditional ORMs?
**A:** Unlike traditional ORMs like Sequelize or TypeORM, Prisma generates a fully type-safe client from a declarative schema and does not use class-based models or active record patterns.

## Q3: What are the main components of Prisma?
**A:** The main components are Prisma Schema (declarative data model), Prisma Migrate (schema migration system), and Prisma Client (auto-generated type-safe query builder).

## Q4: What languages does Prisma support?
**A:** Prisma supports TypeScript, JavaScript (Node.js), Go, and Java through community-maintained clients, with TypeScript being the primary target.

## Q5: What databases does Prisma support?
**A:** Prisma supports PostgreSQL, MySQL, SQLite, SQL Server, MongoDB, CockroachDB, and PlanetScale (MySQL-compatible).

## Q6: What is the Prisma schema file?
**A:** The Prisma schema file (schema.prisma) is the single source of truth for your database schema, defining datasources, generators, models, enums, and relations.

## Q7: What syntax is used in a Prisma schema?
**A:** The Prisma schema uses a dedicated Prisma Schema Language (PSL) with blocks for datasource, generator, model, enum, and type definitions.

## Q8: How do you define a model in Prisma schema?
**A:** A model is defined with the model keyword followed by the model name and fields with their types, attributes, and optional modifiers.

## Q9: What field types does Prisma support?
**A:** Prisma supports String, Int, Float, Boolean, DateTime, Json, Bytes, Decimal, BigInt, and enum types, plus relation fields.

## Q10: What do field modifiers and attributes look like?
**A:** Modifiers include ? (optional) and [] (list). Attributes use @ syntax like @id, @default, @unique, @relation, @map, and @@ syntax for block-level attributes.

## Q11: What are enums in Prisma schema?
**A:** Enums are defined with the enum keyword and list of string values that Prisma maps to database enum types in supported databases.

## Q12: What is the purpose of @@index and @@unique?
**A:** @@index creates a database index on specified fields, and @@unique defines a composite unique constraint across multiple fields.

## Q13: What is a datasource block in Prisma schema?
**A:** The datasource block specifies the database provider (postgresql, mysql, sqlite, sqlserver, mongodb, cockroachdb) and the connection URL.

## Q14: How do you specify a datasource URL in Prisma?
**A:** The datasource URL is set using the url field in the datasource block, typically referencing an environment variable like env(DATABASE_URL).

## Q15: Can you use environment variables in Prisma schema?
**A:** Yes, Prisma supports env() function in datasource url and other string fields to reference environment variables securely.

## Q16: How do you define multiple datasources?
**A:** Prisma supports multiple datasource blocks for shadow databases or preview features, but production setups typically use a single datasource.

## Q17: What is a generator in Prisma schema?
**A:** A generator block defines what client code to generate, most commonly generator client for Prisma Client.

## Q18: How do you generate Prisma Client?
**A:** Run prisma generate to create the Prisma Client in node_modules/.prisma/client based on your schema.

## Q19: Where is Prisma Client generated?
**A:** Prisma Client is generated in node_modules/.prisma/client by default, and can also be customized with the output field in the generator block.

## Q20: Can you customize the Prisma Client output location?
**A:** Yes, use the output field in the generator block like output = "../src/generated/prisma".

## Q21: How do you define a one-to-one relation in Prisma?
**A:** Use a relation field on one side with @relation and a unique constraint on the foreign key, with the related model having a corresponding field.

## Q22: How do you define a one-to-many relation in Prisma?
**A:** The parent model has a relation field typed as Child[] and the child model has a scalar foreign key field with @relation.

## Q23: How do you define a many-to-many relation in Prisma?
**A:** Use implicit M:N with relation fields on both sides typed as the other model's array, or explicit M:N with a junction model.

## Q24: What is an implicit many-to-many relation?
**A:** Prisma automatically creates a junction table when both sides have array relation fields without using @relation, no manual join model needed.

## Q25: What is an explicit many-to-many relation?
**A:** You manually define a junction model with foreign keys to both related models and @relation attributes on both sides for full control.

## Q26: How do you name a relation in Prisma?
**A:** Use the name argument in @relation like @relation("UserPosts") when you need to disambiguate multiple relations between the same models.

## Q27: What are relation fields and scalar fields?
**A:** Relation fields hold connected model instances, while scalar fields hold primitive values like strings and numbers that map to database columns.

## Q28: How does Prisma handle foreign keys?
**A:** Foreign keys are defined as scalar fields in the child model with @relation specifying which fields reference the parent's fields.

## Q29: What is referential integrity in Prisma?
**A:** It controls the action when a referenced record is deleted, with onDelete and onUpdate options using referential actions like Cascade, Restrict, SetNull.

## Q30: What referential actions does Prisma support?
**A:** Prisma supports Cascade, Restrict, NoAction, SetNull, SetDefault for onDelete and onUpdate in @relation attributes.

## Q31: How do you create a record with Prisma Client?
**A:** Use prisma.model.create({ data: { field: value } }) with mandatory fields provided in the data object.

## Q32: How do you find many records in Prisma?
**A:** Use prisma.model.findMany() optionally passing where, orderBy, skip, take, include, and select options.

## Q33: How do you find a single record by unique field?
**A:** Use prisma.model.findUnique({ where: { id: value } }) which requires a field with @id or @unique.

## Q34: How do you find the first matching record?
**A:** Use prisma.model.findFirst({ where: { field: value } }) which returns the first record matching the where clause.

## Q35: How do you update a record in Prisma?
**A:** Use prisma.model.update({ where: { id: value }, data: { field: newValue } }) to update fields on an existing record.

## Q36: How do you update many records at once?
**A:** Use prisma.model.updateMany({ where: { field: value }, data: { field: newValue } }) which returns a count of updated records.

## Q37: How do you delete a record in Prisma?
**A:** Use prisma.model.delete({ where: { id: value } }) to delete a single record by unique identifier.

## Q38: How do you delete many records at once?
**A:** Use prisma.model.deleteMany({ where: { field: value } }) which deletes all matching records and returns a count.

## Q39: How do you upsert a record in Prisma?
**A:** Use prisma.model.upsert({ where: { id: value }, update: { field: newValue }, create: { field: value } }) which creates or updates.

## Q40: How do you count records in Prisma?
**A:** Use prisma.model.count({ where: { field: value } }) to count records matching optional filter conditions.

## Q41: How does Prisma filtering work?
**A:** Prisma Client provides type-safe filter conditions in the where clause using operators like equals, in, gt, lt, contains, startsWith.

## Q42: How do you use AND in Prisma filters?
**A:** Use where: { AND: [ { field1: value1 }, { field2: value2 } ] } to require all conditions to be true.

## Q43: How do you use OR in Prisma filters?
**A:** Use where: { OR: [ { field1: value1 }, { field2: value2 } ] } to match records satisfying any condition.

## Q44: How do you use NOT in Prisma filters?
**A:** Use where: { NOT: { field: value } } or where: { NOT: [ { field1: value1 }, { field2: value2 } ] } to exclude matching records.

## Q45: How do you filter with in operator?
**A:** Use where: { field: { in: [value1, value2] } } to match records where the field matches any value in the array.

## Q46: How do you filter with contains?
**A:** Use where: { field: { contains: "text" } } to match records where the field contains the given substring (case-insensitive by default).

## Q47: How do you filter with startsWith and endsWith?
**A:** Use where: { field: { startsWith: "prefix" } } or where: { field: { endsWith: "suffix" } } for prefix/suffix matching.

## Q48: How do you filter with comparison operators?
**A:** Use operators like gt, gte, lt, lte for numeric/date comparison, e.g., where: { age: { gte: 18 } }.

## Q49: How does Prisma pagination work with skip and take?
**A:** Use skip and take options in findMany: prisma.model.findMany({ skip: 10, take: 5 }) skips 10 records and returns 5.

## Q50: What is cursor-based pagination in Prisma?
**A:** Use cursor and take options: prisma.model.findMany({ cursor: { id: cursorValue }, skip: 1, take: 5 }) for efficient pagination on large datasets.

## Q51: How do you implement offset pagination?
**A:** Pass skip (number of records to skip) and take (number to return) alongside where and orderBy in findMany.

## Q52: How do you implement cursor-based pagination?
**A:** Pass a cursor object with a unique field value and take for forward pagination, along with skip: 1 to exclude the cursor record.

## Q53: How do you sort results in Prisma?
**A:** Use orderBy with an object like { field: "asc" } or { field: "desc" }, or an array for multi-field sorting.

## Q54: Can you sort by related model fields?
**A:** Yes, use orderBy with nested object syntax like { posts: { title: "asc" } } to sort by a related model's field.

## Q55: How do you aggregate in Prisma?
**A:** Use prisma.model.aggregate({ _count: true, _sum: { field: true }, _avg: { field: true }, _min: { field: true }, _max: { field: true } }).

## Q56: How do you use aggregate count in Prisma?
**A:** Use _count: true or _count: { _all: true } in aggregate to get total record count, or specify individual fields.

## Q57: What does _sum do in aggregation?
**A:** _sum computes the sum of numeric field values across matching records, e.g., _sum: { price: true }.

## Q58: What does _avg, _min, _max do in aggregation?
**A:** _avg calculates the average, _min finds the minimum, and _max finds the maximum value of the specified numeric field.

## Q59: How do you use groupBy in Prisma?
**A:** prisma.model.groupBy({ by: ["field"], _count: true, _sum: { amount: true } }) aggregates data grouped by specified fields.

## Q60: How do you execute raw SQL queries in Prisma?
**A:** Use prisma.$queryRaw\`SELECT * FROM User WHERE age > ${minAge}\` to send raw SQL and get typed results.

## Q61: How do you execute raw SQL commands in Prisma?
**A:** Use prisma.$executeRaw\`UPDATE User SET name = ${name} WHERE id = ${id}\` to run raw SQL that modifies data and returns count.

## Q62: What is the difference between $queryRaw and $executeRaw?
**A:** $queryRaw returns rows from SELECT queries, while $executeRaw runs INSERT, UPDATE, DELETE commands and returns the count of affected rows.

## Q63: How does Prisma handle SQL injection in raw queries?
**A:** Prisma uses parameterized queries with tagged template literals, so variables are automatically escaped and parameterized.

## Q64: What are transactions in Prisma?
**A:** Transactions allow multiple database operations to execute atomically, committing all or rolling back on failure.

## Q65: What is an interactive transaction in Prisma?
**A:** Interactive transactions use prisma.$transaction(async (tx) => { ... }) with a callback where you use tx instead of prisma for operations.

## Q66: What are batch transactions in Prisma?
**A:** Pass an array of Prisma Client operations to prisma.$transaction([op1, op2, op3]) to run them sequentially in a single transaction.

## Q67: Can you mix interactive and batch transactions?
**A:** No, interactive transactions use callback syntax with tx, while batch transactions use an array of independent operations.

## Q68: What are nested writes in Prisma?
**A:** Nested writes allow creating or updating records along with their related records in a single operation using nested create, connect, disconnect.

## Q69: How do you create a record with nested related records?
**A:** Use prisma.user.create({ data: { name: "Alice", posts: { create: { title: "Post 1" } } } }) to create user with posts.

## Q70: How do you connect existing related records?
**A:** Use prisma.post.create({ data: { title: "Post", author: { connect: { id: userId } } } }) to link to existing author.

## Q71: How do you disconnect related records?
**A:** Use prisma.user.update({ where: { id }, data: { posts: { disconnect: { id: postId } } } }) to remove a relation without deleting the record.

## Q72: How do you use set for relations?
**A:** Use prisma.user.update({ where: { id }, data: { posts: { set: [{ id: postId1 }, { id: postId2 }] } } }) to replace all related records.

## Q73: How do you include related records in queries?
**A:** Use the include option: prisma.user.findMany({ include: { posts: true } }) to eagerly load related records.

## Q74: How do you select specific fields including relations?
**A:** Use the select option with nested select for relations: prisma.user.findMany({ select: { name: true, posts: { select: { title: true } } } }).

## Q75: What is the difference between include and select?
**A:** include loads all fields of related models, while select lets you pick specific fields from both the parent and related models.

## Q76: What was rejectOnNotFound used for?
**A:** rejectOnNotFound was an option on findUnique and findFirst that threw an error when no record was found, now replaced with findUniqueOrThrow and findFirstOrThrow.

## Q77: What is prisma migrate?
**A:** prisma migrate generates and runs SQL migration files from changes in the Prisma schema to keep the database schema in sync.

## Q78: What is prisma migrate dev?
**A:** prisma migrate dev creates a new migration from schema changes, applies it to the development database, and regenerates Prisma Client.

## Q79: What is prisma migrate deploy?
**A:** prisma migrate deploy applies pending migrations to a database without creating new ones, used in testing and production deployments.

## Q80: What is prisma migrate reset?
**A:** prisma migrate reset drops the database, recreates it from migrations, and runs seed scripts, useful for development resets.

## Q81: What is Prisma Studio?
**A:** Prisma Studio is a GUI tool accessible via prisma studio command for browsing, editing, and visualizing data in your database.

## Q82: How do you seed a database in Prisma?
**A:** Configure "prisma": { "seed": "ts-node prisma/seed.ts" } in package.json and run prisma db seed to execute the seed script.

## Q83: What is prisma db seed used for?
**A:** It executes the configured seed script to populate the database with initial or test data for development environments.

## Q84: What is Prisma middleware?
**A:** Middleware in Prisma allows you to hook into Client operations (like find, create) before or after they execute using the $use method.

## Q85: How do you create middleware in Prisma?
**A:** Use prisma.$use(async (params, next) => { const result = await next(params); return result; }) with the params and next callback.

## Q86: How is Prisma Client extensions different from middleware?
**A:** Extensions (v5+) provide a more modular way to add computed fields, custom methods, and model-level transformations without intercepting params.

## Q87: What are the types of Prisma Client extensions?
**A:** Prisma extensions support result (computed fields), query (custom query logic), model (custom model methods), and client (global client methods).

## Q88: How do you create a Prisma Client extension in v5?
**A:** Use prisma.$extends({ query: { user: { findMany({ args, query }) { return query(args) } } } }) to extend the client.

## Q89: How do you enable logging in Prisma Client?
**A:** Configure the PrismaClient constructor with log: ["query", "info", "warn", "error"] to output database queries and events.

## Q90: How does Prisma handle errors?
**A:** Prisma throws PrismaClientKnownRequestError, PrismaClientUnknownRequestError, PrismaClientValidationError, and PrismaClientInitializationError.

## Q91: What is PrismaClientKnownRequestError?
**A:** It is an error for database-level issues with a code property (like P2002 for unique constraint violations) that maps to specific database errors.

## Q92: How does Prisma handle connection pooling?
**A:** Prisma Client has a built-in connection pool, with connection_limit option in the datasource URL controlling pool size.

## Q93: Can Prisma work with PgBouncer?
**A:** Yes, use pgBouncer=true in the PostgreSQL connection string to enable prepared statement caching compatible with PgBouncer transaction mode.

## Q94: How do you deploy Prisma to production?
**A:** Run prisma migrate deploy in CI/CD to apply migrations, then start the application with generated Prisma Client ready.

## Q95: How do you use Prisma with Next.js?
**A:** Create a singleton PrismaClient instance in a global file to prevent multiple clients during hot reloading in development.

## Q96: How do you use Prisma with NestJS?
**A:** Create a PrismaModule with a PrismaService that extends PrismaClient and implements OnModuleInit for database connection.

## Q97: How do you use Prisma with GraphQL?
**A:** Prisma integrates with GraphQL through Nexus, TypeGraphQL, or directly in resolvers using Prisma Client for database access.

## Q98: What is Prisma Accelerate?
**A:** Accelerate is a global database cache and connection pooler that speeds up queries and manages connection limits for serverless environments.

## Q99: What is Prisma Pulse?
**A:** Pulse provides real-time database change streaming, allowing applications to react to data changes with type-safe events.

## Q100: What is relation mode in Prisma?
**A:** Relation mode defines how foreign keys are handled, with foreignKeys (default) using DB-level constraints and prisma handling relations in application code.

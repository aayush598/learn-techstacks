# Prisma with TypeScript

## Overview

Prisma is a modern ORM for Node.js and TypeScript. It provides a schema-first approach with auto-generated types, making it one of the most type-safe database tools available.

---

## 1. Prisma Setup

```bash
npm install prisma @prisma/client
npx prisma init
```

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  name      String
  email     String   @unique
  password  String
  role      Role     @default(USER)
  age       Int?
  posts     Post[]
  profile   Profile?
  tags      String[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@map("users")
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  tags      Tag[]
  comments  Comment[]
  score     Float?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([authorId])
  @@map("posts")
}

model Profile {
  id     String  @id @default(cuid())
  bio    String?
  avatar String?
  user   User    @relation(fields: [userId], references: [id])
  userId String  @unique

  @@map("profiles")
}

model Tag {
  id    String @id @default(cuid())
  name  String @unique
  posts Post[]

  @@map("tags")
}

model Comment {
  id        String @id @default(cuid())
  content   String
  post      Post   @relation(fields: [postId], references: [id])
  postId    String
  authorId  String
  author    User   @relation(fields: [authorId], references: [id])

  @@map("comments")
}

enum Role {
  USER
  ADMIN
  GUEST
}
```

```bash
npx prisma migrate dev --name init
```

---

## 2. CRUD Operations with Types

```typescript
import { PrismaClient, Prisma } from '@prisma/client';

const prisma = new PrismaClient();

// CREATE — type-safe insert
async function createUser() {
  const user = await prisma.user.create({
    data: {
      name: 'Alice',
      email: 'alice@example.com',
      password: await hashPassword('securepass'),
      role: 'ADMIN',
      age: 30,
    },
  });

  console.log(user.id);     // string (cuid)
  console.log(user.name);   // string
  console.log(user.role);   // 'ADMIN'
  console.log(user.createdAt); // Date
}

// READ — type-safe queries
async function findUsers() {
  // Find many with filter
  const adults = await prisma.user.findMany({
    where: {
      age: { gte: 18 },
      role: { not: 'GUEST' },
    },
    orderBy: { name: 'asc' },
    skip: 0,
    take: 10,
  });

  // Find unique
  const user = await prisma.user.findUnique({
    where: { email: 'alice@example.com' },
  });

  // Find first
  const firstAdmin = await prisma.user.findFirst({
    where: { role: 'ADMIN' },
    orderBy: { createdAt: 'asc' },
  });

  // Count
  const totalUsers = await prisma.user.count({
    where: { isActive: true },
  });
}

// UPDATE — type-safe update
async function updateUser(id: string) {
  const updated = await prisma.user.update({
    where: { id },
    data: {
      name: 'Alice Updated',
      age: { increment: 1 }, // Atomic operation
    },
  });
}

// UPSERT — create or update
async function upsertUser(email: string, name: string) {
  const user = await prisma.user.upsert({
    where: { email },
    create: { email, name, password: 'temp' },
    update: { name },
  });
}

// DELETE — type-safe delete
async function deleteUser(id: string) {
  await prisma.user.delete({ where: { id } });
}

// DELETE MANY
async function deleteInactiveUsers() {
  const { count } = await prisma.user.deleteMany({
    where: { isActive: false },
  });
  return count;
}
```

---

## 3. Include/Select Typing

```typescript
// Include — type-safe relation loading
async function getUserWithPosts(email: string) {
  const user = await prisma.user.findUnique({
    where: { email },
    include: {
      posts: true,
      profile: true,
    },
  });

  // user.posts is Post[] (not optional)
  // user.profile is Profile | null (not Post[] since it's a one-to-one)
  console.log(user?.posts[0].title);
  console.log(user?.profile?.bio);
}

// Select — pick specific fields
async function getUserSummary(email: string) {
  const user = await prisma.user.findUnique({
    where: { email },
    select: {
      name: true,
      email: true,
      posts: {
        select: {
          title: true,
          published: true,
        },
        where: { published: true },
      },
    },
  });

  // user.name is string
  // user.email is string
  // user.posts is { title: string; published: boolean }[]
  console.log(user?.name);
  user?.posts.forEach((post) => console.log(post.title));
}

// Nested includes with filtering
async function getUserWithRecentPosts(email: string) {
  const user = await prisma.user.findUnique({
    where: { email },
    include: {
      posts: {
        where: {
          published: true,
          createdAt: {
            gte: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
          },
        },
        orderBy: { createdAt: 'desc' },
        take: 5,
        include: {
          comments: {
            select: { content: true, authorId: true },
          },
          tags: true,
        },
      },
    },
  });

  return user;
}
```

---

## 4. Relation Queries

```typescript
// One-to-one
async function getProfile(userId: string) {
  const profile = await prisma.profile.findUnique({
    where: { userId },
    include: { user: true },
  });
  return profile;
}

// One-to-many
async function getUserPosts(userId: string) {
  const posts = await prisma.post.findMany({
    where: { authorId: userId },
    include: {
      author: { select: { name: true, email: true } },
      comments: true,
      tags: true,
    },
    orderBy: { createdAt: 'desc' },
  });
  return posts;
}

// Many-to-many
async function getPostsByTag(tagName: string) {
  const posts = await prisma.post.findMany({
    where: {
      tags: { some: { name: tagName } },
    },
    include: {
      tags: true,
      author: { select: { name: true } },
    },
  });
  return posts;
}

// Complex relation query
async function getDashboardData() {
  const data = await prisma.user.findMany({
    include: {
      posts: {
        where: { published: true },
        include: {
          comments: true,
          tags: true,
        },
      },
      profile: true,
    },
  });

  return data.map((user) => ({
    name: user.name,
    bio: user.profile?.bio,
    postCount: user.posts.length,
    totalComments: user.posts.reduce((sum, post) => sum + post.comments.length, 0),
    tags: [...new Set(user.posts.flatMap((p) => p.tags.map((t) => t.name)))],
  }));
}
```

---

## 5. Transactions

```typescript
// Interactive transaction
async function transferPosts(fromUserId: string, toUserId: string) {
  const result = await prisma.$transaction(async (tx) => {
    // Verify both users exist
    const [fromUser, toUser] = await Promise.all([
      tx.user.findUnique({ where: { id: fromUserId } }),
      tx.user.findUnique({ where: { id: toUserId } }),
    ]);

    if (!fromUser || !toUser) {
      throw new Error('One or both users not found');
    }

    // Transfer all posts
    const updated = await tx.post.updateMany({
      where: { authorId: fromUserId },
      data: { authorId: toUserId },
    });

    return { transferred: updated.count };
  });

  return result;
}

// Batch transaction
async function batchCreateUsers(users: Prisma.UserCreateManyInput[]) {
  const result = await prisma.$transaction([
    ...users.map((user) =>
      prisma.user.create({ data: user })
    ),
  ]);
  return result;
}

// Nested transaction
async function createPostWithTags(
  authorId: string,
  title: string,
  tagNames: string[]
) {
  return prisma.$transaction(async (tx) => {
    // Find or create tags
    const tags = await Promise.all(
      tagNames.map((name) =>
        tx.tag.upsert({
          where: { name },
          create: { name },
          update: {},
        })
      )
    );

    // Create post with tags
    const post = await tx.post.create({
      data: {
        title,
        authorId,
        tags: { connect: tags.map((t) => ({ id: t.id })) },
      },
      include: { tags: true, author: true },
    });

    return post;
  });
}
```

---

## 6. Typed Queries with Prisma Types

```typescript
import { Prisma, User, Post } from '@prisma/client';

// Using Prisma types directly
function formatUser(user: User): string {
  return `${user.name} (${user.email})`;
}

// Using Prisma's GetResult for inferred types
type UserWithPosts = Prisma.UserGetResult<{
  include: { posts: true };
}>;

// Type-safe where clause
type UserWhere = Prisma.UserWhereInput;

function buildUserFilter(search: string, role?: string): UserWhere {
  const where: UserWhere = {
    OR: [
      { name: { contains: search, mode: 'insensitive' } },
      { email: { contains: search, mode: 'insensitive' } },
    ],
  };

  if (role) {
    where.role = role as any;
  }

  return where;
}

// Type-safe orderBy
type UserOrderBy = Prisma.UserOrderByWithRelationInput;

const sortOptions: Record<string, UserOrderBy> = {
  name: { name: 'asc' },
  email: { name: 'desc' },
  created: { createdAt: 'desc' },
};

// Type-safe select
type UserSelect = Prisma.UserSelect;

const selectOptions: UserSelect = {
  name: true,
  email: true,
  posts: {
    select: {
      title: true,
      published: true,
    },
  },
};

// Generic query builder
async function paginatedQuery<T extends Record<string, any>>(
  model: { findMany: (args: any) => Promise<T[]>; count: (args: any) => Promise<number> },
  where: any,
  page: number,
  limit: number,
  orderBy?: any
): Promise<{ data: T[]; total: number; page: number; pages: number }> {
  const [data, total] = await Promise.all([
    model.findMany({ where, skip: (page - 1) * limit, take: limit, orderBy }),
    model.count({ where }),
  ]);

  return { data, total, page, pages: Math.ceil(total / limit) };
}

// Usage
const result = await paginatedQuery(
  prisma.user,
  { role: 'ADMIN' },
  1,
  20,
  { createdAt: 'desc' }
);
```

---

## 7. Best Practices

1. **Use Prisma schema** as the single source of truth for your data model.
2. **Let Prisma generate types** — never manually define database types.
3. **Use `include`** for one-to-one and one-to-many relations.
4. **Use `select`** when you only need specific fields.
5. **Use `Prisma.UserCreateInput`** for create operations, not the model type.
6. **Use transactions** for operations that must succeed or fail together.
7. **Use `upsert`** for create-or-update patterns.
8. **Create service layers** that wrap Prisma operations.
9. **Use `Prisma.UserWhereInput`** for dynamic filters.
10. **Handle `null` returns** — `findUnique` returns `T | null`.

---

## Interview Questions

1. What are the benefits of Prisma over Mongoose for TypeScript?
2. How does Prisma generate types from the schema?
3. Explain the difference between `include` and `select` with types.
4. How do you type a paginated query result?
5. What is `Prisma.UserGetResult` and when should you use it?
6. How do you handle transactions in Prisma with TypeScript?
7. How do you create type-safe dynamic filters?
8. What is the difference between `findUnique` and `findFirst` return types?
9. How do you type a Prisma middleware?
10. How do you handle null returns from `findUnique`?

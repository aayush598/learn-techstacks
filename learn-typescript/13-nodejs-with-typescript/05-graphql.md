# GraphQL with TypeScript

## Overview

GraphQL is a query language for APIs. TypeScript provides end-to-end type safety for schemas, resolvers, context, and client-side queries. This covers both schema-first and code-first approaches.

---

## 1. Schema-First Approach (TypeGraphQL)

```bash
npm install type-graphql reflect-metadata
npm install apollo-server-express express
```

```typescript
import 'reflect-metadata';
import {
  Resolver,
  Query,
  Mutation,
  Arg,
  Field,
  ObjectType,
  ID,
  InputType,
  Int,
  Authorized,
  Ctx,
  FieldResolver,
  Root,
} from 'type-graphql';
import { ApolloServer } from 'apollo-server-express';

// Object types
@ObjectType()
class User {
  @Field(() => ID)
  id: string;

  @Field()
  name: string;

  @Field()
  email: string;

  @Field(() => Int)
  age: number;

  @Field()
  role: string;

  @Field()
  isActive: boolean;

  @Field(() => Date)
  createdAt: Date;
}

@ObjectType()
class Post {
  @Field(() => ID)
  id: string;

  @Field()
  title: string;

  @Field({ nullable: true })
  content?: string;

  @Field()
  published: boolean;

  @Field(() => User)
  author: User;

  @Field(() => [String])
  tags: string[];
}

// Input types
@InputType()
class CreateUserInput {
  @Field()
  name: string;

  @Field()
  email: string;

  @Field(() => Int)
  age: number;

  @Field({ defaultValue: 'USER' })
  role: string;
}

@InputType()
class UpdateUserInput {
  @Field({ nullable: true })
  name?: string;

  @Field({ nullable: true })
  email?: string;

  @Field(() => Int, { nullable: true })
  age?: number;
}

@InputType()
class PaginationInput {
  @Field(() => Int, { defaultValue: 1 })
  page: number;

  @Field(() => Int, { defaultValue: 10 })
  limit: number;
}

// Context type
interface GraphQLContext {
  user: User | null;
  loaders: DataLoaderMap;
}

// Resolver
@Resolver(() => User)
class UserResolver {
  @Query(() => [User])
  async users(
    @Arg('pagination', { nullable: true }) pagination: PaginationInput,
    @Ctx() ctx: GraphQLContext
  ): Promise<User[]> {
    return UserService.findAll(pagination);
  }

  @Query(() => User, { nullable: true })
  async user(@Arg('id') id: string): Promise<User | null> {
    return UserService.findById(id);
  }

  @Mutation(() => User)
  async createUser(@Arg('data') data: CreateUserInput): Promise<User> {
    return UserService.create(data);
  }

  @Mutation(() => User, { nullable: true })
  async updateUser(
    @Arg('id') id: string,
    @Arg('data') data: UpdateUserInput
  ): Promise<User | null> {
    return UserService.update(id, data);
  }

  @Mutation(() => Boolean)
  async deleteUser(@Arg('id') id: string): Promise<boolean> {
    return UserService.delete(id);
  }

  // Field resolver — resolves User.posts
  @FieldResolver(() => [Post])
  async posts(@Root() user: User): Promise<Post[]> {
    return PostService.findByAuthor(user.id);
  }
}
```

---

## 2. Code-First Approach

```typescript
import {
  Resolver,
  Query,
  Mutation,
  Arg,
  Field,
  ObjectType,
  ID,
  InputType,
  Int,
  Ctx,
} from 'type-graphql';

// Types
@ObjectType()
class User {
  @Field(() => ID)
  id: string;

  @Field()
  name: string;

  @Field()
  email: string;

  @Field(() => Int)
  age: number;

  @Field()
  role: string;
}

@ObjectType()
class AuthPayload {
  @Field()
  token: string;

  @Field(() => User)
  user: User;
}

// Input types
@InputType()
class LoginInput {
  @Field()
  email: string;

  @Field()
  password: string;
}

// Custom scalar type
import { GraphQLScalarType, Kind } from 'graphql';

const DateTimeScalar = new GraphQLScalarType({
  name: 'DateTime',
  description: 'ISO date string',
  serialize(value: unknown): string {
    if (value instanceof Date) {
      return value.toISOString();
    }
    throw new Error('DateTimeScalar can only serialize Date objects');
  },
  parseValue(value: unknown): Date {
    if (typeof value === 'string') {
      const date = new Date(value);
      if (isNaN(date.getTime())) {
        throw new Error('Invalid date string');
      }
      return date;
    }
    throw new Error('DateTimeScalar can only parse string values');
  },
});

// Union types
@ObjectType()
class PostSuccess {
  @Field(() => Post)
  post: Post;
}

@ObjectType()
class PostError {
  @Field()
  message: string;

  @Field(() => [String], { nullable: true })
  fields?: string[];
}

import { createUnionType } from 'type-graphql';

const PostResult = createUnionType({
  name: 'PostResult',
  types: () => [PostSuccess, PostError],
  resolveType(value) {
    if ('post' in value) return PostSuccess;
    if ('message' in value) return PostError;
    return undefined;
  },
});

// Context
interface Context {
  user: User | null;
}

// Resolver with union return type
@Resolver()
class PostResolver {
  @Mutation(() => PostResult)
  async createPost(
    @Arg('title') title: string,
    @Arg('content', { nullable: true }) content: string,
    @Ctx() ctx: Context
  ): Promise<typeof PostResult> {
    if (!ctx.user) {
      return { message: 'Not authenticated' };
    }

    if (title.length < 3) {
      return { message: 'Title too short', fields: ['title'] };
    }

    const post = await PostService.create({
      title,
      content,
      authorId: ctx.user.id,
    });

    return { post };
  }
}
```

---

## 3. Typed Resolvers

```typescript
import { Resolver, Query, Mutation, Args, ID } from '@type-graphql';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// Service with typed methods
class UserService {
  async findAll(args: { skip?: number; take?: number; where?: any }) {
    return prisma.user.findMany(args);
  }

  async findById(id: string) {
    return prisma.user.findUnique({ where: { id } });
  }

  async create(data: { name: string; email: string; age: number }) {
    return prisma.user.create({ data });
  }
}

// Resolver using service
@Resolver()
class UserResolver {
  private userService = new UserService();

  @Query(() => [User])
  async users(
    @Args() { skip, take }: PaginationArgs
  ): Promise<User[]> {
    return this.userService.findAll({ skip, take });
  }

  @Query(() => User, { nullable: true })
  async user(@Arg('id', () => ID) id: string): Promise<User | null> {
    return this.userService.findById(id);
  }

  @Mutation(() => User)
  async createUser(
    @Args() { name, email, age }: CreateUserArgs
  ): Promise<User> {
    return this.userService.create({ name, email, age });
  }
}

// Args classes
import { ArgsType, Field } from 'type-graphql';

@ArgsType()
class PaginationArgs {
  @Field(() => Int, { defaultValue: 0 })
  skip: number;

  @Field(() => Int, { defaultValue: 10 })
  take: number;
}

@ArgsType()
class CreateUserArgs {
  @Field()
  name: string;

  @Field()
  email: string;

  @Field(() => Int)
  age: number;
}
```

---

## 4. Typed Context

```typescript
import { ContextFunction } from 'apollo-server';
import { Request, Response } from 'express';
import { PrismaClient } from '@prisma/client';

// Context type
interface Context {
  prisma: PrismaClient;
  user: User | null;
  loaders: {
    userLoader: DataLoader<string, User>;
    postsByAuthorLoader: DataLoader<string, Post[]>;
  };
}

// Context creation function
const prisma = new PrismaClient();

const contextFn: ContextFunction<{ req: Request; res: Response }, Context> = async ({
  req,
  res,
}) => {
  const token = req.headers.authorization?.split(' ')[1];
  let user = null;

  if (token) {
    try {
      const payload = verifyToken(token);
      user = await prisma.user.findUnique({ where: { id: payload.userId } });
    } catch {
      // Invalid token
    }
  }

  return {
    prisma,
    user,
    loaders: createDataLoaders(),
  };
};

// Apollo Server setup
const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: contextFn,
});
```

---

## 5. Client-Side Typed Queries (Typed GraphQL)

```typescript
// With graphql-codegen
// Install: npm install -D @graphql-codegen/cli @graphql-codegen/typescript @graphql-codegen/typescript-operations

// schema.graphql
/*
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String
  author: User!
}

type Query {
  users: [User!]!
  user(id: ID!): User
}
*/

// Generated types (from codegen)
interface GetUsersQuery {
  users: Array<{
    id: string;
    name: string;
    email: string;
  }>;
}

interface GetUserQuery {
  user: {
    id: string;
    name: string;
    email: string;
    posts: Array<{
      id: string;
      title: string;
    }>;
  } | null;
}

// Type-safe query function
import { gql } from 'graphql-tag';

const GET_USERS = gql`
  query GetUsers {
    users {
      id
      name
      email
    }
  }
`;

async function fetchUsers(): Promise<GetUsersQuery> {
  const response = await fetch('/graphql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: GET_USERS.loc?.source.body,
    }),
  });
  return response.json();
}
```

---

## 6. Input Validation

```typescript
import { InputType, Field, ClassType } from 'type-graphql';
import { Length, IsEmail, IsInt, Min, Max } from 'class-validator';

@InputType()
class CreateUserInput {
  @Field()
  @Length(1, 100, { message: 'Name must be 1-100 characters' })
  name: string;

  @Field()
  @IsEmail({}, { message: 'Invalid email address' })
  email: string;

  @Field(() => Int)
  @IsInt()
  @Min(13)
  @Max(150)
  age: number;
}
```

---

## 7. Best Practices

1. **Use code-first** for TypeScript-heavy projects — types are the source of truth.
2. **Use schema-first** for team projects with multiple languages.
3. **Always type your context** — it's used across all resolvers.
4. **Use `@ObjectType()`** and `@InputType()` decorators for type-safe schemas.
5. **Use `graphql-codegen`** for client-side type generation.
6. **Validate inputs** with class-validator decorators.
7. **Use DataLoaders** to prevent N+1 queries.
8. **Return union types** for operations that can fail.
9. **Use `FieldResolver`** for computed fields and relation loading.
10. **Keep resolvers thin** — delegate business logic to service classes.

---

## Interview Questions

1. What is the difference between schema-first and code-first in GraphQL?
2. How do you type the GraphQL context in TypeScript?
3. How do you handle N+1 queries in GraphQL?
4. Explain union types in GraphQL with TypeScript.
5. How do you generate TypeScript types from a GraphQL schema?
6. How do you type GraphQL resolvers?
7. What are DataLoaders and why are they needed?
8. How do you validate GraphQL inputs with TypeScript?
9. How do you handle authentication in GraphQL resolvers?
10. What are the advantages of GraphQL over REST for TypeScript?

# Typegoose/Mongoose with TypeScript

## Overview

Mongoose is the most popular MongoDB ODM for Node.js. Typegoose is a wrapper that lets you define Mongoose schemas using TypeScript classes with decorators, providing end-to-end type safety.

---

## 1. Mongoose with TypeScript (Plain)

```typescript
import mongoose, { Schema, Document, Model, model } from 'mongoose';

// Define interface
interface IUser {
  name: string;
  email: string;
  age: number;
  role: 'admin' | 'user' | 'guest';
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

// Extend Document for instance methods and properties
interface IUserDocument extends IUser, Document {
  fullName(): string;
  isAdmin(): boolean;
}

// Static methods interface
interface IUserModel extends Model<IUserDocument> {
  findByEmail(email: string): Promise<IUserDocument | null>;
  findActive(): Promise<IUserDocument[]>;
}

// Schema definition
const userSchema = new Schema<IUserDocument, IUserModel>(
  {
    name: { type: String, required: true, trim: true },
    email: { type: String, required: true, unique: true, lowercase: true },
    age: { type: Number, required: true, min: 0, max: 150 },
    role: { type: String, enum: ['admin', 'user', 'guest'], default: 'user' },
    isActive: { type: Boolean, default: true },
  },
  {
    timestamps: true, // Adds createdAt and updatedAt
  }
);

// Instance methods
userSchema.methods.fullName = function (): string {
  return this.name;
};

userSchema.methods.isAdmin = function (): boolean {
  return this.role === 'admin';
};

// Static methods
userSchema.statics.findByEmail = function (email: string) {
  return this.findOne({ email: email.toLowerCase() });
};

userSchema.statics.findActive = function () {
  return this.find({ isActive: true });
};

// Create model
const User: IUserModel = model<IUserDocument, IUserModel>('User', userSchema);

// Usage
async function createUser() {
  const user = await User.create({
    name: 'Alice',
    email: 'alice@example.com',
    age: 30,
    role: 'admin',
  });

  console.log(user.fullName()); // TypeScript knows about fullName
  console.log(user.isAdmin());  // TypeScript knows about isAdmin

  const found = await User.findByEmail('alice@example.com');
  const active = await User.findActive();
}
```

---

## 2. Typegoose Setup

```bash
npm install @typegoose/typegoose mongoose
npm install -D @types/mongoose
```

```typescript
import { prop, getModelForClass, ModelOptions, Severity, Pre } from '@typegoose/typegoose';
import { Types } from 'mongoose';

// User model with Typegoose
@ModelOptions({ schemaOptions: { timestamps: true } })
class User {
  @prop({ required: true, trim: true })
  public name!: string;

  @prop({ required: true, unique: true, lowercase: true })
  public email!: string;

  @prop({ min: 0, max: 150 })
  public age!: number;

  @prop({ enum: ['admin', 'user', 'guest'], default: 'user' })
  public role!: 'admin' | 'user' | 'guest';

  @prop({ default: true })
  public isActive!: boolean;

  @prop({ type: () => [String] })
  public tags?: string[];

  // Virtual property
  public get isAdult(): boolean {
    return this.age >= 18;
  }

  // Instance method
  public fullName(): string {
    return this.name;
  }

  // Static method
  static async findByEmail(this: any, email: string) {
    return this.findOne({ email: email.toLowerCase() });
  }
}

// Get the Mongoose model
const UserModel = getModelForClass(User);

// Usage — fully typed
async function main() {
  const user = new UserModel({
    name: 'Alice',
    email: 'alice@example.com',
    age: 30,
    role: 'admin',
  });

  await user.save();
  console.log(user.isAdult);    // true
  console.log(user.fullName()); // 'Alice'

  const found = await UserModel.findByEmail('alice@example.com');
}
```

---

## 3. Nested Documents and Arrays

```typescript
import { prop, getModelForClass, ModelOptions, Ref } from '@typegoose/typegoose';
import { Types } from 'mongoose';

// Embedded document
class Address {
  @prop({ required: true })
  public street!: string;

  @prop({ required: true })
  public city!: string;

  @prop({ required: true })
  public state!: string;

  @prop({ required: true })
  public zipCode!: string;

  @prop()
  public country?: string;
}

// Embedded document with ref
class Comment {
  @prop({ required: true })
  public content!: string;

  @prop({ ref: () => User, required: true })
  public author!: Ref<User>;

  @prop({ default: Date.now })
  public createdAt!: Date;
}

// Post model with embedded documents
@ModelOptions({ schemaOptions: { timestamps: true } })
class Post {
  @prop({ required: true })
  public title!: string;

  @prop({ required: true })
  public content!: string;

  @prop({ ref: () => User, required: true })
  public author!: Ref<User>;

  @prop({ type: () => [String] })
  public tags!: string[];

  @prop({ type: () => [Comment], default: [] })
  public comments!: Comment[];

  @prop({ type: () => Address })
  public location?: Address;
}

const PostModel = getModelForClass(Post);

// Query with populated refs
async function getPostWithAuthor(postId: string) {
  const post = await PostModel.findById(postId)
    .populate('author')  // Populates the User ref
    .populate('comments.author');

  if (!post) return null;

  // post.author is now User (populated)
  console.log(post.author.name);  // TypeScript knows about name
  console.log(post.comments[0].author.name);
}
```

---

## 4. Virtual Properties

```typescript
import { prop, getModelForClass, virtual } from '@typegoose/typegoose';

class Product {
  @prop({ required: true })
  public name!: string;

  @prop({ required: true, min: 0 })
  public price!: number;

  @prop({ required: true, min: 0 })
  public quantity!: number;

  // Virtual computed property
  @virtual
  public get stockStatus(): 'in-stock' | 'low-stock' | 'out-of-stock' {
    if (this.quantity === 0) return 'out-of-stock';
    if (this.quantity < 10) return 'low-stock';
    return 'in-stock';
  }

  @virtual
  public get formattedPrice(): string {
    return `$${this.price.toFixed(2)}`;
  }

  // Virtual setter
  @virtual
  public set discountPrice(value: number) {
    this.price = value / (1 - 0.1); // Reverse 10% discount
  }
}

const ProductModel = getModelForClass(Product);

// Virtual properties are computed, not stored
const product = new ProductModel({
  name: 'Widget',
  price: 9.99,
  quantity: 5,
});

console.log(product.stockStatus);   // 'low-stock'
console.log(product.formattedPrice); // '$9.99'
```

---

## 5. Static and Instance Methods

```typescript
import { prop, getModelForClass, ModelOptions, Pre } from '@typegoose/typegoose';

@ModelOptions({ schemaOptions: { timestamps: true } })
class User {
  @prop({ required: true })
  public name!: string;

  @prop({ required: true, unique: true })
  public email!: string;

  @prop({ required: true, select: false })
  public password!: string;

  @prop({ default: 0 })
  public loginAttempts!: number;

  // Instance method
  public async comparePassword(candidatePassword: string): Promise<boolean> {
    return bcrypt.compare(candidatePassword, this.password);
  }

  // Static method
  static async findByEmail(this: any, email: string) {
    return this.findOne({ email }).select('+password');
  }

  // Static method with return type
  static async findOrCreate(
    this: any,
    email: string,
    defaults: Partial<User>
  ): Promise<{ user: any; created: boolean }> {
    const user = await this.findOne({ email });
    if (user) return { user, created: false };
    const newUser = await this.create({ email, ...defaults });
    return { user: newUser, created: true };
  }
}

// Pre-save hook
@Pre<User>('save', async function (next) {
  if (this.isModified('password')) {
    this.password = await bcrypt.hash(this.password, 12);
  }
  next();
})
class UserWithHook extends User {}

const UserModel = getModelForClass(User);

// Usage
async function authenticate(email: string, password: string) {
  const user = await UserModel.findByEmail(email);
  if (!user) throw new Error('User not found');

  const isValid = await user.comparePassword(password);
  if (!isValid) throw new Error('Invalid password');

  return user;
}
```

---

## 6. Query Typing

```typescript
import { DocumentType, ModelType, Query, FilterQuery } from '@typegoose/typegoose';
import { UserModel } from './models/user';

// Typed query helpers
type UserDocument = DocumentType<User>;

// Filter type
type UserFilter = FilterQuery<UserDocument>;

// Find with options
interface FindOptions {
  page?: number;
  limit?: number;
  sort?: Record<string, 1 | -1>;
  select?: string;
  populate?: string[];
}

async function findUsers(
  filter: UserFilter = {},
  options: FindOptions = {}
): Promise<{ data: UserDocument[]; total: number }> {
  const { page = 1, limit = 10, sort = { createdAt: -1 }, select, populate = [] } = options;

  let query = UserModel.find(filter)
    .sort(sort)
    .skip((page - 1) * limit)
    .limit(limit);

  if (select) query = query.select(select);
  if (populate.length) {
    populate.forEach((p) => { query = query.populate(p); });
  }

  const [data, total] = await Promise.all([
    query.exec(),
    UserModel.countDocuments(filter).exec(),
  ]);

  return { data, total };
}

// Aggregation with typed pipeline
interface UserStats {
  _id: string;
  totalPosts: number;
  avgScore: number;
}

async function getUserStats(): Promise<UserStats[]> {
  return UserModel.aggregate<UserStats>([
    { $lookup: { from: 'posts', localField: '_id', foreignField: 'author', as: 'posts' } },
    { $project: { totalPosts: { $size: '$posts' }, avgScore: { $avg: '$posts.score' } } },
  ]);
}
```

---

## 7. Best Practices

1. **Use Typegoose** for schema-first development with TypeScript classes.
2. **Define interfaces** for all document shapes before creating schemas.
3. **Use `Ref<T>`** for references between collections.
4. **Always type query results** — use `DocumentType<T>` for full document type.
5. **Use virtual properties** for computed values not stored in MongoDB.
6. **Add pre/post hooks** for common operations (password hashing, etc.).
7. **Use `select: false`** for sensitive fields like passwords.
8. **Type static methods** with explicit return types.
9. **Use `FilterQuery<T>`** for typed find queries.
10. **Create separate DTOs** for input validation vs database models.

---

## Interview Questions

1. What is the difference between Mongoose Document and plain interface?
2. How do you type static methods in Mongoose?
3. Explain `Ref<T>` in Typegoose — how do you type populated documents?
4. How do you type a Mongoose aggregation pipeline?
5. What is `DocumentType<T>` and when should you use it?
6. How do you handle virtual properties in TypeScript?
7. How do you type a Mongoose middleware hook?
8. What are the benefits of Typegoose over plain Mongoose?
9. How do you type a Mongoose query with chained methods?
10. How do you handle relationships between Mongoose models with types?

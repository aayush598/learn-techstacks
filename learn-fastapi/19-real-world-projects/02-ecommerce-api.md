# Complete E-Commerce API Blueprint

## Project Overview

A production-grade REST API for e-commerce with product catalog, cart, orders, payments (Stripe), inventory management, and admin features.

## Feature List

- JWT authentication with role-based access (customer, admin, vendor)
- Product catalog with categories, variants, and images
- Full-text search with filtering and sorting
- Shopping cart with real-time sync
- Order processing with state machine
- Stripe payment integration
- Inventory management with stock tracking
- Email notifications (order confirmation, shipping)
- Admin dashboard API
- Vendor product management
- Review and rating system
- Coupon/discount system

## Folder Structure

```
ecommerce-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   └── events.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   ├── payment.py
│   │   ├── inventory.py
│   │   └── review.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   └── payment.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       ├── auth.py
│   │       ├── products.py
│   │       ├── categories.py
│   │       ├── cart.py
│   │       ├── orders.py
│   │       ├── payments.py
│   │       ├── reviews.py
│   │       └── admin.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── product_service.py
│   │   ├── cart_service.py
│   │   ├── order_service.py
│   │   ├── payment_service.py
│   │   ├── inventory_service.py
│   │   ├── email_service.py
│   │   └── search_service.py
│   └── utils/
│       ├── __init__.py
│       ├── pagination.py
│       ├── cache.py
│       └── image.py
├── tests/
├── migrations/
├── Dockerfile
└── docker-compose.yml
```

## Data Models

```python
# app/models/user.py
from sqlalchemy import String, Boolean, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    VENDOR = "vendor"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(100))
    role: Mapped[UserRole] = mapped_column(default=UserRole.CUSTOMER)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    addresses: Mapped[list["Address"]] = relationship(back_populates="user")
    orders: Mapped[list["Order"]] = relationship(back_populates="customer")
    cart: Mapped["Cart | None"] = relationship(back_populates="user", uselist=False)


# app/models/product.py
from sqlalchemy import String, Text, Float, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str] = mapped_column(Text)
    short_description: Mapped[str | None] = mapped_column(String(500))
    price: Mapped[float] = mapped_column(Float)
    compare_at_price: Mapped[float | None] = mapped_column(Float)
    sku: Mapped[str] = mapped_column(String(100), unique=True)
    vendor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_featured: Mapped[bool] = mapped_column(default=False)
    weight: Mapped[float | None] = mapped_column(Float)
    tags: Mapped[str | None] = mapped_column(Text)  # Comma-separated
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    vendor: Mapped["User"] = relationship()
    category: Mapped["Category"] = relationship(back_populates="products")
    images: Mapped[list["ProductImage"]] = relationship(back_populates="product", cascade="all, delete-orphan")
    variants: Mapped[list["ProductVariant"]] = relationship(back_populates="product", cascade="all, delete-orphan")
    inventory: Mapped["Inventory | None"] = relationship(back_populates="product", uselist=False)
    reviews: Mapped[list["Review"]] = relationship(back_populates="product")


class ProductVariant(Base):
    __tablename__ = "product_variants"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(100))  # e.g., "Red / XL"
    sku: Mapped[str] = mapped_column(String(100), unique=True)
    price_modifier: Mapped[float] = mapped_column(default=0.0)
    stock: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)

    product: Mapped["Product"] = relationship(back_populates="variants")


class ProductImage(Base):
    __tablename__ = "product_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    url: Mapped[str] = mapped_column(String(500))
    alt_text: Mapped[str | None] = mapped_column(String(255))
    sort_order: Mapped[int] = mapped_column(default=0)
    is_primary: Mapped[bool] = mapped_column(default=False)

    product: Mapped["Product"] = relationship(back_populates="images")


# app/models/category.py
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(String(500))
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    sort_order: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)

    products: Mapped[list["Product"]] = relationship(back_populates="category")
    parent: Mapped["Category | None"] = relationship("Category", remote_side="Category.id")
    children: Mapped[list["Category"]] = relationship("Category", back_populates="parent")


# app/models/cart.py
class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    coupon_code: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="cart")
    items: Mapped[list["CartItem"]] = relationship(back_populates="cart", cascade="all, delete-orphan")


class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    variant_id: Mapped[int | None] = mapped_column(ForeignKey("product_variants.id"))
    quantity: Mapped[int] = mapped_column(default=1)
    added_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    cart: Mapped["Cart"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()


# app/models/order.py
class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_number: Mapped[str] = mapped_column(String(20), unique=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(30), default="pending")
    subtotal: Mapped[float] = mapped_column(Float)
    tax: Mapped[float] = mapped_column(Float, default=0.0)
    shipping_cost: Mapped[float] = mapped_column(Float, default=0.0)
    discount: Mapped[float] = mapped_column(Float, default=0.0)
    total: Mapped[float] = mapped_column(Float)
    shipping_address: Mapped[str] = mapped_column(Text)
    billing_address: Mapped[str] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    customer: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")
    payment: Mapped["Payment | None"] = relationship(back_populates="order", uselist=False)


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product_name: Mapped[str] = mapped_column(String(255))
    product_image: Mapped[str | None] = mapped_column(String(500))
    quantity: Mapped[int] = mapped_column()
    unit_price: Mapped[float] = mapped_column(Float)
    total_price: Mapped[float] = mapped_column(Float)

    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()


# app/models/payment.py
class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    stripe_payment_intent_id: Mapped[str | None] = mapped_column(String(255))
    stripe_charge_id: Mapped[str | None] = mapped_column(String(255))
    amount: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    status: Mapped[str] = mapped_column(String(30), default="pending")
    payment_method: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    order: Mapped["Order"] = relationship(back_populates="payment")


# app/models/inventory.py
class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), unique=True)
    quantity: Mapped[int] = mapped_column(default=0)
    reserved: Mapped[int] = mapped_column(default=0)
    low_stock_threshold: Mapped[int] = mapped_column(default=10)
    track_inventory: Mapped[bool] = mapped_column(default=True)

    product: Mapped["Product"] = relationship(back_populates="inventory")

    @property
    def available(self) -> int:
        return self.quantity - self.reserved

    @property
    def is_in_stock(self) -> bool:
        return self.available > 0 if self.track_inventory else True

    @property
    def is_low_stock(self) -> bool:
        return self.available <= self.low_stock_threshold


# app/models/review.py
class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    rating: Mapped[int] = mapped_column()  # 1-5
    title: Mapped[str | None] = mapped_column(String(255))
    content: Mapped[str | None] = mapped_column(Text)
    is_verified: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    product: Mapped["Product"] = relationship(back_populates="reviews")
    user: Mapped["User"] = relationship()
```

## Core API Endpoints

```python
# app/api/v1/products.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, desc
from sqlalchemy.orm import selectinload
from app.core.database import get_db
from app.models.product import Product, ProductVariant, ProductImage
from app.models.inventory import Inventory
from app.models.user import User, UserRole

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
async def list_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    search: str | None = None,
    sort: str = "newest",
    is_featured: bool | None = None,
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Product)
        .options(
            selectinload(Product.images),
            selectinload(Product.category),
            selectinload(Product.inventory),
        )
        .where(Product.is_active == True)
    )

    if category_id:
        query = query.where(Product.category_id == category_id)
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    if max_price is not None:
        query = query.where(Product.price <= max_price)
    if is_featured is not None:
        query = query.where(Product.is_featured == is_featured)
    if search:
        term = f"%{search}%"
        query = query.where(or_(Product.name.ilike(term), Product.description.ilike(term), Product.tags.ilike(term)))

    sort_map = {
        "newest": desc(Product.created_at),
        "price_asc": Product.price,
        "price_desc": desc(Product.price),
        "name_asc": Product.name,
        "popular": desc(Product.view_count) if hasattr(Product, 'view_count') else desc(Product.created_at),
    }
    query = query.order_by(sort_map.get(sort, desc(Product.created_at)))

    total = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar()
    query = query.offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(query)
    products = result.scalars().unique().all()

    return {
        "products": [_product_to_dict(p) for p in products],
        "total": total,
        "page": page,
        "pages": max(1, -(-total // per_page)),
    }


def _product_to_dict(p: Product) -> dict:
    return {
        "id": p.id,
        "name": p.name,
        "slug": p.slug,
        "description": p.description,
        "short_description": p.short_description,
        "price": p.price,
        "compare_at_price": p.compare_at_price,
        "sku": p.sku,
        "category": {"id": p.category.id, "name": p.category.name} if p.category else None,
        "images": [{"id": img.id, "url": img.url, "alt": img.alt_text, "is_primary": img.is_primary} for img in sorted(p.images, key=lambda x: (not x.is_primary, x.sort_order))],
        "stock": p.inventory.available if p.inventory else None,
        "is_in_stock": p.inventory.is_in_stock if p.inventory else True,
        "is_featured": p.is_featured,
        "created_at": p.created_at.isoformat(),
    }


@router.get("/{product_id}")
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Product)
        .options(
            selectinload(Product.images),
            selectinload(Product.variants),
            selectinload(Product.category),
            selectinload(Product.inventory),
            selectinload(Product.reviews).selectinload(Review.user),
        )
        .where(Product.id == product_id, Product.is_active == True)
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(404, "Product not found")

    data = _product_to_dict(product)
    data["variants"] = [
        {"id": v.id, "name": v.name, "sku": v.sku, "price_modifier": v.price_modifier, "stock": v.stock}
        for v in product.variants
    ]
    data["reviews"] = [
        {"id": r.id, "rating": r.rating, "title": r.title, "content": r.content, "user": r.user.username, "created_at": r.created_at.isoformat()}
        for r in product.reviews
    ]
    avg_rating = sum(r.rating for r in product.reviews) / len(product.reviews) if product.reviews else 0
    data["average_rating"] = round(avg_rating, 1)
    data["review_count"] = len(product.reviews)

    return data
```

## Cart Service

```python
# app/services/cart_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.models.inventory import Inventory

class CartService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_cart(self, user_id: int) -> Cart:
        result = await self.db.execute(select(Cart).where(Cart.user_id == user_id))
        cart = result.scalar_one_or_none()
        if not cart:
            cart = Cart(user_id=user_id)
            self.db.add(cart)
            await self.db.flush()
        return cart

    async def add_item(self, user_id: int, product_id: int, quantity: int = 1) -> dict:
        cart = await self.get_or_create_cart(user_id)

        # Check stock
        inv_result = await self.db.execute(
            select(Inventory).where(Inventory.product_id == product_id)
        )
        inventory = inv_result.scalar_one_or_none()
        if inventory and not inventory.is_in_stock:
            raise ValueError("Product out of stock")
        if inventory and inventory.available < quantity:
            raise ValueError(f"Only {inventory.available} items available")

        # Check if already in cart
        existing = await self.db.execute(
            select(CartItem).where(
                CartItem.cart_id == cart.id,
                CartItem.product_id == product_id,
            )
        )
        item = existing.scalar_one_or_none()

        if item:
            item.quantity += quantity
        else:
            item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
            self.db.add(item)

        await self.db.flush()
        return await self._cart_summary(cart.id)

    async def update_item_quantity(self, user_id: int, product_id: int, quantity: int) -> dict:
        cart = await self.get_or_create_cart(user_id)
        result = await self.db.execute(
            select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == product_id)
        )
        item = result.scalar_one_or_none()
        if not item:
            raise ValueError("Item not in cart")

        if quantity <= 0:
            await self.db.delete(item)
        else:
            item.quantity = quantity

        await self.db.flush()
        return await self._cart_summary(cart.id)

    async def remove_item(self, user_id: int, product_id: int) -> dict:
        cart = await self.get_or_create_cart(user_id)
        result = await self.db.execute(
            select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == product_id)
        )
        item = result.scalar_one_or_none()
        if item:
            await self.db.delete(item)
            await self.db.flush()
        return await self._cart_summary(cart.id)

    async def clear_cart(self, user_id: int):
        cart = await self.get_or_create_cart(user_id)
        for item in cart.items:
            await self.db.delete(item)
        await self.db.flush()

    async def _cart_summary(self, cart_id: int) -> dict:
        result = await self.db.execute(
            select(CartItem).where(CartItem.cart_id == cart_id).options(
                selectinload(CartItem.product)
            )
        )
        items = result.scalars().all()

        total = 0.0
        items_data = []
        for item in items:
            subtotal = item.product.price * item.quantity
            total += subtotal
            items_data.append({
                "product_id": item.product_id,
                "name": item.product.name,
                "price": item.product.price,
                "quantity": item.quantity,
                "subtotal": subtotal,
            })

        return {
            "items": items_data,
            "total_items": sum(i["quantity"] for i in items_data),
            "subtotal": round(total, 2),
        }


# app/api/v1/cart.py
from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from app.models.user import User
from app.api.deps import get_current_active_user
from app.services.cart_service import CartService

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/")
async def get_cart(user: User = Depends(get_current_active_user), db = Depends(get_db)):
    service = CartService(db)
    cart = await service.get_or_create_cart(user.id)
    return await service._cart_summary(cart.id)

@router.post("/items")
async def add_to_cart(
    product_id: int,
    quantity: int = 1,
    user: User = Depends(get_current_active_user),
    db = Depends(get_db),
):
    try:
        service = CartService(db)
        return await service.add_item(user.id, product_id, quantity)
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.put("/items/{product_id}")
async def update_cart_item(
    product_id: int,
    quantity: int,
    user: User = Depends(get_current_active_user),
    db = Depends(get_db),
):
    try:
        service = CartService(db)
        return await service.update_item_quantity(user.id, product_id, quantity)
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.delete("/items/{product_id}")
async def remove_from_cart(
    product_id: int,
    user: User = Depends(get_current_active_user),
    db = Depends(get_db),
):
    service = CartService(db)
    return await service.remove_item(user.id, product_id)
```

## Order Processing

```python
# app/services/order_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.order import Order, OrderItem
from app.models.cart import Cart
from app.models.inventory import Inventory
from app.models.payment import Payment
import uuid
from datetime import datetime

class OrderStatus:
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PAID = "paid"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

VALID_TRANSITIONS = {
    OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
    OrderStatus.CONFIRMED: [OrderStatus.PAID, OrderStatus.CANCELLED],
    OrderStatus.PAID: [OrderStatus.PROCESSING, OrderStatus.CANCELLED],
    OrderStatus.PROCESSING: [OrderStatus.SHIPPED],
    OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
    OrderStatus.DELIVERED: [],
    OrderStatus.CANCELLED: [],
}


class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, user_id: int, shipping_address: str, billing_address: str) -> Order:
        # Get cart
        cart_result = await self.db.execute(
            select(Cart).where(Cart.user_id == user_id).options(
                selectinload(Cart.items).selectinload(CartItem.product)
            )
        )
        cart = cart_result.scalar_one_or_none()
        if not cart or not cart.items:
            raise ValueError("Cart is empty")

        # Create order
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        subtotal = 0.0

        order = Order(
            order_number=order_number,
            customer_id=user_id,
            status=OrderStatus.PENDING,
            shipping_address=shipping_address,
            billing_address=billing_address,
        )
        self.db.add(order)
        await self.db.flush()

        for cart_item in cart.items:
            product = cart_item.product
            item_total = product.price * cart_item.quantity
            subtotal += item_total

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                product_name=product.name,
                product_image=product.images[0].url if product.images else None,
                quantity=cart_item.quantity,
                unit_price=product.price,
                total_price=item_total,
            )
            self.db.add(order_item)

            # Reserve inventory
            inv_result = await self.db.execute(
                select(Inventory).where(Inventory.product_id == product.id)
            )
            inventory = inv_result.scalar_one_or_none()
            if inventory:
                if inventory.available < cart_item.quantity:
                    raise ValueError(f"Insufficient stock for {product.name}")
                inventory.reserved += cart_item.quantity

        tax = round(subtotal * 0.08, 2)  # 8% tax
        total = round(subtotal + tax, 2)

        order.subtotal = subtotal
        order.tax = tax
        order.total = total

        # Clear cart
        for item in cart.items:
            await self.db.delete(item)

        await self.db.flush()
        return order

    async def confirm_payment(self, order_id: int, payment_id: str, amount: float):
        order = (await self.db.execute(select(Order).where(Order.id == order_id))).scalar_one_or_none()
        if not order:
            raise ValueError("Order not found")

        # Create payment record
        payment = Payment(
            order_id=order.id,
            stripe_payment_intent_id=payment_id,
            amount=amount,
            status="succeeded",
        )
        self.db.add(payment)

        # Update order status
        order.status = OrderStatus.PAID

        # Commit inventory (decrement stock, clear reserved)
        for item in order.items:
            inv_result = await self.db.execute(
                select(Inventory).where(Inventory.product_id == item.product_id)
            )
            inventory = inv_result.scalar_one_or_none()
            if inventory:
                inventory.quantity -= item.quantity
                inventory.reserved -= item.quantity

        await self.db.flush()
        return order


# app/api/v1/orders.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/orders", tags=["Orders"])

class OrderCreate(BaseModel):
    shipping_address: str
    billing_address: str

@router.post("/", status_code=201)
async def create_order(
    payload: OrderCreate,
    user: User = Depends(get_current_active_user),
    db = Depends(get_db),
):
    try:
        service = OrderService(db)
        order = await service.create_order(user.id, payload.shipping_address, payload.billing_address)
        return {
            "id": order.id,
            "order_number": order.order_number,
            "total": order.total,
            "status": order.status,
        }
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/")
async def list_orders(user: User = Depends(get_current_active_user), db = Depends(get_db)):
    result = await db.execute(
        select(Order).where(Order.customer_id == user.id).order_by(desc(Order.created_at))
    )
    orders = result.scalars().all()
    return [{"id": o.id, "number": o.order_number, "total": o.total, "status": o.status, "created_at": o.created_at.isoformat()} for o in orders]

@router.get("/{order_id}")
async def get_order(order_id: int, user: User = Depends(get_current_active_user), db = Depends(get_db)):
    result = await db.execute(
        select(Order).where(Order.id == order_id, Order.customer_id == user.id).options(
            selectinload(Order.items), selectinload(Order.payment)
        )
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(404)
    return {
        "id": order.id,
        "order_number": order.order_number,
        "status": order.status,
        "subtotal": order.subtotal,
        "tax": order.tax,
        "total": order.total,
        "items": [{"name": i.product_name, "quantity": i.quantity, "price": i.unit_price, "total": i.total_price} for i in order.items],
        "payment": {"status": order.payment.status, "method": order.payment.payment_method} if order.payment else None,
        "created_at": order.created_at.isoformat(),
    }
```

## Stripe Payment Integration

```python
# app/services/payment_service.py
import stripe
from app.core.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentService:
    @staticmethod
    async def create_payment_intent(amount: float, currency: str = "usd", metadata: dict = None) -> dict:
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Stripe uses cents
            currency=currency,
            metadata=metadata or {},
            automatic_payment_methods={"enabled": True},
        )
        return {
            "client_secret": intent.client_secret,
            "payment_intent_id": intent.id,
            "amount": amount,
        }

    @staticmethod
    async def confirm_payment(payment_intent_id: str) -> dict:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return {
            "status": intent.status,
            "payment_intent_id": intent.id,
            "amount_received": intent.amount_received / 100,
        }

    @staticmethod
    async def create_refund(payment_intent_id: str, amount: float | None = None) -> dict:
        refund_data = {"payment_intent": payment_intent_id}
        if amount:
            refund_data["amount"] = int(amount * 100)
        refund = stripe.Refund.create(**refund_data)
        return {"refund_id": refund.id, "status": refund.status}


# app/api/v1/payments.py
from fastapi import APIRouter, Depends, HTTPException, Request

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/create-intent")
async def create_payment_intent(
    order_id: int,
    user: User = Depends(get_current_active_user),
    db = Depends(get_db),
):
    order = (await db.execute(select(Order).where(Order.id == order_id, Order.customer_id == user.id))).scalar_one_or_none()
    if not order:
        raise HTTPException(404, "Order not found")
    if order.status != "confirmed":
        raise HTTPException(400, f"Order cannot be paid. Status: {order.status}")

    result = await PaymentService.create_payment_intent(
        amount=order.total,
        metadata={"order_id": order.id, "user_id": user.id},
    )
    return result


@app.post("/webhook/stripe")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except (ValueError, stripe.error.SignatureVerificationError):
        raise HTTPException(400, "Invalid webhook")

    if event["type"] == "payment_intent.succeeded":
        pi = event["data"]["object"]
        order_id = int(pi["metadata"]["order_id"])
        order_service = OrderService(db)
        await order_service.confirm_payment(order_id, pi["id"], pi["amount_received"] / 100)

    return {"status": "ok"}
```

## Inventory Management

```python
# app/services/inventory_service.py
class InventoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_stock(self, product_id: int) -> dict:
        result = await self.db.execute(
            select(Inventory).where(Inventory.product_id == product_id)
        )
        inv = result.scalar_one_or_none()
        if not inv:
            return {"available": 999, "in_stock": True, "low_stock": False}
        return {
            "quantity": inv.quantity,
            "reserved": inv.reserved,
            "available": inv.available,
            "in_stock": inv.is_in_stock,
            "low_stock": inv.is_low_stock,
        }

    async def adjust_stock(self, product_id: int, adjustment: int, reason: str = "") -> dict:
        result = await self.db.execute(
            select(Inventory).where(Inventory.product_id == product_id)
        )
        inv = result.scalar_one_or_none()
        if not inv:
            inv = Inventory(product_id=product_id, quantity=adjustment)
            self.db.add(inv)
        else:
            inv.quantity += adjustment

        await self.db.flush()
        return {"product_id": product_id, "new_quantity": inv.quantity, "available": inv.available}

    async def bulk_update(self, updates: list[dict]) -> list[dict]:
        results = []
        for update in updates:
            result = await self.adjust_stock(
                update["product_id"],
                update["adjustment"],
                update.get("reason", ""),
            )
            results.append(result)
        return results


# app/api/v1/admin.py
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/admin", tags=["Admin"])

async def require_admin(user: User = Depends(get_current_user)):
    if user.role != UserRole.ADMIN:
        raise HTTPException(403, "Admin access required")
    return user

@router.get("/dashboard")
async def admin_dashboard(user: User = Depends(require_admin), db = Depends(get_db)):
    total_orders = (await db.execute(select(func.count()).select_from(Order))).scalar()
    total_revenue = (await db.execute(select(func.coalesce(func.sum(Order.total), 0)).where(Order.status == "paid"))).scalar()
    total_users = (await db.execute(select(func.count()).select_from(User))).scalar()
    total_products = (await db.execute(select(func.count()).select_from(Product))).scalar()

    return {
        "total_orders": total_orders,
        "total_revenue": round(total_revenue, 2),
        "total_users": total_users,
        "total_products": total_products,
    }

@router.get("/orders")
async def admin_list_orders(
    status: str | None = None,
    page: int = 1,
    per_page: int = 20,
    user: User = Depends(require_admin),
    db = Depends(get_db),
):
    query = select(Order).options(selectinload(Order.items), selectinload(Order.customer))
    if status:
        query = query.where(Order.status == status)
    query = query.order_by(desc(Order.created_at)).offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(query)
    orders = result.scalars().all()
    return [{"id": o.id, "number": o.order_number, "customer": o.customer.email, "total": o.total, "status": o.status} for o in orders]

@router.put("/orders/{order_id}/status")
async def update_order_status(
    order_id: int,
    new_status: str,
    user: User = Depends(require_admin),
    db = Depends(get_db),
):
    order = (await db.execute(select(Order).where(Order.id == order_id))).scalar_one_or_none()
    if not order:
        raise HTTPException(404)

    if new_status not in VALID_TRANSITIONS.get(order.status, []):
        raise HTTPException(400, f"Cannot transition from {order.status} to {new_status}")

    order.status = new_status
    await db.commit()
    return {"id": order.id, "status": order.status}
```

## Email Notification Service

```python
# app/services/email_service.py
import aiosmtplib
from email.mime.text import MIMEText
from jinja2 import Template
from app.core.config import settings

EMAIL_TEMPLATES = {
    "order_confirmation": """
        <h1>Order Confirmed!</h1>
        <p>Hi {{ name }},</p>
        <p>Your order <strong>{{ order_number }}</strong> has been confirmed.</p>
        <p>Total: ${{ total }}</p>
        <p>We'll notify you when it ships.</p>
    """,
    "shipping_notification": """
        <h1>Your Order Has Shipped!</h1>
        <p>Hi {{ name }},</p>
        <p>Order {{ order_number }} is on its way.</p>
        <p>Tracking: {{ tracking_number }}</p>
    """,
}

class EmailService:
    @staticmethod
    async def send(to: str, template_name: str, context: dict):
        html = Template(EMAIL_TEMPLATES[template_name]).render(**context)
        msg = MIMEText(html, "html")
        msg["Subject"] = context.get("subject", "Notification")
        msg["To"] = to
        msg["From"] = settings.EMAIL_FROM

        await aiosmtplib.send(msg, hostname=settings.SMTP_HOST, port=settings.SMTP_PORT)

    @staticmethod
    async def send_order_confirmation(email: str, name: str, order_number: str, total: float):
        await EmailService.send(email, "order_confirmation", {
            "name": name, "order_number": order_number, "total": f"{total:.2f}",
            "subject": f"Order {order_number} Confirmed",
        })
```

## Deployment Configuration

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
    env_file: .env
    ports: ["8000:8000"]
    depends_on: [db, redis]

  celery-worker:
    build: .
    command: celery -A app.core.celery_app worker -l info
    env_file: .env
    depends_on: [db, redis]

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ecommerce
      POSTGRES_USER: shop
      POSTGRES_PASSWORD: secret
    volumes: [pgdata:/var/lib/postgresql/data]
    ports: ["5432:5432"]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  stripe-cli:
    image: stripe/stripe-cli:latest
    command: listen --forward-to api:8000/webhook/stripe
    environment:
      STRIPE_API_KEY: ${STRIPE_SECRET_KEY}

volumes:
  pgdata:
```

## Requirements

```
fastapi==0.115.0
uvicorn[standard]==0.30.0
sqlalchemy[asyncio]==2.0.35
asyncpg==0.29.0
alembic==1.13.0
pydantic[email]==2.9.0
pydantic-settings==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
stripe==10.0.0
httpx==0.27.0
redis[hiredis]==5.1.0
Pillow==10.4.0
aiosmtplib==3.0.0
Jinja2==3.1.0
python-multipart==0.0.9
celery[redis]==5.4.0
```

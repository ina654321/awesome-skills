# Examples

## 10.1 Document Design Patterns

### E-commerce Product

```javascript
// Embedded for read-heavy
{
  _id: ObjectId("..."),
  name: "Wireless Mouse",
  price: 29.99,
  category: "electronics",
  tags: ["wireless", "mouse", "computer"],
  variants: [
    { color: "black", sku: "WM-BLK-001", stock: 45 },
    { color: "white", sku: "WM-WHT-001", stock: 32 }
  ],
  reviews: [
    { userId: ObjectId("..."), rating: 5, comment: "Great!" }
  ]
}
```

### Order with References

```javascript
// Reference pattern for complex relationships
{
  _id: ObjectId("..."),
  userId: ObjectId("user_ref"),      // Reference to users
  items: [
    { productId: ObjectId("prod1"), quantity: 2 },
    { productId: ObjectId("prod2"), quantity: 1 }
  ],
  total: 89.97,
  status: "pending",
  createdAt: ISODate("2024-01-15")
}
```

## 10.2 Aggregation Pipeline Patterns

### Basic Grouping

```javascript
db.orders.aggregate([
  { $match: { status: "completed" } },
  { $group: {
      _id: "$customerId",
      totalSpent: { $sum: "$total" },
      orderCount: { $sum: 1 },
      avgOrderValue: { $avg: "$total" }
    }
  },
  { $sort: { totalSpent: -1 } },
  { $limit: 10 }
])
```

### Complex Aggregation

```javascript
db.sales.aggregate([
  { $match: { date: { $gte: ISODate("2024-01-01") } } },
  { $group: {
      _id: {
        month: { $month: "$date" },
        category: "$category"
      },
      revenue: { $sum: "$amount" },
      quantity: { $sum: "$quantity" }
    }
  },
  { $project: {
      _id: 0,
      month: "$_id.month",
      category: "$_id.category",
      revenue: 1,
      quantity: 1,
      avgPrice: { $divide: ["$revenue", "$quantity"] }
    }
  },
  { $sort: { month: 1, revenue: -1 } }
])
```

### Lookup (Join)

```javascript
db.orders.aggregate([
  { $match: { status: "shipped" } },
  { $lookup: {
      from: "users",
      localField: "userId",
      foreignField: "_id",
      as: "user"
    }
  },
  { $unwind: "$user" },
  { $project: {
      orderId: "$_id",
      customerName: "$user.name",
      total: 1,
      status: 1
    }
  }
])
```

### Facet (Multiple Pipelines)

```javascript
db.products.aggregate([
  { $match: { category: "electronics" } },
  { $facet: {
      byPriceRange: [
        { $bucket: {
            groupBy: "$price",
            boundaries: [0, 50, 100, 200, Infinity],
            default: "Other",
            output: { count: { $sum: 1 } }
          }
        }
      ],
      topRated: [
        { $sort: { rating: -1 } },
        { $limit: 5 },
        { $project: { name: 1, rating: 1, price: 1 } }
      ],
      totalCount: [
        { $count: "count" }
      ]
    }
  }
])
```

## 10.3 Index Patterns

### Covering Index

```javascript
// Query: find by email, return name, createdAt
db.users.createIndex(
  { email: 1 },
  { name: 1, createdAt: 1 },  // covered fields
  { name: "email_covered_idx" }
)
```

### Compound Index Order

```javascript
// Query: WHERE status = 'active' AND createdAt >= date SORT BY createdAt
// Index order: equality fields first, then sort fields
db.orders.createIndex({ status: 1, createdAt: 1 })

// Query: WHERE status = 'active' SORT BY status, createdAt
// Index order: sort fields first
db.orders.createIndex({ createdAt: 1, status: 1 })
```

### Wildcard Index

```javascript
// Index all fields matching pattern
db.products.createIndex({ "attributes.$**": 1 })

// Wildcard for metadata
db.events.createIndex({ "metadata.*": 1 })
```

## 10.4 Update Patterns

### Array Updates

```javascript
// Add to array (no duplicates with $addToSet)
db.users.updateOne(
  { _id: id },
  { $addToSet: { interests: "reading" } }
)

// Push multiple
db.users.updateOne(
  { _id: id },
  { $push: { tags: { $each: ["new", "tags"] } } }
)

// Update array element
db.orders.updateOne(
  { _id: id, "items.productId": prodId },
  { $inc: { "items.$.quantity": 1 } }
)

// Filter array elements
db.orders.updateOne(
  { _id: id },
  { $pull: { items: { quantity: { $lt: 1 } } } }
)
```

### Conditional Updates

```javascript
// Update if exists, insert if not
db.users.updateOne(
  { email: "user@example.com" },
  { $set: { lastLogin: new Date() } },
  { upsert: true }
)

// Update with aggregation (4.2+)
db.orders.updateOne(
  { _id: id },
  [{ $set: {
      discount: { $multiply: ["$total", 0.1] },
      finalTotal: { $subtract: ["$total", { $multiply: ["$total", 0.1] }] }
    }
  }]
)
```

## 10.5 Shell Commands

```javascript
// Batch operations
db.collection.insertMany([
  { name: "Item 1" },
  { name: "Item 2" },
  { name: "Item 3" }
], { ordered: false })

// Find and modify
db.counters.findOneAndUpdate(
  { _id: "orderId" },
  { $inc: { seq: 1 } },
  { returnDocument: "after" }
)

// Bulk operations
const bulk = db.orders.initializeUnorderedBulkOp()
bulk.find({ status: "pending" }).update({ $set: { status: "processed" } })
bulk.insert({ item: "new", date: new Date() })
bulk.execute()
```

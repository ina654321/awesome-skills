# Standards & Reference

## 7.1 Coding Standards

### Clean Code Principles
| Principle | Description |
|-----------|-------------|
| **DRY** | Don't Repeat Yourself |
| **SOLID** | Single responsibility, Open-closed, Liskov substitution, Interface segregation, Dependency inversion |
| **YAGNI** | You Aren't Gonna Need It |
| **KISS** | Keep It Simple, Stupid |

### Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Variables | camelCase | `userName` |
| Constants | SCREAMING_SNAKE | `MAX_RETRIES` |
| Classes | PascalCase | `UserService` |
| Functions | camelCase | `getUserById()` |

## 7.2 Architecture Patterns

| Pattern | Use Case | Benefits |
|---------|----------|----------|
| Microservices | Large scale, team autonomy | Scalability, deployment |
| Monolith | Small teams, MVPs | Simplicity, performance |
| Event-driven | Async processing | Loose coupling |
| Layered | Traditional web apps | Separation of concerns |

## 7.3 API Design Standards

- REST: Resource-oriented, HTTP verbs
- GraphQL: Flexible queries
- gRPC: High performance, binary protocol
- WebSocket: Real-time bidirectional

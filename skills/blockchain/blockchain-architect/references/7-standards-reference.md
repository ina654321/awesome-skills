## § 7 · Standards & Reference

### Key ERC/EIP Standards

| Standard | Purpose | Use When | Security Considerations |
|----------|---------|----------|------------------------|
| **ERC-20** | Fungible tokens | Standard tokens, governance tokens, stablecoins | Check for reentrancy in transfer hooks; verify decimals handling |
| **ERC-721** | Non-fungible tokens (NFTs) | Unique digital collectibles, art, gaming items | Reentrancy on safeTransferFrom; check ownership before transfers |
| **ERC-1155** | Multi-token standard | Gaming items with both fungible and unique assets | Batch transfer reentrancy; safeTransferFrom callbacks |
| **ERC-4626** | Tokenized vaults | Yield-bearing vaults, lending protocols | Round-down on withdrawal; inflation attacks; first depositor bug |
| **ERC-4337** | Account abstraction | Smart wallets, social recovery, gasless transactions | Signature replay attacks; bundler DoS; entry point security |
| **ERC-2612** | Permit (gasless approvals) | Meta-transactions, improved UX | Signature replay across chains; deadline validation |
| **EIP-712** | Typed data signing | Structured data signing for dApps | Domain separator correctness; verifyingContract validation |
| **EIP-1559** | Fee market change | Dynamic gas pricing on Ethereum | Priority fee analysis for MEV; base fee estimation |
| **ERC-1967** | Proxy storage slots | Upgradeable contracts | Storage collision prevention; implementation slot validation |
| **ERC-1822** | Universal upgradeable proxy | UUPS pattern | Implementation contract must not self-destruct |
| **ERC-2981** | NFT royalty standard | Creator royalty enforcement | Optional enforcement; marketplace compliance varies |

### Smart Contract Design Patterns

| Pattern | Description | Use Case | Implementation |
|---------|-------------|----------|----------------|
| **Checks-Effects-Interactions** | Validate → Update state → External calls | All state-changing functions | Prevents reentrancy |
| **Pull over Push** | Users withdraw funds vs automatic transfers | Payments, refunds, rewards | Prevents reentrancy and gas limit issues |
| **Guard Check (Modifier)** | Pre-condition validation | Access control, state validation | Reusable modifiers |
| **Emergency Stop (Circuit Breaker)** | Pause functionality for crises | DeFi protocols, critical systems | Multi-sig or governance controlled |
| **Rate Limiting** | Throttle operations per time window | Minting, withdrawals, governance | Time-delayed operations |
| **Commit-Reveal** | Two-phase commit then reveal | Sealed-bid auctions, voting | Prevents frontrunning |
| **Merkle Proofs** | Efficient whitelist verification | Airdrops, allowlists | O(log n) verification |
| **Multicall** | Batch multiple operations | Gas optimization | Watch for reentrancy across calls |

### Consensus Mechanism Comparison

| Mechanism | Finality | Energy | Decentralization | Use Case | Examples |
|-----------|----------|--------|------------------|----------|----------|
| **PoW (Proof of Work)** | Probabilistic | High | Very High | Store of value, high security | Bitcoin, Ethereum (pre-merge) |
| **PoS (Proof of Stake)** | Probabilistic | Low | High | General purpose smart contracts | Ethereum 2.0, Polygon |
| **DPoS (Delegated PoS)** | Fast | Low | Medium | High throughput applications | EOS, Tron |
| **BFT (Byzantine Fault Tolerant)** | Immediate | Low | Medium | Enterprise, permissioned | Hyperledger Fabric, Cosmos |
| **Avalanche Consensus** | Sub-second | Low | High | DeFi, subnets | Avalanche |
| **Tendermint/Cosmos SDK** | ~1-2 seconds | Low | High | App chains, IBC ecosystem | Cosmos Hub, Osmosis |
| **HotStuff (Libra/BFT)** | ~3 seconds | Low | Medium | High-performance chains | Aptos, Sui, Diem |

### Layer 2 Solutions Deep Dive

| Solution Type | Security Model | Withdrawal Time | Gas Cost | Best For | Examples |
|---------------|----------------|-----------------|----------|----------|----------|
| **Optimistic Rollup** | Fraud proofs (7-day challenge) | 7 days | ~10x cheaper | General purpose EVM | Arbitrum, Optimism, Base |
| **ZK Rollup** | Validity proofs | Minutes | ~100x cheaper | High throughput, fast finality | zkSync Era, Scroll, Polygon zkEVM |
| **Validium** | ZK proofs + off-chain data | Minutes | ~1000x cheaper | Gaming, social (lower security) | Immutable X, Sorare |
| **State Channels** | Multi-sig with disputes | Instant | Off-chain | Micropayments, gaming | Lightning Network, Raiden |
| **Sidechain** | Separate consensus | Variable | Cheap | Lower security requirements | Polygon PoS (historically) |
| **App-Specific Rollup** | Custom data availability | Configurable | Optimized | High-performance single-app | dYdX v3, Immutable |

### Security Best Practices Matrix

| Layer | Practice | Tools | Priority |
|-------|----------|-------|----------|
| **Code** | Use established libraries (OpenZeppelin) | OZ Contracts | Critical |
| **Code** | Run static analysis on every commit | Slither, Mythril | Critical |
| **Code** | Fuzzing for invariant testing | Echidna, Medusa | High |
| **Code** | Formal verification for critical invariants | Certora, Halmos | Critical for DeFi |
| **Operational** | Multi-sig for privileged operations | Gnosis Safe | Critical |
| **Operational** | Timelocks for upgrades (48hr+ min) | OZ Defender | Critical |
| **Operational** | Emergency pause capability | OZ Pausable | High |
| **Monitoring** | Real-time threat detection | Forta, Hypernative | High |
| **Monitoring** | On-chain anomaly detection | Tenderly, Chaos Labs | High |

---

## Phase 1: Requirements & Risk Assessment

**Tasks:**
- Define use case, business model, and value proposition
- Determine public vs permissioned vs consortium blockchain
- Identify total value at risk (TVL projections) and regulatory constraints
- Document functional requirements and non-functional requirements (TPS, latency, finality)
- Assess cross-chain needs and integration points

**Deliverables:**
- [✓] Requirements specification document with user stories
- [✓] Risk assessment matrix with TVL estimates and regulatory analysis
- [✓] Platform selection decision document with trade-off analysis
- [✗] FAIL: Missing TVL estimates or regulatory analysis
- [✗] FAIL: No security threat model documented

### Phase 2: Architecture Design

**Tasks:**
- Select blockchain platform (L1/L2/L3) based on requirements
- Design smart contract architecture with upgrade strategy
- Define tokenomics model (supply, distribution, inflation, burns)
- Design governance structure (voting mechanism, quorum, timelock)
- Plan cross-chain integration architecture if needed
- Create data availability and privacy architecture

**Deliverables:**
- [✓] Architecture diagrams (C4 model: Context, Container, Component, Code)
- [✓] Tokenomics specification with mathematical modeling
- [✓] Governance framework documentation
- [✓] Upgrade path documentation with timelock parameters
- [✗] FAIL: No security considerations in architecture
- [✗] FAIL: Missing formal verification plan for critical invariants

### Phase 3: Smart Contract Development

**Tasks:**
- Implement contracts following security best practices (Checks-Effects-Interactions)
- Write comprehensive unit tests (aim for >95% coverage, 100% for critical paths)
- Implement integration tests for complex interactions and edge cases
- Run automated security scans (Slither, MythX) and fix findings
- Document code with NatSpec comments for all public functions
- Gas optimization review and implementation

**Deliverables:**
- [✓] Production-ready Solidity/Rust code with NatSpec
- [✓] Comprehensive test suite with >95% coverage
- [✓] Automated security scan reports (clean or documented exceptions)
- [✓] Gas optimization report with benchmarks
- [✗] FAIL: Missing access controls or reentrancy guards
- [✗] FAIL: Critical/high findings from automated scans not addressed

### Phase 4: Security Hardening

**Tasks:**
- Perform internal code review with comprehensive security checklist
- Write formal specifications for critical invariants
- Engage reputable audit firm for external review
- Address all audit findings with documented remediation
- Set up bug bounty program (Immunefi, Sherlock)
- Perform economic stress testing and game theory analysis

**Deliverables:**
- [✓] Internal security review document with checklist completion
- [✓] Formal verification results for critical invariants (Certora/Halmos)
- [✓] External audit report with all critical/high issues resolved
- [✓] Bug bounty program live with appropriate rewards
- [✓] Economic stress test report
- [✗] FAIL: Unresolved critical/high severity findings
- [✗] FAIL: No formal verification for critical financial invariants

### Phase 5: Testnet Deployment & Validation

**Tasks:**
- Deploy to public testnet (Sepolia, Holesky, or L2 testnets)
- Conduct user acceptance testing with beta users
- Test upgrade mechanisms and emergency procedures
- Verify monitoring, alerting, and incident response capabilities
- Simulate attack scenarios (fuzzing, economic attacks)

**Deliverables:**
- [✓] Testnet deployment with verified contracts on Etherscan
- [✓] UAT test results with user feedback
- [✓] Monitoring dashboard configured (Forta, Tenderly)
- [✓] Emergency procedure tested (pause, upgrade, recovery)
- [✗] FAIL: No test coverage for emergency procedures
- [✗] FAIL: Upgrade mechanism not tested with real conditions

### Phase 6: Mainnet Deployment & Operations

**Tasks:**
- Execute deployment plan with multi-sig governance
- Verify contracts on block explorers with full source code
- Initialize protocol with minimal initial state (gradual rollout)
- Activate monitoring, alerting, and incident response
- Execute gradual TVL increase plan with safety limits

**Deliverables:**
- [✓] Successful mainnet deployment with multi-sig
- [✓] Contracts verified and documented on all explorers
- [✓] Incident response plan active with runbooks
- [✓] Gradual TVL increase plan with circuit breakers
- [✗] FAIL: Deployment without timelock or guardian multisig
- [✗] FAIL: No monitoring or incident response capability

---


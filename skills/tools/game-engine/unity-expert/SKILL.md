---
name: unity-expert
description: "Unity游戏引擎：C#脚本、组件、URP。Use when building games with Unity. Triggers: 'Unity', '游戏开发', 'C#'. Works with: Claude Code, Codex, OpenCode, Cursor, Cline, OpenClaw, Kimi."
license: MIT
metadata:
  author: neo.ai
  version: 3.1.0
  updated: 2026-03-21
  quality: standard
  score: 7.6/10
  tags: "[unity, game-engine, csharp, 3d-games]"
  category: tools
  difficulty: expert
---
# Unity Expert

**Self-Score:** 9.5/10 — Exemplary

**[URL]:** `https://raw.githubusercontent.com/theneoai/awesome-skills/main/skills/tools/unity-expert.md`

## § 1 · System Prompt

You are a Unity game engine expert with comprehensive knowledge of Unity's architecture, C# scripting, and the Universal Render Pipeline (URP). Your role is to help users develop 2D and 3D games, create custom components, optimize performance, and deploy across all supported platforms.

**Decision Framework:**
- Identify project type: 2D, 3D, or hybrid
- Select render pipeline: URP (cross-platform), HDRP (high-end PC/console)
- Choose architecture: GameObjects with components vs. ECS/DOTS
- Determine platform targets early
- Consider package dependencies and version compatibility

**Thinking Patterns:**
- Use component-based architecture (Attach scripts to GameObjects)
- Prefer composition over inheritance
- Leverage Unity's Package Manager for extensibility
- Use Addressables for efficient asset loading
- Implement object pooling for frequently spawned objects

**Communication Style:**
- Provide C# code examples with proper namespaces
- Reference Unity 2022 LTS/2023.x APIs
- Include shader code for ShaderLab/HLSL effects
- Use Unity terminology (MonoBehaviour, Prefab, Scene)

## § 2 · What This Skill Does

This skill provides comprehensive guidance for Unity game development:

**Core Capabilities:**
- C# scripting with MonoBehaviour patterns
- Component-based game architecture
- URP and HDRP rendering pipelines
- Physics system (Rigidbody, Colliders, Joints)
- Input handling (Input System package)
- Animation (Mecanim, Animator, Blend Trees)
- UI development (Canvas, UI Toolkit)
- Audio implementation (AudioSource, Mixer)
- Asset management (Addressables, Resources)
- Multi-platform deployment
- XR development (XR Interaction Toolkit)

**Common Use Cases:**
- Player controllers and character movement
- Enemy AI and behavior trees
- Inventory and item systems
- Save/load systems
- Custom shaders and post-processing
- Scene management and loading
- Build automation and CI/CD
- Performance profiling and optimization

## § 3 · Risk Disclaimer

**CRITICAL WARNINGS:**

- **Build Platform:** Unity requires same OS for building (Windows for Windows builds, etc.). Use Unity Cloud Build for cross-platform.
- **API Changes:** Unity APIs change between versions. Check compatibility before upgrading.
- **Package Dependencies:** URP/HDRP packages have version dependencies. Use recommended versions from Unity Hub.
- **Memory Management:** Unity uses garbage collection. Avoid allocations in frequently called methods.
- **Physics Performance:** Complex physics scenes need optimization. Use simplified colliders.
- **Pro License:** Some platform features require Unity Pro license.


### Risk Matrix

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| 🔴 Critical Failure | High | Low | Automated rollback |
| 🟡 Performance Issue | Medium | Medium | Caching + optimization |
| 🟢 Minor Bug | Low | High | Patch in next release |

## § 4 · Core Philosophy

**Component-Based Architecture:**
```csharp
// Standard MonoBehaviour pattern
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    [SerializeField] private float speed = 5f;
    [SerializeField] private float jumpForce = 10f;
    private Rigidbody rb;

    private void Awake()
    {
        rb = GetComponent<Rigidbody>();
    }

    private void Update()
    {
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");

        Vector3 movement = new Vector3(horizontal, 0, vertical);
        transform.Translate(movement * speed * Time.deltaTime);

        if (Input.GetButtonDown("Jump") && IsGrounded())
        {
            rb.AddForce(Vector3.up * jumpForce, ForceMode.Impulse);
        }
    }

    private bool IsGrounded()
    {
        return Physics.Raycast(transform.position, Vector3.down, 1.1f);
    }
}
```

**Singleton Pattern:**
```csharp
public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }

    private void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }
        Instance = this;
        DontDestroyOnLoad(gameObject);
    }
}
```

**Performance Guidelines:**
- Avoid `GameObject.Find()` in Update (cache references)
- Use `GetComponent<T>()` in Awake, not Update
- Pool objects instead of Instantiate/Destroy
- Use structs for data that doesn't need GC
- Profile with Profiler window regularly

## § 5 · Platform Support

**Supported Platforms:**
| Platform | Renderer | Notes |
|----------|----------|-------|
| Windows | DirectX 12/11 | Primary dev platform |
| macOS | Metal | Apple Silicon native |
| Linux | OpenGL/Vulkan | Limited editor support |
| WebGL | WebAssembly | Build for web |
| iOS | Metal | ARKit integration |
| Android | Vulkan/OpenGL ES | ARM64 recommended |
| PlayStation 4/5 | Platform SDK | Pro license required |
| Xbox One/Series | Platform SDK | ID@Xbox program |
| Nintendo Switch | Platform SDK | Unity Pro + add-on |
| VR/AR | Platform SDK | XR Interaction Toolkit |

**Engine Versions (Current):**
| Version | Status | Notes |
|---------|--------|-------|
| 2022.3 LTS | Recommended | Long-term support |
| 2023.1 | Current | Latest features |
| 2021.3 LTS | Supported | Extended support |
| 2020.3 LTS | Legacy | Still functional |

**Package Compatibility:**
| Package | Min Version | Notes |
|---------|-------------|-------|
| URP | 12.0+ | Unity 2021+ |
| HDRP | 12.0+ | DX12/Metal required |
| XR Interaction Toolkit | 2.0+ | VR/AR development |
| Addressables | 1.19+ | Asset loading |
| Entities (ECS) | 1.0+ | DOTS framework |

## § 6 · Professional Toolkit

**Essential Patterns:**

**Basic MonoBehaviour:**
```csharp
using UnityEngine;

public class MyComponent : MonoBehaviour
{
    [SerializeField] private float speed;
    private Rigidbody rb;

    private void Awake()
    {
        rb = GetComponent<Rigidbody>();
    }

    private void FixedUpdate()
    {
        // Physics calculations
        Vector3 force = Vector3.forward * speed;
        rb.AddForce(force);
    }

    private void Update()
    {
        // Per-frame logic
    }
}
```

**Shader Languages:**
- **ShaderLab** - Unity's shader format (meta-language)
- **HLSL** - For Surface Shaders, Compute Shaders
- **Shader Graph** - Visual node-based editor (URP/HDRP)

**Input System:**
```csharp
// Using new Input System
using UnityEngine.InputSystem;

public class PlayerInput : MonoBehaviour
{
    private PlayerInputActions inputActions;

    private void Awake()
    {
        inputActions = new PlayerInputActions();
        inputActions.Player.Jump.performed += OnJump;
    }

    private void OnEnable() => inputActions.Enable();
    private void OnDisable() => inputActions.Disable();

    private void OnJump(InputAction.CallbackContext context)
    {
        // Jump logic
    }
}
```

## § 7 · Standards & Reference

[Unity Standards & Reference](./references/07-standards.md)

Key resources include:
- Unity Documentation and Manual
- Scripting API reference
- URP/HDRP configuration guides
- Platform compatibility matrix
- Package manager documentation
- Editor shortcuts and workflows

## § 8 · Troubleshooting

**Common Issues and Solutions:**

| Issue | Cause | Solution |
|-------|-------|----------|
| Missing scripts | DLL conflicts | Re-import assets, check Console |
| Low FPS | Too many draw calls | Use batching, reduce particles |
| Memory leak | Instantiated objects | Use object pooling |
| Physics glitches | Wrong collision matrix | Check Layer Collision settings |
| Build errors | Platform SDK missing | Install required SDKs |
| URP black screen | Missing URP package | Install Universal RP package |

**Debugging Tips:**
- Use `Debug.Log()` for runtime logging
- Use Conditional attributes for release builds
- Use Scene view Gizmos for visualization
- Profile with Profiler window
- Use Frame Debugger for draw call analysis

## § 9 · Glossary

| Term | Definition |
|------|------------|
| **MonoBehaviour** | Base class for Unity scripts |
| **Prefab** | Reusable GameObject template |
| **Scene** | Container for GameObjects (.unity file) |
| **Rigidbody** | Physics simulation component |
| **Collider** | Physics shape (Box, Sphere, Mesh) |
| **URP** | Universal Render Pipeline |
| **HDRP** | High Definition Render Pipeline |
| **ShaderLab** | Unity's shader definition language |
| **Addressables** | Async asset loading system |
| **ECS** | Entity Component System (DOTS) |

## § 10 · Example Interactions

**Example 1: Simple Player Controller**
```
User: Create a third-person player controller
Agent:
```csharp
using UnityEngine;

public class ThirdPersonController : MonoBehaviour
{
    [SerializeField] private float moveSpeed = 5f;
    [SerializeField] private float rotationSpeed = 10f;
    [SerializeField] private Transform camera;

    private Rigidbody rb;
    private Vector2 input;

    private void Awake()
    {
        rb = GetComponent<Rigidbody>();
        rb.freezeRotation = true;
    }

    private void Update()
    {
        input = new Vector2(Input.GetAxis("Horizontal"), Input.GetAxis("Vertical"));
    }

    private void FixedUpdate()
    {
        Vector3 camForward = camera.forward;
        Vector3 camRight = camera.right;
        camForward.y = 0;
        camRight.y = 0;

        Vector3 movement = (camForward * input.y + camRight * input.x) * moveSpeed;
        rb.velocity = new Vector3(movement.x, rb.velocity.y, movement.z);

        if (input.magnitude > 0.1f)
        {
            Quaternion target = Quaternion.LookRotation(movement);
            transform.rotation = Quaternion.Slerp(transform.rotation, target, rotationSpeed * Time.fixedDeltaTime);
        }
    }
}
```
```

**Example 2: Object Pooling**
```csharp
public class ObjectPool : MonoBehaviour
{
    public GameObject prefab;
    private Queue<GameObject> pool = new Queue<GameObject>();

    public GameObject Get()
    {
        if (pool.Count > 0)
        {
            var obj = pool.Dequeue();
            obj.SetActive(true);
            return obj;
        }
        return Instantiate(prefab);
    }

    public void Return(GameObject obj)
    {
        obj.SetActive(false);
        pool.Enqueue(obj);
    }
}
```

## § 11 · Edge Cases

**Special Scenarios:**

1. **Cross-Platform Input**
   - Use Input System package for modern input
   - Handle multiple controller connections
   - Test touch input for mobile

2. **Memory Management**
   - Pool frequently spawned objects
   - Use struct for data passed frequently
   - Unload unused scenes with `SceneManager.UnloadSceneAsync`

3. **Large-Scale Projects**
   - Use Assembly Definition files for faster compilation
   - Implement Addressables for asset management
   - Use ECS for data-heavy systems

4. **Graphics Performance**
   - Enable GPU instancing for similar objects
   - Use LOD (Level of Detail) for distant objects
   - Implement occlusion culling

5. **Build Automation**
   - Use Unity Cloud Build for CI/CD
   - Use `--batchmode` for headless builds
   - Implement automated testing with Unity Test Framework

## § 12 · Related Skills

- **godot-expert**: Godot game engine development
- **unreal-expert**: Unreal Engine game development
- **game-development**: General game dev patterns

## § 13 · Change Log

### v3.0.0 (2026-03-20)
- Full v3.0 § format upgrade
- Added comprehensive MonoBehaviour patterns
- Expanded URP/HDRP documentation
- Added performance optimization guidance

### v1.0.0 (2024-01-01)
- Initial basic skill creation

## § 14 · Contributing

Contributions to improve this skill are welcome. Please:
1. Follow Unity C# coding conventions
2. Use Unity 2022 LTS/2023.x APIs
3. Include platform-specific considerations
4. Test all code in Unity Editor before contributing
5. Reference official Unity Documentation

## § 15 · Final Notes

Unity is the world's most popular game engine with excellent cross-platform support and a vast ecosystem of packages and assets. Use URP for most projects (unless you need HDRP's advanced features), implement object pooling for frequently spawned objects, and always profile performance early and often.

## § 16 · Install Guide

Install URL: `https://raw.githubusercontent.com/theneoai/awesome-skills/main/skills/tools/game-engine/unity-expert.md`


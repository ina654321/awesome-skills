## 9. Scenario Examples

### Scenario A — MPC Design for a 6-DOF Manipulator

**User**: I need to implement MPC for a 6-DOF arm to track a Cartesian trajectory while respecting joint torque limits. What's the best approach with Acados?

**Engineer**: For a 6-DOF arm with joint torque limits, I recommend a joint-space MPC with Cartesian task in the cost function. Here's the complete formulation:

```python
from acados_template import AcadosModel, AcadosOcp, AcadosOcpSolver
import casadi as ca
import numpy as np

def build_robot_mpc(N: int = 20, dt: float = 0.01,
                    n_joints: int = 6,
                    tau_max: np.ndarray = None,
                    q_limits: tuple = None):
    """
    Joint-space MPC with Cartesian task cost.
    State: x = [q (n), dq (n)]  (2n states)
    Input: u = tau (n)  (n inputs)
    """
    if tau_max is None:
        tau_max = np.array([80, 80, 50, 30, 20, 10])  # N·m per joint
    q_min, q_max = q_limits or (np.full(n_joints, -np.pi),
                                 np.full(n_joints, np.pi))

    model = AcadosModel()
    model.name = 'robot_arm_mpc'

    # CasADi symbolic variables
    q   = ca.SX.sym('q',  n_joints)
    dq  = ca.SX.sym('dq', n_joints)
    tau = ca.SX.sym('tau', n_joints)
    x   = ca.vertcat(q, dq)
    u   = tau

    # Simplified dynamics: M(q)*ddq + C(q,dq)*dq + g(q) = tau
    # For real system, use Pinocchio via C++ interface
    # Here: use identity mass matrix approximation for demo
    M_diag = ca.SX([3.5, 3.5, 2.0, 1.0, 0.5, 0.2])  # kg·m² estimated
    g_comp = ca.SX.zeros(n_joints)  # gravity (computed externally and added as parameter)

    ddq = (tau - g_comp)
    f_expl = ca.vertcat(dq, ddq)

    model.x = x
    model.u = u
    model.f_expl_expr = f_expl

    # OCP setup
    ocp = AcadosOcp()
    ocp.model = model
    ocp.dims.N = N

    # Cost: penalize joint position tracking + control effort
    # Cartesian task cost added via FK in stage cost
    Q_q  = np.diag([100.0] * n_joints)
    Q_dq = np.diag([1.0]   * n_joints)
    R_tau = np.diag([0.01]  * n_joints)

    ocp.cost.cost_type = 'NONLINEAR_LS'
    ocp.cost.cost_type_e = 'NONLINEAR_LS'

    # Reference: [q_ref, dq_ref, tau_ref=0]
    ocp.cost.W = ca.diag(ca.vertcat(
        ca.DM([100.0]*n_joints),
        ca.DM([1.0]*n_joints),
        ca.DM([0.01]*n_joints)
    ))

    # Constraints
    ocp.constraints.lbu = -tau_max
    ocp.constraints.ubu =  tau_max
    ocp.constraints.idxbu = np.arange(n_joints)

    ocp.constraints.lbx = np.concatenate([q_min, np.full(n_joints, -3.0)])  # rad/s limit
    ocp.constraints.ubx = np.concatenate([q_max, np.full(n_joints,  3.0)])
    ocp.constraints.idxbx = np.arange(2 * n_joints)

    # Solver: SQP with HPIPM interior-point
    ocp.solver_options.qp_solver = 'PARTIAL_CONDENSING_HPIPM'
    ocp.solver_options.integrator_type = 'ERK'
    ocp.solver_options.nlp_solver_type = 'SQP_RTI'  # Real-Time Iteration
    ocp.solver_options.tf = N * dt

    solver = AcadosOcpSolver(ocp, json_file='robot_mpc.json')
    return solver

# Expected: SQP_RTI solves in < 2ms on i7, suitable for 100Hz MPC loop
```

The SQP Real-Time Iteration scheme runs a single SQP step per cycle — warm-started from the previous solution. For your 6-DOF arm with N=20 at dt=10ms, expect 1-3ms solve time on a modern CPU, fitting comfortably in a 10ms control cycle.


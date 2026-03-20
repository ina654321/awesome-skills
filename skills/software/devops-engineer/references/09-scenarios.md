# Scenario Examples

## 9.1 Scenario: Kubernetes Pod Crash Loop

**User:** "One of our pods is in CrashLoopBackOff and I can't access the application. How do I debug this?"

**DevOps Engineer:**
> **CrashLoopBackOff means the container keeps crashing and restarting:**
> 
> **Step 1: Check Pod Status**
> ```bash
> kubectl describe pod <pod-name>
> kubectl logs <pod-name> --previous
> ```
> Look for the exit code and error message
> 
> **Common Causes:**
> 
> 1. **Application Error**
>    - Check logs for exceptions
>    - Misconfigured environment variables
>    - Missing dependencies
> 
> 2. **Resource Issues**
>    - OOMKilled: Increase memory limits
>    - CPU throttling: Increase CPU limits
> 
> 3. **Liveness Probe Failure**
>    - Check probe configuration
>    - Increase initialDelaySeconds
>    - Adjust timeout/period
> 
> 4. **Missing ConfigMap/Secret**
>    - Volume mounts not available
>    - Missing Kubernetes resources
> 
> **Quick Fixes:**
> ```bash
> # Increase resources
> kubectl patch deployment <name> -p '{"spec":{"template":{"spec":{"containers":[{"name":"app","resources":{"limits":{"memory":"512Mi"}}}]}}}}'
> 
> # Debug interactively
> kubectl run -it --rm debug --image=busybox -- /bin/sh
> ```
> 
> **Long-term:** Set proper resource requests/limits in deployment manifest

---

## 9.2 Scenario: Production Deployment Failed

**User:** "Our production deployment failed mid-way and now we're in a broken state. Half the pods are new version, half are old. What do we do?"

**DevOps Engineer:**
> **This is a partial deployment failure — let's recover:**
> 
> **Immediate Assessment:**
> 1. Is the application still serving? (It might be)
> 2. What exactly failed? (Image pull? Init container? Probe?)
> 3. Are users affected?
> 
> **Option A: Rollback (Fastest)**
> ```bash
> # Immediate rollback to previous version
> kubectl rollout undo deployment/<name>
> 
> # Or to specific revision
> kubectl rollout undo deployment/<name> --to-revision=3
> 
> # Monitor rollback
> kubectl rollout status deployment/<name>
> ```
> 
> **Option B: Fix and Redeploy (If you know the fix)**
> 1. Fix the issue in code/config
> 2. Update image tag or config
> 3. Redeploy with rolling update
> 
> **Prevention for Future:**
> - Add deployment verification step
> - Configure failureThreshold and progressDeadlineSeconds
> - Use readiness gates for deployment validation
> - Have automated smoke tests
> 
> **Post-Incident:**
> - Document what failed
> - Add health checks
> - Create deployment checklist

---

## 9.3 Scenario: High Cloud Costs

**User:** "Our AWS bill tripled this month. How do I find out what's causing the spike?"

**DevOps Engineer:**
> **Systematic cost analysis approach:**
> 
> **Step 1: Identify the Service**
> - Check AWS Cost Explorer
> - Look at linked accounts/services
> - Identify spike timeframe
> 
> **Step 2: Resource Analysis**
> ```bash
> # Check running instances
> aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,State,Tags]'
> 
> # Check RDS
> aws rds describe-db-instances
> 
> # Check EBS volumes
> aws ec2 describe-volumes --query 'Volumes[*].[VolumeId,Size,State,VolumeType]'
> ```
> 
> **Common Culprits:**
> 
> 1. **RDS Misconfigured**: Large instance left running
> 2. **EBS Snapshots**: Too many retained
> 3. **Data Transfer**: Cross-region or out to internet
> 4. **NAT Gateway**: Used heavily with large instances
> 5. **Elastic IPs**: Attached to stopped instances
> 
> **Quick Wins:**
> - Delete unattached EBS volumes
> - Stop dev/test instances at night
> - Right-size over-provisioned instances
> - Use Reserved Instances for steady-state
> 
> **Long-term:**
> - Set up cost alerts
> - Use budget tracking
> - Implement resource tagging
> - Regular cost reviews
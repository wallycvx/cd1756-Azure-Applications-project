# Write-up Template

### Analyze, choose, and justify the appropriate resource option for deploying the app.

*For **both** a VM or App Service solution for the CMS app:*
- *Analyze costs, scalability, availability, and workflow*
- *Choose the appropriate solution (VM or App Service) for deploying the app*
- *Justify your choice*

### Assess app changes that would change your decision.

### Comparing Virtual Machine(VM) and App Service.
#### VM
Cost: You pay for full control of compute resources and cost-effective if workloads are predictable and long-term running.
Scalability: You have full flexibility to scale vertically(bigger VM) and horizontally(VM scale sets). VM scale sets support autoscaling, but user must own its configuration and maintenance. Scaling is slower because VM provisioning is slower.
Availability: User controls availability strategy, highly available but owns configuration and maintenance. OS patching, failover scripts, and redundancy is user’s responsibility.
Workflow: Full control over OS, runtime, networking, and deployment pipeline. Requires more DevOps overhead. Hiher operational cost, slower deployment and scaling, more complex to secure and monitor. Cost can grow quickly if not optimized.

#### App Service.
Cost: You pay for the App Service plan, not the underlying OS. Cheaper for web apps because you are paying for full VM capacity. Built-in scaling and patching reduce ops cost.
Scalability: Autoscaling is built-in and very fast because you are not scaling the whole VM. It supports high-density hosting with multiple apps per plan.
Availability: High availability is built-in. MS handles OS patching, platform updates, and infrastructure redundancy. Easy deployment slots for zero-downtime releases.
Workflow: Very streamlined, GitHub Actions, DevOps pipelines, deployment slots, built‑in logging. No OS management responsibility. Great for teams that want to focus on code and not infrastructure.
Less control of OS and runtime. Not suitable for apps requiring custom drivers, depp OS access, or unusual networking.

#### My Choice
In my case, I want a fully managed platform with minimal ops overhead. Fast autoscaling and zero-downtime deployments. CI/CD integration and modern DevOps workflows with built-in authentication, custom domains, ssl, and logging. App Service is suitable for me.


*Detail how the app and any other needs would have to change for you to change your decision in the last section.* 
If my requirements will later change to having full OS Control, running legacy or custom application hosting sensitive/personal identification data with predictable long-term running workloads on GPU or specialized hardware, then I will consider to change my application deployments to Virtual Machine.
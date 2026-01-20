# Write-up Template

### Analyze, choose, and justify the appropriate resource option for deploying the app.

*For **both** a VM or App Service solution for the CMS app:*
- *Analyze costs, scalability, availability, and workflow*
- *Choose the appropriate solution (VM or App Service) for deploying the app*
- *Justify your choice*

### Assess app changes that would change your decision.
For my Flask application, I will choose Azure web app services over Virtual Machine. This is because my application is lightweighted as of now, no sensitive data that warrant secluded infrastructure, hence reduce my overhead cost because I will only pay for the web hosting plan. App services provide strimlined deployment workflow. It also automates the scale out or up the resources when the traffic is at the peak and the application is expected to maintain its high availability. Web App Services has the ability scale back down and/or in when the resources are not needed.

*Detail how the app and any other needs would have to change for you to change your decision in the last section.* 
The choice will change if I need to deal with highly sensitive data that warrant building dedicated infrastructure. High Volume of data that do not need as much availability.
# Cloud Infrastructure RFP - Acme Corp

## 1. Company Overview
Acme Corp is a multinational financial services firm founded in 2004. Our primary platform processes over 50 million daily transactions.

## 2. Technical and Security Requirements
Vendors responding to this RFP must confirm adherence to the following criteria:

- REQ-01: The vendor must provide SOC 2 Type II compliance reports audited within the last 12 months. (Mandatory)
- REQ-02: All customer data at rest must be encrypted using AES-256 keys managed via a dedicated HSM or cloud KMS. (Mandatory)
- REQ-03: The system should offer out-of-the-box integration with Okta via SAML 2.0 or OIDC. (Preferred)
- REQ-04: Disaster recovery systems must maintain a Recovery Point Objective (RPO) of under 15 minutes and a Recovery Time Objective (RTO) of under 1 hour. (Mandatory)
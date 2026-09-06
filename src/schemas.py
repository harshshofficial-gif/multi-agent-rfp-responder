from enum import Enum
from pydantic import BaseModel
from pydantic import Field
from typing import List, Optional, Dict, Any, Union

class RequirementCategory(str, Enum):
    TECHNICAL = "Technical"
    PRICING = "Pricing"
    LEGAL = "Legal"
    
class RequirementStatus(str, Enum):
    EXTRACTED = "Extracted"
    RETRIEVED = "Retrieved"
    DRAFTED = "Drafted"
    COMPLIANT = "Compliant"
    FLAGGED = "Flagged"

class RFPRequirement(BaseModel):
    id: str = Field(..., description="Unique identifier for the requirement")
    raw_text: str = Field(..., description="The raw text of the requirement")
    category: RequirementCategory = Field(..., description="The category of the requirement")
    is_mandatory: bool = Field(default=True, description="Indicates if the requirement is mandatory")
    reviewed_evidence: List[str] = Field(default_factory=list, description="List of reviewed evidence for the requirement")
    response_draft: Optional[str] = Field(default = None, description="Draft response for the requirement")
    compliance_notes: Optional[str] = Field(default = None, description="Notes on compliance for the requirement")
    status: RequirementStatus = Field(default=RequirementStatus.EXTRACTED, description="The status of the requirement")


class RFPState(BaseModel):
    document_path: str = Field(..., description="Path to the RFP document")
    requirements: List[RFPRequirement] = Field(default_factory=list, description="List of requirements extracted from the RFP")
    current_stage: str = Field(default="parsing", description="The current stage of the RFP")
    revision_count: int = Field(default=0, description="Number of times the RFP has been revised")
    max_revisions: int = Field(default=2, description="Maximum allowed revisions")

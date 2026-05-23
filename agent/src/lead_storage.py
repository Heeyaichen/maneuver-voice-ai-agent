"""Lead data storage and persistence."""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger("lead_storage")


class LeadStorage:
    """Manages lead data capture and persistence."""
    
    def __init__(self, storage_dir: str = "leads"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.current_lead: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "name": None,
            "company": None,
            "role": None,
            "problem": None,
            "business_metrics": None,
            "ai_context": None,
            "timeline": None,
            "budget": None,
            "current_solutions": None,
            "additional_notes": [],
        }
    
    def update_field(self, field: str, value: str) -> bool:
        """
        Update a lead field with a value.
        
        Args:
            field: The field name (e.g., 'name', 'company', 'problem')
            value: The value to store
        
        Returns:
            True if successful, False otherwise
        """
        field_lower = field.lower().replace(" ", "_")
        
        # Map common variations to standard fields
        field_map = {
            "name": "name",
            "full_name": "name",
            "contact_name": "name",
            "company": "company",
            "company_name": "company",
            "organization": "company",
            "role": "role",
            "title": "role",
            "position": "role",
            "job_title": "role",
            "problem": "problem",
            "challenge": "problem",
            "pain_point": "problem",
            "issue": "problem",
            "business_metrics": "business_metrics",
            "metrics": "business_metrics",
            "kpis": "business_metrics",
            "goals": "business_metrics",
            "ai_context": "ai_context",
            "ai_experience": "ai_context",
            "current_ai": "ai_context",
            "timeline": "timeline",
            "timeframe": "timeline",
            "when": "timeline",
            "budget": "budget",
            "price_range": "budget",
            "investment": "budget",
            "current_solutions": "current_solutions",
            "current_tools": "current_solutions",
            "existing_solutions": "current_solutions",
            "what_tried": "current_solutions",
        }

        
        mapped_field = field_map.get(field_lower, field_lower)
        
        if mapped_field in self.current_lead:
            self.current_lead[mapped_field] = value
            logger.info(f"Updated lead field: {mapped_field} = {value}")
            return True
        else:
            # Store as additional note if not a standard field
            self.current_lead["additional_notes"].append(f"{field}: {value}")
            logger.info(f"Added to additional notes: {field} = {value}")
            return True
    
    def get_lead_data(self) -> Dict[str, Any]:
        """Get current lead data."""
        return self.current_lead.copy()
    
    def save_lead(self, session_id: str = None) -> str:
        """
        Save current lead to JSON file.
        
        Args:
            session_id: Optional session identifier
        
        Returns:
            Path to saved file
        """
        if session_id is None:
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        filename = self.storage_dir / f"lead_{session_id}.json"
        
        with open(filename, "w") as f:
            json.dump(self.current_lead, f, indent=2)
        
        logger.info(f"Saved lead data to {filename}")
        return str(filename)
    
    def get_summary(self) -> str:
        """Get a human-readable summary of captured lead data."""
        summary_parts = []
        
        for field, value in self.current_lead.items():
            if field == "timestamp":
                continue
            if field == "additional_notes":
                if value:
                    summary_parts.append(f"Additional notes: {', '.join(value)}")
            elif value:
                summary_parts.append(f"{field.replace('_', ' ').title()}: {value}")
        
        if not summary_parts:
            return "No information captured yet."
        
        return "\n".join(summary_parts)

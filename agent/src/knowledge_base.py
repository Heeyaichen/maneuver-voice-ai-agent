"""Knowledge base loader for Maneuver company information."""

from pathlib import Path


class KnowledgeBase:
    """Loads and retrieves Maneuver company information."""

    def __init__(self):
        self.knowledge = self._load_knowledge()

    def _load_knowledge(self) -> dict:
        """Load knowledge from markdown file."""
        kb_path = Path(__file__).parent / "maneuver_knowledge.md"

        if not kb_path.exists():
            return {}

        with open(kb_path) as f:
            content = f.read()

        # Parse sections
        sections = {}
        current_section = None
        current_content = []

        for line in content.split("\n"):
            if line.startswith("## "):
                if current_section:
                    sections[current_section.lower()] = "\n".join(
                        current_content
                    ).strip()
                current_section = line[3:].strip()
                current_content = []
            else:
                current_content.append(line)

        # Add last section
        if current_section:
            sections[current_section.lower()] = "\n".join(current_content).strip()

        return sections

    def get_info(self, topic: str) -> str:
        """
        Retrieve information about a specific topic.

        Args:
            topic: The topic to retrieve (e.g., 'services', 'pricing', 'process')

        Returns:
            Information about the topic, or a message if not found
        """
        topic_lower = topic.lower()

        # Direct match
        if topic_lower in self.knowledge:
            return self.knowledge[topic_lower]

        # Fuzzy matching for common queries
        topic_map = {
            "service": "services",
            "what you do": "what we do",
            "about": "what we do",
            "price": "pricing",
            "cost": "pricing",
            "how much": "pricing",
            "case study": "case studies",
            "example": "case studies",
            "results": "case studies",
            "team": "team",
            "founder": "team",
            "who": "team",
            "process": "process",
            "how it works": "process",
            "steps": "process",
        }

        for key, value in topic_map.items():
            if key in topic_lower:
                return self.knowledge.get(value, "")

        # Return all if no specific match
        return "\n\n".join([f"**{k.title()}**\n{v}" for k, v in self.knowledge.items()])

    def get_all(self) -> str:
        """Get all knowledge base content."""
        return "\n\n".join([f"**{k.title()}**\n{v}" for k, v in self.knowledge.items()])

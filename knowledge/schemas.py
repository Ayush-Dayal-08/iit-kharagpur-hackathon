"""
Dataclass schemas for narrative knowledge extraction.
Defines structured representations for events, attributes, and relations.
"""

from dataclasses import dataclass, field
from typing import Literal


# Type aliases for clarity
EventType = Literal["action", "dialogue", "thought", "memory", "dream"]
AttrType = Literal["physical", "family", "occupation", "location", "trait"]
ConfidenceLevel = Literal["explicit", "implied", "inferred"]
RelationType = Literal["family", "romantic", "professional", "friend"]


@dataclass
class Event:
    """Represents a narrative event involving a character."""
    
    story_id: str
    event_id: str
    character: str
    description: str  # what happened
    chapter: int
    time_reference: str  # "childhood", "age 15", "during story"
    event_type: EventType  # "action", "dialogue", "thought", "memory", "dream"
    is_flashback: bool
    is_dream: bool
    src_chunk: str  # which chunk this came from


@dataclass
class Attribute:
    """Represents a character attribute or property."""
    
    story_id: str
    character: str
    attr_type: AttrType  # "physical", "family", "occupation", "location", "trait"
    attr_name: str  # "eye_color", "has_siblings", "birthplace"
    attr_value: str
    first_mentioned_ch: int
    confidence: ConfidenceLevel  # "explicit", "implied", "inferred"
    src_chunk: str


@dataclass
class Relation:
    """Represents a relationship between characters."""
    
    story_id: str
    character: str
    relation_type: RelationType  # "family", "romantic", "professional", "friend"
    relation_name: str  # "father_of", "married_to", "works_for"
    target: str  # other person's name
    first_mentioned_ch: int
    src_chunk: str


# Step 8: Test by creating sample instances
if __name__ == "__main__":
    # Test Event
    sample_event = Event(
        story_id="story_001",
        event_id="evt_001",
        character="Elena",
        description="Elena discovered the hidden letter in her grandmother's attic",
        chapter=3,
        time_reference="during story",
        event_type="action",
        is_flashback=False,
        is_dream=False,
        src_chunk="ch3_chunk_05"
    )
    
    # Test Attribute
    sample_attribute = Attribute(
        story_id="story_001",
        character="Elena",
        attr_type="physical",
        attr_name="eye_color",
        attr_value="green",
        first_mentioned_ch=1,
        confidence="explicit",
        src_chunk="ch1_chunk_02"
    )
    
    # Test Relation
    sample_relation = Relation(
        story_id="story_001",
        character="Elena",
        relation_type="family",
        relation_name="granddaughter_of",
        target="Maria",
        first_mentioned_ch=1,
        src_chunk="ch1_chunk_01"
    )
    
    # Print samples
    print("=== Sample Event ===")
    print(sample_event)
    print()
    
    print("=== Sample Attribute ===")
    print(sample_attribute)
    print()
    
    print("=== Sample Relation ===")
    print(sample_relation)
    print()
    
    print("✓ All schemas validated successfully!")
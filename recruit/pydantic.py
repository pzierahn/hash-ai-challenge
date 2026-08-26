from pydantic import BaseModel, Field


class RoleCriterion(BaseModel):
    name: str = Field(
        ...,
        description="Short label for the criterion (e.g., 'Master's in CS', '5+ Years Backend', 'React Proficiency')",
    )
    description: str = Field(
        ...,
        description="Concise description of the requirement covering skill, education, experience, or background",
    )


class RoleRequirements(BaseModel):
    required: list[RoleCriterion] = Field(
        ...,
        description="Mandatory, non-negotiable requirements for the role",
    )
    preferred: list[RoleCriterion] = Field(
        ...,
        description="Nice-to-have qualifications and preferred background",
    )

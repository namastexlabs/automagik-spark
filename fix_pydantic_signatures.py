#!/usr/bin/env python3
"""Fix Pydantic model_validate signature incompatibilities."""

import re


def fix_model_validate_signatures(file_path: str) -> None:
    """Fix all model_validate method signatures to match BaseModel."""

    with open(file_path, "r") as f:
        content = f.read()

    # Pattern to match the old signature
    old_pattern = r'(@classmethod\s+def model_validate\(cls, obj: Any\) -> "(?:TaskResponse|WorkflowListResponse|WorkflowResponse|ScheduleResponse)":\s+"""[^"]+""")'

    # For TaskResponse and ScheduleResponse (they use super().model_validate)
    def replace_with_super(match):
        class_name = match.group(1).split('"')[1]
        method_start = match.group(0)

        # Find the complete method body
        start_pos = content.find(method_start)
        if start_pos == -1:
            return match.group(0)

        # Find where this method ends (next method or class definition)
        method_content = content[start_pos:]

        # Replace signature
        new_signature = f'''@classmethod
    def model_validate(
        cls,
        obj: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: dict[str, Any] | None = None,
    ) -> "{class_name}":
        """Convert a {class_name.replace("Response", "")} object to {class_name}."""'''

        return new_signature

    # Replace TaskResponse signature (line 54)
    content = re.sub(
        r'(@classmethod\s+def model_validate\(cls, obj: Any\) -> "TaskResponse":\s+"""Convert a Task object to TaskResponse\.""")',
        '''@classmethod
    def model_validate(
        cls,
        obj: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: dict[str, Any] | None = None,
    ) -> "TaskResponse":
        """Convert a Task object to TaskResponse."""''',
        content,
    )

    # Replace super().model_validate(data) calls for TaskResponse
    content = re.sub(
        r"(            return super\(\)\.model_validate\(data\))\n(        return super\(\)\.model_validate\(obj\))",
        r"""            return super().model_validate(
                data, strict=strict, from_attributes=from_attributes, context=context
            )
        return super().model_validate(
            obj, strict=strict, from_attributes=from_attributes, context=context
        )""",
        content,
        count=1,
    )

    # Replace WorkflowListResponse signature (line 150)
    content = re.sub(
        r'(@classmethod\s+def model_validate\(cls, obj: Any\) -> "WorkflowListResponse":\s+"""Convert a Workflow object to WorkflowListResponse\.""")',
        '''@classmethod
    def model_validate(
        cls,
        obj: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: dict[str, Any] | None = None,
    ) -> "WorkflowListResponse":
        """Convert a Workflow object to WorkflowListResponse."""''',
        content,
    )

    # Replace WorkflowResponse signature (line 198)
    content = re.sub(
        r'(@classmethod\s+def model_validate\(cls, obj: Any\) -> "WorkflowResponse":\s+"""Convert a Workflow object to WorkflowResponse\.""")',
        '''@classmethod
    def model_validate(
        cls,
        obj: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: dict[str, Any] | None = None,
    ) -> "WorkflowResponse":
        """Convert a Workflow object to WorkflowResponse."""''',
        content,
    )

    # Replace ScheduleResponse signature (line 278)
    content = re.sub(
        r'(@classmethod\s+def model_validate\(cls, obj: Any\) -> "ScheduleResponse":\s+"""Convert a Schedule object to ScheduleResponse\.""")',
        '''@classmethod
    def model_validate(
        cls,
        obj: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: dict[str, Any] | None = None,
    ) -> "ScheduleResponse":
        """Convert a Schedule object to ScheduleResponse."""''',
        content,
    )

    # Replace super().model_validate calls for ScheduleResponse (the second occurrence)
    # Find the ScheduleResponse class and replace its super() calls
    schedule_response_pattern = r"(class ScheduleResponse.*?)(return super\(\)\.model_validate\(data\))\n(\s+return super\(\)\.model_validate\(obj\))"

    def replace_schedule_super(match):
        class_content = match.group(1)
        return (
            class_content
            + """return super().model_validate(
                data, strict=strict, from_attributes=from_attributes, context=context
            )
        return super().model_validate(
            obj, strict=strict, from_attributes=from_attributes, context=context
        )"""
        )

    content = re.sub(schedule_response_pattern, replace_schedule_super, content, flags=re.DOTALL)

    # Write back
    with open(file_path, "w") as f:
        f.write(content)

    print(f"Fixed model_validate signatures in {file_path}")


if __name__ == "__main__":
    fix_model_validate_signatures("/home/cezar/automagik/automagik-spark/automagik_spark/api/models.py")

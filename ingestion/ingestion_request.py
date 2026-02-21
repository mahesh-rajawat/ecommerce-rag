from pydantic import BaseModel, Field, model_validator


class IngestRequest(BaseModel):
    company: str
    domain: str | None = Field(
        default=None,
        description="What is this data about? E.g. sales, hr, policy"
    )

    text: str | None = None
    file_path: str | None = None
    dir_path: str | None = None
    url: str | None = None

    source_type: str | None = None  # auto-set

    @model_validator(mode="after")
    def detect_source(self):

        sources = {
            "text": self.text,
            "file": self.file_path,
            "dir": self.dir_path,
            "url": self.url
        }

        active = [k for k, v in sources.items() if v]

        if len(active) != 1:
            raise ValueError(
                "Provide exactly one source: text, file_path, dir_path, or url"
            )

        # Auto-set source type
        self.source_type = active[0]

        return self

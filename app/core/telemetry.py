import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup_telemetry(app):
    if os.getenv("ENABLE_TELEMETRY") != "true":
        return

    from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
        OTLPSpanExporter,
    )
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

    provider = TracerProvider()
    trace.set_tracer_provider(provider)

    exporter = OTLPSpanExporter(
        endpoint="http://localhost:4318/v1/traces"
    )

    provider.add_span_processor(
        BatchSpanProcessor(exporter)
    )

    # 🔥 auto-instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)

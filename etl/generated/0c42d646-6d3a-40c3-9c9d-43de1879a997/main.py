import argparse
import asyncio
import logging
import signal
import sys
import time
from typing import Any, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PipelineOrchestrator:
    async def run(self, phase: str, dry_run: bool) -> Dict[str, Any]:
        start_time = time.time()
        logger.info(f"Starting phase: {phase}")
        # Simulate processing
        await asyncio.sleep(1)  # Simulate async work
        duration = time.time() - start_time
        logger.info(f"Completed phase: {phase} in {duration:.2f} seconds")
        return {"duration": duration, "rows_processed": 100, "errors": []}

async def main(config_path: str, dry_run: bool, phase: str) -> int:
    orchestrator = PipelineOrchestrator()
    execution_summary = {"total_duration": 0, "total_rows": 0, "total_errors": 0}
    
    phases = ["extract", "transform", "validate", "load"] if phase == "all" else [phase]
    
    for phase in phases:
        result = await orchestrator.run(phase, dry_run)
        execution_summary["total_duration"] += result["duration"]
        execution_summary["total_rows"] += result["rows_processed"]
        execution_summary["total_errors"] += len(result["errors"])
    
    logger.info(f"Execution Summary: {execution_summary}")
    
    if execution_summary["total_errors"] > 0:
        return 1  # Partial failure
    return 0  # Success

def signal_handler(sig: int, frame: Any) -> None:
    logger.info("Graceful shutdown initiated.")
    sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Global Data Analytics Pipeline")
    parser.add_argument("--config", type=str, required=True, help="Path to the configuration file")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without making changes")
    parser.add_argument("--phase", type=str, choices=["extract", "transform", "validate", "load", "all"], required=True, help="Phase to execute")
    
    args = parser.parse_args()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        exit_code = asyncio.run(main(args.config, args.dry_run, args.phase))
        sys.exit(exit_code)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(2)
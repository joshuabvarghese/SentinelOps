import asyncio
import psutil
import json
import logging
from datetime import datetime
from typing import Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# 1. Setup Logging so we can see the engine working
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

@dataclass
class HealthCheck:
    name: str
    status: HealthStatus
    message: str
    timestamp: str
    metadata: Dict

class SystemMonitor:
    """The Engine: Interacts with the OS to get hardware stats"""
    def __init__(self):
        self.thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 85.0,
            'disk_percent': 90.0
        }

    def check_cpu(self) -> HealthCheck:
        usage = psutil.cpu_percent(interval=1)
        status = HealthStatus.HEALTHY if usage < self.thresholds['cpu_percent'] else HealthStatus.UNHEALTHY
        return HealthCheck(
            name="CPU Usage",
            status=status.value,
            message=f"CPU at {usage}%",
            timestamp=datetime.now().isoformat(),
            metadata={"usage_percent": usage}
        )

    def check_memory(self) -> HealthCheck:
        mem = psutil.virtual_memory()
        status = HealthStatus.HEALTHY if mem.percent < self.thresholds['memory_percent'] else HealthStatus.UNHEALTHY
        return HealthCheck(
            name="Memory Usage",
            status=status.value,
            message=f"RAM at {mem.percent}%",
            timestamp=datetime.now().isoformat(),
            metadata={"used_gb": round(mem.used / (1024**3), 2), "percent": mem.percent}
        )

class MonitoringService:
    """The Orchestrator: Runs the engine and saves the data"""
    def __init__(self, interval=30):
        self.monitor = SystemMonitor()
        self.interval = interval

    async def start(self):
        logger.info(f"Engine started. Checking every {self.interval}s...")
        while True:
            # Gather data
            results = {
                "last_updated": datetime.now().isoformat(),
                "checks": [
                    asdict(self.monitor.check_cpu()),
                    asdict(self.monitor.check_memory())
                ]
            }
            
            # Save to file (This is the bridge to the Dashboard)
            with open('monitoring_results.json', 'w') as f:
                json.dump(results, f, indent=2)
            
            logger.info("Metrics updated in monitoring_results.json")
            await asyncio.sleep(self.interval)

if __name__ == "__main__":
    service = MonitoringService()
    asyncio.run(service.start())
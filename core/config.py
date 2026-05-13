import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the .env file in the root directory
load_dotenv()

class AuraConfig:
    """
    Centralized configuration for the Aura Agent.
    Optimized for Intel i5 + RTX 3050 (6GB VRAM).
    """
    
    # --- Project Metadata ---
    PROJECT_NAME = "Aura"
    VERSION = "0.1.0"
    ROOT_DIR = Path(__file__).parent.parent
    
    # --- API Credentials (Zero-Trust Approach) ---
    # Ensure GEMINI_API_KEY is defined in your root .env file
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # --- Audio Engine Optimization (STT) ---
    # Optimized for CUDA to achieve sub-200ms processing
    WHISPER_MODEL = "small.en"
    DEVICE_TYPE = "cuda" # Targeted for RTX 3050[cite: 2]
    COMPUTE_TYPE = "int8_float16" # Balanced precision for 6GB VRAM[cite: 2]
    VRAM_LIMIT_GB = 1.0 # STT specific VRAM ceiling[cite: 2]
    VRAM_TTL_MINUTES = 10 # Time before unloading model from VRAM[cite: 2]
    
    # --- Automation Settings (Playwright) ---
    # Browser flags to offload rendering to CPU[cite: 2]
    BROWSER_HEADLESS = True
    BROWSER_ARGS = [
        "--disable-extensions",
        "--disable-gpu", # Preserve VRAM for Whisper/System[cite: 2]
        "--no-sandbox"
    ]
    WHATSAPP_SESSION_PATH = ROOT_DIR / "skills" / "whatsapp_session"
    
    # --- Security & HITL ---
    HITL_ENABLED = True # Enforces Human-in-the-Loop for high-stakes tasks[cite: 2]
    LOG_LEVEL = "INFO"

    @classmethod
    def validate_config(cls):
        """Simple check to ensure core credentials exist."""
        if not cls.GEMINI_API_KEY:
            raise ValueError("CRITICAL: GEMINI_API_KEY not found in .env file.")
        
        # Ensure session directory exists for the WhatsApp Controller
        cls.WHATSAPP_SESSION_PATH.mkdir(parents=True, exist_ok=True)